"""Recency, training-tercile RFM, and the original BG/NBD likelihood."""

import numpy as np
from scipy.optimize import minimize
from scipy.special import betaln, expit, gammaln


def bg_log_likelihood(parameters, x, tx, age):
    r, alpha, a, b = parameters
    common = gammaln(r + x) - gammaln(r) + r * np.log(alpha) + betaln(a, b + x) - betaln(a, b)
    alive = -(r + x) * np.log(alpha + age)
    dead = np.full_like(alive, -np.inf)
    mask = x > 0
    dead[mask] = np.log(a) - np.log(b + x[mask] - 1) - (r + x[mask]) * np.log(alpha + tx[mask])
    return common + np.logaddexp(alive, dead)


class BGNBD:
    def fit(self, frame):
        latest = frame[frame.cutoff == frame.cutoff.max()]
        x, tx, age = self.inputs(latest)
        attempts = []
        for start in ([1, 30, 1, 3], [0.3, 10, 0.5, 5], [2, 100, 2, 10]):
            result = minimize(
                lambda theta: -bg_log_likelihood(np.exp(theta), x, tx, age).mean(),
                np.log(start),
                method="L-BFGS-B",
                bounds=[(-10, 15)] * 4,
                options={"maxiter": 2000, "ftol": 1e-12},
            )
            attempts.append(
                {
                    "start": start,
                    "success": bool(result.success),
                    "objective": float(result.fun),
                    "message": str(result.message),
                    "parameters": np.exp(result.x).tolist(),
                }
            )
        self.attempts = attempts
        good = [a for a in attempts if a["success"] and np.isfinite(a["objective"])]
        if not good:
            raise RuntimeError(f"BG/NBD did not converge: {attempts}")
        self.parameters = np.array(min(good, key=lambda a: a["objective"])["parameters"])
        return self

    @staticmethod
    def inputs(frame):
        return [
            frame[name].to_numpy(float)
            for name in ("bg_repeat_days", "bg_recency_days", "bg_age_days")
        ]

    def probability_alive(self, frame):
        x, tx, age = self.inputs(frame)
        r, alpha, a, b = self.parameters
        log_odds = np.full(len(x), -np.inf)
        mask = x > 0
        log_odds[mask] = (
            np.log(a)
            - np.log(b + x[mask] - 1)
            + (r + x[mask]) * np.log((alpha + age[mask]) / (alpha + tx[mask]))
        )
        return expit(-log_odds)

    def predict(self, frame, horizon=90):
        x, _, age = self.inputs(frame)
        r, alpha, _, _ = self.parameters
        alive = self.probability_alive(frame)
        # If alive, zero future arrivals is the posterior gamma-Poisson zero probability.
        zero_if_alive = np.exp((r + x) * np.log((alpha + age) / (alpha + age + horizon)))
        return 1 - alive + alive * zero_if_alive


class RFM:
    columns = ["recency_days", "frequency_365", "monetary_365"]

    def codes(self, frame):
        return sum(
            np.searchsorted(cuts, frame[col], side="left") * 3**i
            for i, (col, cuts) in enumerate(zip(self.columns, self.cuts, strict=True))
        )

    def fit(self, frame):
        self.cuts = [np.quantile(frame[col], [1 / 3, 2 / 3]) for col in self.columns]
        codes = self.codes(frame)
        self.base = float(frame.churn.mean())
        self.risk = {
            int(k): float((frame.churn.to_numpy()[codes == k].sum() + 1) / ((codes == k).sum() + 2))
            for k in np.unique(codes)
        }
        return self

    def predict(self, frame):
        return np.array([self.risk.get(int(k), self.base) for k in self.codes(frame)])


class Recency:
    def fit(self, frame):
        self.base = float(frame.churn.mean())
        return self

    def predict(self, frame):
        # Uncalibrated ranking score is raw recency. Without forward calibration,
        # probabilities fall back to training prevalence, not invented probabilities.
        return np.full(len(frame), self.base)
