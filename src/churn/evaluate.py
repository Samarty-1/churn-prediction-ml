"""Customer-cluster bootstrap; frozen policies, paired comparisons and calibration bins."""

import numpy as np


class Metrics:
    def __init__(self, frame):
        self.y = frame.churn.to_numpy(float)
        self.p = frame.probability.to_numpy(float)
        self.profit = frame.profit.to_numpy(float)
        self.order = np.lexsort((frame.customer_id.to_numpy(str), -self.p))
        self.ends = np.r_[np.flatnonzero(np.diff(self.p[self.order]) != 0), len(frame) - 1]
        self.top = {}
        # Pooled precision/lift retain each cutoff's top fraction, not a global campaign.
        for fraction in (0.1, 0.2):
            selected = np.zeros(len(frame), bool)
            for _, indices in frame.groupby("cutoff", sort=False).indices.items():
                local = indices[
                    np.lexsort((frame.customer_id.iloc[indices].to_numpy(str), -self.p[indices]))
                ]
                selected[local[: int(np.ceil(len(local) * fraction))]] = True
            self.top[fraction] = selected

    def calculate(self, weights=None):
        w = np.ones(len(self.y)) if weights is None else weights
        total = w.sum()
        pos = (w * self.y).sum()
        neg = total - pos
        if total == 0:
            return {}
        tp = np.cumsum((w * self.y)[self.order])[self.ends]
        fp = np.cumsum((w * (1 - self.y))[self.order])[self.ends]
        delta_tp, delta_fp = np.diff(np.r_[0, tp]), np.diff(np.r_[0, fp])
        precision = np.divide(tp, tp + fp, out=np.zeros_like(tp), where=tp + fp > 0)
        result = {
            "pr_auc": float(np.sum(delta_tp * precision) / pos) if pos else np.nan,
            "roc_auc": float(np.sum(delta_fp * (tp - delta_tp / 2)) / (pos * neg))
            if pos and neg
            else np.nan,
            "brier": float(np.sum(w * (self.p - self.y) ** 2) / total),
            "base_rate": float(pos / total),
            "profit": float(np.sum(w * self.profit)),
            "profit_per_customer_cutoff": float(np.sum(w * self.profit) / total),
        }
        for fraction, selected in self.top.items():
            denom = w[selected].sum()
            prec = float((w[selected] * self.y[selected]).sum() / denom) if denom else np.nan
            result[f"precision_top_{int(fraction * 100)}"] = prec
            result[f"lift_top_{int(fraction * 100)}"] = prec / (pos / total) if pos else np.nan
        return result


def interval(values, alpha=0.05):
    finite = np.asarray(values)[np.isfinite(values)]
    if not len(finite):
        return [None, None]
    return np.quantile(finite, [alpha / 2, 1 - alpha / 2]).tolist()


def summarize(predictions, *, draws=2000, seed=20261105):
    output = {"bootstrap_draws": draws, "bootstrap_unit": "customer", "groups": {}}
    for name, group in [("pooled", predictions), *list(predictions.groupby("cutoff"))]:
        methods = {m: g.reset_index(drop=True) for m, g in group.groupby("method")}
        customers = sorted(group.customer_id.unique())
        index = {c: i for i, c in enumerate(customers)}
        lookup = {m: g.customer_id.map(index).to_numpy() for m, g in methods.items()}
        metrics = {m: Metrics(g) for m, g in methods.items()}
        point = {m: calc.calculate() for m, calc in metrics.items()}
        samples = {m: {k: [] for k in point[m]} for m in methods}
        rng = np.random.default_rng(seed)
        for _ in range(draws):
            weights = np.bincount(
                rng.integers(0, len(customers), len(customers)), minlength=len(customers)
            )
            for method, calc in metrics.items():
                result = calc.calculate(weights[lookup[method]])
                for key in samples[method]:
                    samples[method][key].append(result.get(key, np.nan))
        result = {}
        for method in methods:
            result[method] = {
                "rows": len(methods[method]),
                "contacts": int(methods[method].contact.sum()),
                "predicted_profit": float(
                    methods[method].predicted_gain.where(methods[method].contact, 0).sum()
                ),
                "metrics": {
                    key: {
                        "value": value if np.isfinite(value) else None,
                        "ci95": interval(samples[method][key]),
                    }
                    for key, value in point[method].items()
                },
            }
        comparisons = {}
        for ml in ("logistic", "lightgbm"):
            if ml not in methods:
                continue
            comparisons[ml] = {}
            for baseline in ("recency", "rfm", "bgnbd", "constant"):
                if baseline not in methods:
                    continue
                diff = np.array(samples[ml]["profit"]) - np.array(samples[baseline]["profit"])
                comparisons[ml][baseline] = {
                    "difference_gbp": point[ml]["profit"] - point[baseline]["profit"],
                    "ci95": interval(diff),
                    "ci_familywise95": interval(diff, alpha=0.05 / 3),
                }
        output["groups"][str(name)] = {"methods": result, "comparisons": comparisons}
        print(f"Bootstrapped {name}: {len(customers)} customer clusters", flush=True)
    return output


def reliability(predictions):
    rows = []
    for method, group in predictions.groupby("method"):
        bins = np.minimum((group.probability.to_numpy() * 10).astype(int), 9)
        for bucket in range(10):
            part = group[bins == bucket]
            if len(part):
                rows.append(
                    {
                        "method": method,
                        "bin": bucket,
                        "count": len(part),
                        "mean_probability": float(part.probability.mean()),
                        "observed_churn": float(part.churn.mean()),
                    }
                )
    return rows
