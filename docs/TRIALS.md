# Trial ledger

Generated from the append-only [full audit](../results/trials.jsonl).
Every fit, optimizer start, warning, candidate, calibration and threshold
is retained there. No unsuccessful result is removed.
Development selection is optimistic; the holdout is confirmatory.

| Audit line | Run | Event | Method | Context | Configuration / result |
|---:|---|---|---|---|---|
| 1 | development | candidate | logistic | outer:2010-11-09 | `{"config": {"C": 0.01}, "inner_average_precision": null, "validation_rows": 0}` |
| 2 | development | candidate | logistic | outer:2010-11-09 | `{"config": {"C": 0.1}, "inner_average_precision": null, "validation_rows": 0}` |
| 3 | development | candidate | logistic | outer:2010-11-09 | `{"config": {"C": 1.0}, "inner_average_precision": null, "validation_rows": 0}` |
| 4 | development | calibration | logistic | outer:2010-11-09 | `{"candidates": [{"reason": "no forward predictions"}], "selected": "native"}` |
| 5 | development | fit | logistic | outer:2010-11-09 | `{"config": {"C": 0.01}, "rows": 8944, "status": "ok", "warnings": []}` |
| 6 | development | outer_result | logistic | 2010-11-09 | `{"average_precision": 0.7765969981612858, "calibration": "native", "config": {"C": 0.01}, "contacts": 595, "cutoff": "2010-11-09", "profit": 7181.3428}` |
| 7 | development | candidate | lightgbm | outer:2010-11-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "inner_average_precision": null, "validation_rows": 0}` |
| 8 | development | candidate | lightgbm | outer:2010-11-09 | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "inner_average_precision": null, "validation_rows": 0}` |
| 9 | development | candidate | lightgbm | outer:2010-11-09 | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "inner_average_precision": null, "validation_rows": 0}` |
| 10 | development | candidate | lightgbm | outer:2010-11-09 | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "inner_average_precision": null, "validation_rows": 0}` |
| 11 | development | calibration | lightgbm | outer:2010-11-09 | `{"candidates": [{"reason": "no forward predictions"}], "selected": "native"}` |
| 12 | development | fit | lightgbm | outer:2010-11-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 8944, "status": "ok", "warnings": []}` |
| 13 | development | outer_result | lightgbm | 2010-11-09 | `{"average_precision": 0.7608403681124972, "calibration": "native", "config": {"min_child_samples": 50, "num_leaves": 7}, "contacts": 812, "cutoff": "2010-11-09", "profit": 8102.6900000000005}` |
| 14 | development | candidate | recency | outer:2010-11-09 | `{"config": {}, "inner_average_precision": null, "validation_rows": 0}` |
| 15 | development | calibration | recency | outer:2010-11-09 | `{"candidates": [{"reason": "no forward predictions"}], "selected": "native"}` |
| 16 | development | fit | recency | outer:2010-11-09 | `{"config": {}, "rows": 8944, "status": "ok", "warnings": []}` |
| 17 | development | outer_result | recency | 2010-11-09 | `{"average_precision": 0.5768268268268268, "calibration": "native", "config": {}, "contacts": 558, "cutoff": "2010-11-09", "profit": 4283.223300000001}` |
| 18 | development | candidate | rfm | outer:2010-11-09 | `{"config": {}, "inner_average_precision": null, "validation_rows": 0}` |
| 19 | development | calibration | rfm | outer:2010-11-09 | `{"candidates": [{"reason": "no forward predictions"}], "selected": "native"}` |
| 20 | development | fit | rfm | outer:2010-11-09 | `{"config": {}, "rows": 8944, "status": "ok", "warnings": []}` |
| 21 | development | outer_result | rfm | 2010-11-09 | `{"average_precision": 0.7572913008067184, "calibration": "native", "config": {}, "contacts": 1051, "cutoff": "2010-11-09", "profit": 7644.5389000000005}` |
| 22 | development | candidate | bgnbd | outer:2010-11-09 | `{"config": {}, "inner_average_precision": null, "validation_rows": 0}` |
| 23 | development | calibration | bgnbd | outer:2010-11-09 | `{"candidates": [{"reason": "no forward predictions"}], "selected": "native"}` |
| 24 | development | fit | bgnbd | outer:2010-11-09 | `{"config": {}, "rows": 8944, "status": "ok", "warnings": []}` |
| 25 | development | outer_result | bgnbd | 2010-11-09 | `{"average_precision": 0.7714896839455474, "calibration": "native", "config": {}, "contacts": 1288, "cutoff": "2010-11-09", "profit": 9250.6561}` |
| 26 | development | candidate | constant | outer:2010-11-09 | `{"config": {}, "inner_average_precision": null, "validation_rows": 0}` |
| 27 | development | calibration | constant | outer:2010-11-09 | `{"candidates": [{"reason": "no forward predictions"}], "selected": "native"}` |
| 28 | development | fit | constant | outer:2010-11-09 | `{"config": {}, "rows": 8944, "status": "ok", "warnings": []}` |
| 29 | development | outer_result | constant | 2010-11-09 | `{"average_precision": 0.5768268268268268, "calibration": "native", "config": {}, "contacts": 1583, "cutoff": "2010-11-09", "profit": 8025.511100000001}` |
| 30 | development | fit | logistic | inner:2010-09-09 | `{"config": {"C": 0.01}, "rows": 2760, "status": "ok", "warnings": []}` |
| 31 | development | candidate | logistic | outer:2010-12-09 | `{"config": {"C": 0.01}, "inner_average_precision": 0.6219621226996974, "validation_rows": 3337}` |
| 32 | development | fit | logistic | inner:2010-09-09 | `{"config": {"C": 0.1}, "rows": 2760, "status": "ok", "warnings": []}` |
| 33 | development | candidate | logistic | outer:2010-12-09 | `{"config": {"C": 0.1}, "inner_average_precision": 0.6213361103996957, "validation_rows": 3337}` |
| 34 | development | fit | logistic | inner:2010-09-09 | `{"config": {"C": 1.0}, "rows": 2760, "status": "ok", "warnings": []}` |
| 35 | development | candidate | logistic | outer:2010-12-09 | `{"config": {"C": 1.0}, "inner_average_precision": 0.6147438003203042, "validation_rows": 3337}` |
| 36 | development | calibration | logistic | outer:2010-12-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "platt"}` |
| 37 | development | fit | logistic | outer:2010-12-09 | `{"config": {"C": 0.01}, "rows": 12281, "status": "ok", "warnings": []}` |
| 38 | development | outer_result | logistic | 2010-12-09 | `{"average_precision": 0.8705977365039302, "calibration": "platt", "config": {"C": 0.01}, "contacts": 580, "cutoff": "2010-12-09", "profit": 10205.0623}` |
| 39 | development | fit | lightgbm | inner:2010-09-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 2760, "status": "ok", "warnings": []}` |
| 40 | development | candidate | lightgbm | outer:2010-12-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "inner_average_precision": 0.6033535768179181, "validation_rows": 3337}` |
| 41 | development | fit | lightgbm | inner:2010-09-09 | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "rows": 2760, "status": "ok", "warnings": []}` |
| 42 | development | candidate | lightgbm | outer:2010-12-09 | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "inner_average_precision": 0.5961962169062103, "validation_rows": 3337}` |
| 43 | development | fit | lightgbm | inner:2010-09-09 | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "rows": 2760, "status": "ok", "warnings": []}` |
| 44 | development | candidate | lightgbm | outer:2010-12-09 | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "inner_average_precision": 0.6001347918244024, "validation_rows": 3337}` |
| 45 | development | fit | lightgbm | inner:2010-09-09 | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "rows": 2760, "status": "ok", "warnings": []}` |
| 46 | development | candidate | lightgbm | outer:2010-12-09 | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "inner_average_precision": 0.5937309811781702, "validation_rows": 3337}` |
| 47 | development | calibration | lightgbm | outer:2010-12-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "platt"}` |
| 48 | development | fit | lightgbm | outer:2010-12-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 12281, "status": "ok", "warnings": []}` |
| 49 | development | outer_result | lightgbm | 2010-12-09 | `{"average_precision": 0.8688021660461567, "calibration": "platt", "config": {"min_child_samples": 50, "num_leaves": 7}, "contacts": 785, "cutoff": "2010-12-09", "profit": 11717.3714}` |
| 50 | development | fit | recency | inner:2010-09-09 | `{"config": {}, "rows": 2760, "status": "ok", "warnings": []}` |
| 51 | development | candidate | recency | outer:2010-12-09 | `{"config": {}, "inner_average_precision": 0.5609722987215954, "validation_rows": 3337}` |
| 52 | development | calibration | recency | outer:2010-12-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "platt"}` |
| 53 | development | threshold | recency | outer:2010-12-09 | `{"inner_profit": 486.15690000000006, "k": 30}` |
| 54 | development | threshold | recency | outer:2010-12-09 | `{"inner_profit": 348.68389999999994, "k": 60}` |
| 55 | development | threshold | recency | outer:2010-12-09 | `{"inner_profit": 0.0, "k": 90}` |
| 56 | development | threshold | recency | outer:2010-12-09 | `{"inner_profit": 0.0, "k": 120}` |
| 57 | development | threshold | recency | outer:2010-12-09 | `{"inner_profit": 0.0, "k": 180}` |
| 58 | development | threshold | recency | outer:2010-12-09 | `{"inner_profit": 0.0, "k": 270}` |
| 59 | development | fit | recency | outer:2010-12-09 | `{"config": {}, "rows": 12281, "status": "ok", "warnings": []}` |
| 60 | development | outer_result | recency | 2010-12-09 | `{"average_precision": 0.8267626563025885, "calibration": "platt", "config": {}, "contacts": 473, "cutoff": "2010-12-09", "profit": 6132.557900000001}` |
| 61 | development | fit | rfm | inner:2010-09-09 | `{"config": {}, "rows": 2760, "status": "ok", "warnings": []}` |
| 62 | development | candidate | rfm | outer:2010-12-09 | `{"config": {}, "inner_average_precision": 0.5935314881849014, "validation_rows": 3337}` |
| 63 | development | calibration | rfm | outer:2010-12-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "platt"}` |
| 64 | development | fit | rfm | outer:2010-12-09 | `{"config": {}, "rows": 12281, "status": "ok", "warnings": []}` |
| 65 | development | outer_result | rfm | 2010-12-09 | `{"average_precision": 0.85725742099891, "calibration": "platt", "config": {}, "contacts": 996, "cutoff": "2010-12-09", "profit": 12692.3235}` |
| 66 | development | fit | bgnbd | inner:2010-09-09 | `{"config": {}, "rows": 2760, "status": "ok", "warnings": []}` |
| 67 | development | candidate | bgnbd | outer:2010-12-09 | `{"config": {}, "inner_average_precision": 0.5972995504976343, "validation_rows": 3337}` |
| 68 | development | calibration | bgnbd | outer:2010-12-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "platt"}` |
| 69 | development | fit | bgnbd | outer:2010-12-09 | `{"config": {}, "rows": 12281, "status": "ok", "warnings": []}` |
| 70 | development | outer_result | bgnbd | 2010-12-09 | `{"average_precision": 0.865885541114328, "calibration": "platt", "config": {}, "contacts": 1275, "cutoff": "2010-12-09", "profit": 14803.00473}` |
| 71 | development | fit | constant | inner:2010-09-09 | `{"config": {}, "rows": 2760, "status": "ok", "warnings": []}` |
| 72 | development | candidate | constant | outer:2010-12-09 | `{"config": {}, "inner_average_precision": 0.42163620017980225, "validation_rows": 3337}` |
| 73 | development | calibration | constant | outer:2010-12-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "native"}` |
| 74 | development | fit | constant | outer:2010-12-09 | `{"config": {}, "rows": 12281, "status": "ok", "warnings": []}` |
| 75 | development | outer_result | constant | 2010-12-09 | `{"average_precision": 0.6862142350437456, "calibration": "native", "config": {}, "contacts": 1776, "cutoff": "2010-12-09", "profit": 15824.612429999997}` |
| 76 | development | fit | logistic | inner:2010-10-09 | `{"config": {"C": 0.01}, "rows": 5770, "status": "ok", "warnings": []}` |
| 77 | development | candidate | logistic | outer:2011-01-09 | `{"config": {"C": 0.01}, "inner_average_precision": 0.6471536131074669, "validation_rows": 6983}` |
| 78 | development | fit | logistic | inner:2010-10-09 | `{"config": {"C": 0.1}, "rows": 5770, "status": "ok", "warnings": []}` |
| 79 | development | candidate | logistic | outer:2011-01-09 | `{"config": {"C": 0.1}, "inner_average_precision": 0.6457114379872927, "validation_rows": 6983}` |
| 80 | development | fit | logistic | inner:2010-10-09 | `{"config": {"C": 1.0}, "rows": 5770, "status": "ok", "warnings": []}` |
| 81 | development | candidate | logistic | outer:2011-01-09 | `{"config": {"C": 1.0}, "inner_average_precision": 0.6390881281197254, "validation_rows": 6983}` |
| 82 | development | calibration | logistic | outer:2011-01-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "platt"}` |
| 83 | development | fit | logistic | outer:2011-01-09 | `{"config": {"C": 0.01}, "rows": 15927, "status": "ok", "warnings": []}` |
| 84 | development | outer_result | logistic | 2011-01-09 | `{"average_precision": 0.8417445795604719, "calibration": "platt", "config": {"C": 0.01}, "contacts": 1185, "cutoff": "2011-01-09", "profit": 10324.91703}` |
| 85 | development | fit | lightgbm | inner:2010-10-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 5770, "status": "ok", "warnings": []}` |
| 86 | development | candidate | lightgbm | outer:2011-01-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "inner_average_precision": 0.6349218444222838, "validation_rows": 6983}` |
| 87 | development | fit | lightgbm | inner:2010-10-09 | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "rows": 5770, "status": "ok", "warnings": []}` |
| 88 | development | candidate | lightgbm | outer:2011-01-09 | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "inner_average_precision": 0.6266011085645993, "validation_rows": 6983}` |
| 89 | development | fit | lightgbm | inner:2010-10-09 | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "rows": 5770, "status": "ok", "warnings": []}` |
| 90 | development | candidate | lightgbm | outer:2011-01-09 | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "inner_average_precision": 0.6257882280093297, "validation_rows": 6983}` |
| 91 | development | fit | lightgbm | inner:2010-10-09 | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "rows": 5770, "status": "ok", "warnings": []}` |
| 92 | development | candidate | lightgbm | outer:2011-01-09 | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "inner_average_precision": 0.6182779485431962, "validation_rows": 6983}` |
| 93 | development | calibration | lightgbm | outer:2011-01-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "platt"}` |
| 94 | development | fit | lightgbm | outer:2011-01-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 15927, "status": "ok", "warnings": []}` |
| 95 | development | outer_result | lightgbm | 2011-01-09 | `{"average_precision": 0.8474696487909654, "calibration": "platt", "config": {"min_child_samples": 50, "num_leaves": 7}, "contacts": 977, "cutoff": "2011-01-09", "profit": 9250.04333}` |
| 96 | development | fit | recency | inner:2010-10-09 | `{"config": {}, "rows": 5770, "status": "ok", "warnings": []}` |
| 97 | development | candidate | recency | outer:2011-01-09 | `{"config": {}, "inner_average_precision": 0.5962907077981499, "validation_rows": 6983}` |
| 98 | development | calibration | recency | outer:2011-01-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "platt"}` |
| 99 | development | threshold | recency | outer:2011-01-09 | `{"inner_profit": 1781.8337000000001, "k": 30}` |
| 100 | development | threshold | recency | outer:2011-01-09 | `{"inner_profit": 774.8391000000001, "k": 60}` |
| 101 | development | threshold | recency | outer:2011-01-09 | `{"inner_profit": 0.0, "k": 90}` |
| 102 | development | threshold | recency | outer:2011-01-09 | `{"inner_profit": 0.0, "k": 120}` |
| 103 | development | threshold | recency | outer:2011-01-09 | `{"inner_profit": 0.0, "k": 180}` |
| 104 | development | threshold | recency | outer:2011-01-09 | `{"inner_profit": 0.0, "k": 270}` |
| 105 | development | fit | recency | outer:2011-01-09 | `{"config": {}, "rows": 15927, "status": "ok", "warnings": []}` |
| 106 | development | outer_result | recency | 2011-01-09 | `{"average_precision": 0.7968760450460262, "calibration": "platt", "config": {}, "contacts": 885, "cutoff": "2011-01-09", "profit": 8181.4881}` |
| 107 | development | fit | rfm | inner:2010-10-09 | `{"config": {}, "rows": 5770, "status": "ok", "warnings": []}` |
| 108 | development | candidate | rfm | outer:2011-01-09 | `{"config": {}, "inner_average_precision": 0.6151499934128435, "validation_rows": 6983}` |
| 109 | development | calibration | rfm | outer:2011-01-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "platt"}` |
| 110 | development | fit | rfm | outer:2011-01-09 | `{"config": {}, "rows": 15927, "status": "ok", "warnings": []}` |
| 111 | development | outer_result | rfm | 2011-01-09 | `{"average_precision": 0.8266615064644243, "calibration": "platt", "config": {}, "contacts": 1117, "cutoff": "2011-01-09", "profit": 9521.77843}` |
| 112 | development | fit | bgnbd | inner:2010-10-09 | `{"config": {}, "rows": 5770, "status": "ok", "warnings": []}` |
| 113 | development | candidate | bgnbd | outer:2011-01-09 | `{"config": {}, "inner_average_precision": 0.63738550286256, "validation_rows": 6983}` |
| 114 | development | calibration | bgnbd | outer:2011-01-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "platt"}` |
| 115 | development | fit | bgnbd | outer:2011-01-09 | `{"config": {}, "rows": 15927, "status": "ok", "warnings": []}` |
| 116 | development | outer_result | bgnbd | 2011-01-09 | `{"average_precision": 0.8390338451431483, "calibration": "platt", "config": {}, "contacts": 1161, "cutoff": "2011-01-09", "profit": 10153.24713}` |
| 117 | development | fit | constant | inner:2010-10-09 | `{"config": {}, "rows": 5770, "status": "ok", "warnings": []}` |
| 118 | development | candidate | constant | outer:2011-01-09 | `{"config": {}, "inner_average_precision": 0.4433519282582873, "validation_rows": 6983}` |
| 119 | development | calibration | constant | outer:2011-01-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "native"}` |
| 120 | development | fit | constant | outer:2011-01-09 | `{"config": {}, "rows": 15927, "status": "ok", "warnings": []}` |
| 121 | development | outer_result | constant | 2011-01-09 | `{"average_precision": 0.6560570071258908, "calibration": "native", "config": {}, "contacts": 1485, "cutoff": "2011-01-09", "profit": 10105.241730000002}` |
| 122 | development | fit | logistic | inner:2010-11-09 | `{"config": {"C": 0.01}, "rows": 8944, "status": "ok", "warnings": []}` |
| 123 | development | candidate | logistic | outer:2011-02-09 | `{"config": {"C": 0.01}, "inner_average_precision": 0.6570513049781709, "validation_rows": 10979}` |
| 124 | development | fit | logistic | inner:2010-11-09 | `{"config": {"C": 0.1}, "rows": 8944, "status": "ok", "warnings": []}` |
| 125 | development | candidate | logistic | outer:2011-02-09 | `{"config": {"C": 0.1}, "inner_average_precision": 0.6562702088504762, "validation_rows": 10979}` |
| 126 | development | fit | logistic | inner:2010-11-09 | `{"config": {"C": 1.0}, "rows": 8944, "status": "ok", "warnings": []}` |
| 127 | development | candidate | logistic | outer:2011-02-09 | `{"config": {"C": 1.0}, "inner_average_precision": 0.6521201470657234, "validation_rows": 10979}` |
| 128 | development | calibration | logistic | outer:2011-02-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "platt"}` |
| 129 | development | fit | logistic | outer:2011-02-09 | `{"config": {"C": 0.01}, "rows": 19923, "status": "ok", "warnings": []}` |
| 130 | development | outer_result | logistic | 2011-02-09 | `{"average_precision": 0.8263197284938852, "calibration": "platt", "config": {"C": 0.01}, "contacts": 915, "cutoff": "2011-02-09", "profit": 4764.395399999999}` |
| 131 | development | fit | lightgbm | inner:2010-11-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 8944, "status": "ok", "warnings": []}` |
| 132 | development | candidate | lightgbm | outer:2011-02-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "inner_average_precision": 0.660588319311552, "validation_rows": 10979}` |
| 133 | development | fit | lightgbm | inner:2010-11-09 | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "rows": 8944, "status": "ok", "warnings": []}` |
| 134 | development | candidate | lightgbm | outer:2011-02-09 | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "inner_average_precision": 0.6545915055846655, "validation_rows": 10979}` |
| 135 | development | fit | lightgbm | inner:2010-11-09 | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "rows": 8944, "status": "ok", "warnings": []}` |
| 136 | development | candidate | lightgbm | outer:2011-02-09 | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "inner_average_precision": 0.6541743387706196, "validation_rows": 10979}` |
| 137 | development | fit | lightgbm | inner:2010-11-09 | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "rows": 8944, "status": "ok", "warnings": []}` |
| 138 | development | candidate | lightgbm | outer:2011-02-09 | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "inner_average_precision": 0.6492637100187924, "validation_rows": 10979}` |
| 139 | development | calibration | lightgbm | outer:2011-02-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "platt"}` |
| 140 | development | fit | lightgbm | outer:2011-02-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 19923, "status": "ok", "warnings": []}` |
| 141 | development | outer_result | lightgbm | 2011-02-09 | `{"average_precision": 0.8297397482587945, "calibration": "platt", "config": {"min_child_samples": 50, "num_leaves": 7}, "contacts": 889, "cutoff": "2011-02-09", "profit": 4938.1474}` |
| 142 | development | fit | recency | inner:2010-11-09 | `{"config": {}, "rows": 8944, "status": "ok", "warnings": []}` |
| 143 | development | candidate | recency | outer:2011-02-09 | `{"config": {}, "inner_average_precision": 0.6442339279355498, "validation_rows": 10979}` |
| 144 | development | calibration | recency | outer:2011-02-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "platt"}` |
| 145 | development | threshold | recency | outer:2011-02-09 | `{"inner_profit": 6065.057, "k": 30}` |
| 146 | development | threshold | recency | outer:2011-02-09 | `{"inner_profit": 1740.8096000000003, "k": 60}` |
| 147 | development | threshold | recency | outer:2011-02-09 | `{"inner_profit": 0.0, "k": 90}` |
| 148 | development | threshold | recency | outer:2011-02-09 | `{"inner_profit": 0.0, "k": 120}` |
| 149 | development | threshold | recency | outer:2011-02-09 | `{"inner_profit": 0.0, "k": 180}` |
| 150 | development | threshold | recency | outer:2011-02-09 | `{"inner_profit": 0.0, "k": 270}` |
| 151 | development | fit | recency | outer:2011-02-09 | `{"config": {}, "rows": 19923, "status": "ok", "warnings": []}` |
| 152 | development | outer_result | recency | 2011-02-09 | `{"average_precision": 0.7933623677339787, "calibration": "platt", "config": {}, "contacts": 589, "cutoff": "2011-02-09", "profit": 3478.4938}` |
| 153 | development | fit | rfm | inner:2010-11-09 | `{"config": {}, "rows": 8944, "status": "ok", "warnings": []}` |
| 154 | development | candidate | rfm | outer:2011-02-09 | `{"config": {}, "inner_average_precision": 0.649810940404078, "validation_rows": 10979}` |
| 155 | development | calibration | rfm | outer:2011-02-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "platt"}` |
| 156 | development | fit | rfm | outer:2011-02-09 | `{"config": {}, "rows": 19923, "status": "ok", "warnings": []}` |
| 157 | development | outer_result | rfm | 2011-02-09 | `{"average_precision": 0.8191876355321647, "calibration": "platt", "config": {}, "contacts": 978, "cutoff": "2011-02-09", "profit": 4902.1017}` |
| 158 | development | fit | bgnbd | inner:2010-11-09 | `{"config": {}, "rows": 8944, "status": "ok", "warnings": []}` |
| 159 | development | candidate | bgnbd | outer:2011-02-09 | `{"config": {}, "inner_average_precision": 0.6915826178570099, "validation_rows": 10979}` |
| 160 | development | calibration | bgnbd | outer:2011-02-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "platt"}` |
| 161 | development | fit | bgnbd | outer:2011-02-09 | `{"config": {}, "rows": 19923, "status": "ok", "warnings": []}` |
| 162 | development | outer_result | bgnbd | 2011-02-09 | `{"average_precision": 0.8244971441027397, "calibration": "platt", "config": {}, "contacts": 894, "cutoff": "2011-02-09", "profit": 5102.6949}` |
| 163 | development | fit | constant | inner:2010-11-09 | `{"config": {}, "rows": 8944, "status": "ok", "warnings": []}` |
| 164 | development | candidate | constant | outer:2011-02-09 | `{"config": {}, "inner_average_precision": 0.46813308790051245, "validation_rows": 10979}` |
| 165 | development | calibration | constant | outer:2011-02-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "native"}` |
| 166 | development | fit | constant | outer:2011-02-09 | `{"config": {}, "rows": 19923, "status": "ok", "warnings": []}` |
| 167 | development | outer_result | constant | 2011-02-09 | `{"average_precision": 0.6459905660377359, "calibration": "native", "config": {}, "contacts": 1171, "cutoff": "2011-02-09", "profit": 4671.7164999999995}` |
| 168 | development | fit | logistic | inner:2010-12-09 | `{"config": {"C": 0.01}, "rows": 12281, "status": "ok", "warnings": []}` |
| 169 | development | candidate | logistic | outer:2011-03-09 | `{"config": {"C": 0.01}, "inner_average_precision": 0.6785342602516634, "validation_rows": 15208}` |
| 170 | development | fit | logistic | inner:2010-12-09 | `{"config": {"C": 0.1}, "rows": 12281, "status": "ok", "warnings": []}` |
| 171 | development | candidate | logistic | outer:2011-03-09 | `{"config": {"C": 0.1}, "inner_average_precision": 0.678211703445116, "validation_rows": 15208}` |
| 172 | development | fit | logistic | inner:2010-12-09 | `{"config": {"C": 1.0}, "rows": 12281, "status": "ok", "warnings": []}` |
| 173 | development | candidate | logistic | outer:2011-03-09 | `{"config": {"C": 1.0}, "inner_average_precision": 0.6752578662598228, "validation_rows": 15208}` |
| 174 | development | calibration | logistic | outer:2011-03-09 | `{"candidates": [{"brier": 0.3597922029295785, "kind": "platt", "validation_rows": 4229}, {"brier": 0.35685649800352637, "kind": "isotonic", "validation_rows": 4229}], "selected": "isotonic"}` |
| 175 | development | fit | logistic | outer:2011-03-09 | `{"config": {"C": 0.01}, "rows": 24152, "status": "ok", "warnings": []}` |
| 176 | development | outer_result | logistic | 2011-03-09 | `{"average_precision": 0.8020431427360007, "calibration": "isotonic", "config": {"C": 0.01}, "contacts": 649, "cutoff": "2011-03-09", "profit": 1701.6574000000003}` |
| 177 | development | fit | lightgbm | inner:2010-12-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 12281, "status": "ok", "warnings": []}` |
| 178 | development | candidate | lightgbm | outer:2011-03-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "inner_average_precision": 0.6900686247932659, "validation_rows": 15208}` |
| 179 | development | fit | lightgbm | inner:2010-12-09 | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "rows": 12281, "status": "ok", "warnings": []}` |
| 180 | development | candidate | lightgbm | outer:2011-03-09 | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "inner_average_precision": 0.685990079782661, "validation_rows": 15208}` |
| 181 | development | fit | lightgbm | inner:2010-12-09 | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "rows": 12281, "status": "ok", "warnings": []}` |
| 182 | development | candidate | lightgbm | outer:2011-03-09 | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "inner_average_precision": 0.685784912345575, "validation_rows": 15208}` |
| 183 | development | fit | lightgbm | inner:2010-12-09 | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "rows": 12281, "status": "ok", "warnings": []}` |
| 184 | development | candidate | lightgbm | outer:2011-03-09 | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "inner_average_precision": 0.6833013196458448, "validation_rows": 15208}` |
| 185 | development | calibration | lightgbm | outer:2011-03-09 | `{"candidates": [{"brier": 0.30712681722584534, "kind": "platt", "validation_rows": 4229}, {"brier": 0.305855749745963, "kind": "isotonic", "validation_rows": 4229}], "selected": "isotonic"}` |
| 186 | development | fit | lightgbm | outer:2011-03-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 24152, "status": "ok", "warnings": []}` |
| 187 | development | outer_result | lightgbm | 2011-03-09 | `{"average_precision": 0.8045249560972629, "calibration": "isotonic", "config": {"min_child_samples": 50, "num_leaves": 7}, "contacts": 766, "cutoff": "2011-03-09", "profit": 1581.7306000000003}` |
| 188 | development | fit | recency | inner:2010-12-09 | `{"config": {}, "rows": 12281, "status": "ok", "warnings": []}` |
| 189 | development | candidate | recency | outer:2011-03-09 | `{"config": {}, "inner_average_precision": 0.693532957515105, "validation_rows": 15208}` |
| 190 | development | calibration | recency | outer:2011-03-09 | `{"candidates": [{"brier": 0.2751502363415978, "kind": "platt", "validation_rows": 4229}, {"brier": 0.2771676296475913, "kind": "isotonic", "validation_rows": 4229}], "selected": "platt"}` |
| 191 | development | threshold | recency | outer:2011-03-09 | `{"inner_profit": 12197.6149, "k": 30}` |
| 192 | development | threshold | recency | outer:2011-03-09 | `{"inner_profit": 4237.2462, "k": 60}` |
| 193 | development | threshold | recency | outer:2011-03-09 | `{"inner_profit": 0.0, "k": 90}` |
| 194 | development | threshold | recency | outer:2011-03-09 | `{"inner_profit": 0.0, "k": 120}` |
| 195 | development | threshold | recency | outer:2011-03-09 | `{"inner_profit": 0.0, "k": 180}` |
| 196 | development | threshold | recency | outer:2011-03-09 | `{"inner_profit": 0.0, "k": 270}` |
| 197 | development | fit | recency | outer:2011-03-09 | `{"config": {}, "rows": 24152, "status": "ok", "warnings": []}` |
| 198 | development | outer_result | recency | 2011-03-09 | `{"average_precision": 0.7882945286639689, "calibration": "platt", "config": {}, "contacts": 358, "cutoff": "2011-03-09", "profit": 731.5081}` |
| 199 | development | fit | rfm | inner:2010-12-09 | `{"config": {}, "rows": 12281, "status": "ok", "warnings": []}` |
| 200 | development | candidate | rfm | outer:2011-03-09 | `{"config": {}, "inner_average_precision": 0.6883986416826839, "validation_rows": 15208}` |
| 201 | development | calibration | rfm | outer:2011-03-09 | `{"candidates": [{"brier": 0.2800506990740386, "kind": "platt", "validation_rows": 4229}, {"brier": 0.28090409933395233, "kind": "isotonic", "validation_rows": 4229}], "selected": "platt"}` |
| 202 | development | fit | rfm | outer:2011-03-09 | `{"config": {}, "rows": 24152, "status": "ok", "warnings": []}` |
| 203 | development | outer_result | rfm | 2011-03-09 | `{"average_precision": 0.8124223702883812, "calibration": "platt", "config": {}, "contacts": 849, "cutoff": "2011-03-09", "profit": 1182.3906000000002}` |
| 204 | development | fit | bgnbd | inner:2010-12-09 | `{"config": {}, "rows": 12281, "status": "ok", "warnings": []}` |
| 205 | development | candidate | bgnbd | outer:2011-03-09 | `{"config": {}, "inner_average_precision": 0.7422627481029658, "validation_rows": 15208}` |
| 206 | development | calibration | bgnbd | outer:2011-03-09 | `{"candidates": [{"brier": 0.24007987572603295, "kind": "platt", "validation_rows": 4229}, {"brier": 0.23920492052113249, "kind": "isotonic", "validation_rows": 4229}], "selected": "isotonic"}` |
| 207 | development | fit | bgnbd | outer:2011-03-09 | `{"config": {}, "rows": 24152, "status": "ok", "warnings": []}` |
| 208 | development | outer_result | bgnbd | 2011-03-09 | `{"average_precision": 0.8162815766950197, "calibration": "isotonic", "config": {}, "contacts": 638, "cutoff": "2011-03-09", "profit": 1806.2720000000002}` |
| 209 | development | fit | constant | inner:2010-12-09 | `{"config": {}, "rows": 12281, "status": "ok", "warnings": []}` |
| 210 | development | candidate | constant | outer:2011-03-09 | `{"config": {}, "inner_average_precision": 0.49762818658781804, "validation_rows": 15208}` |
| 211 | development | calibration | constant | outer:2011-03-09 | `{"candidates": [{"brier": 0.2845349861977539, "kind": "platt", "validation_rows": 4229}, {"brier": 0.2853257951995387, "kind": "isotonic", "validation_rows": 4229}], "selected": "native"}` |
| 212 | development | fit | constant | outer:2011-03-09 | `{"config": {}, "rows": 24152, "status": "ok", "warnings": []}` |
| 213 | development | outer_result | constant | 2011-03-09 | `{"average_precision": 0.6331305568554048, "calibration": "native", "config": {}, "contacts": 917, "cutoff": "2011-03-09", "profit": 979.5968000000003}` |
| 214 | development | fit | logistic | inner:2011-01-09 | `{"config": {"C": 0.01}, "rows": 15927, "status": "ok", "warnings": []}` |
| 215 | development | candidate | logistic | outer:2011-04-09 | `{"config": {"C": 0.01}, "inner_average_precision": 0.730335701072681, "validation_rows": 19418}` |
| 216 | development | fit | logistic | inner:2011-01-09 | `{"config": {"C": 0.1}, "rows": 15927, "status": "ok", "warnings": []}` |
| 217 | development | candidate | logistic | outer:2011-04-09 | `{"config": {"C": 0.1}, "inner_average_precision": 0.7296195448708759, "validation_rows": 19418}` |
| 218 | development | fit | logistic | inner:2011-01-09 | `{"config": {"C": 1.0}, "rows": 15927, "status": "ok", "warnings": []}` |
| 219 | development | candidate | logistic | outer:2011-04-09 | `{"config": {"C": 1.0}, "inner_average_precision": 0.7261767501509875, "validation_rows": 19418}` |
| 220 | development | calibration | logistic | outer:2011-04-09 | `{"candidates": [{"brier": 0.285579239238499, "kind": "platt", "validation_rows": 8439}, {"brier": 0.28194172079878255, "kind": "isotonic", "validation_rows": 8439}], "selected": "isotonic"}` |
| 221 | development | fit | logistic | outer:2011-04-09 | `{"config": {"C": 0.01}, "rows": 28362, "status": "ok", "warnings": []}` |
| 222 | development | outer_result | logistic | 2011-04-09 | `{"average_precision": 0.8011253057411712, "calibration": "isotonic", "config": {"C": 0.01}, "contacts": 1260, "cutoff": "2011-04-09", "profit": 2223.8409}` |
| 223 | development | fit | lightgbm | inner:2011-01-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 15927, "status": "ok", "warnings": []}` |
| 224 | development | candidate | lightgbm | outer:2011-04-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "inner_average_precision": 0.721792294803943, "validation_rows": 19418}` |
| 225 | development | fit | lightgbm | inner:2011-01-09 | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "rows": 15927, "status": "ok", "warnings": []}` |
| 226 | development | candidate | lightgbm | outer:2011-04-09 | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "inner_average_precision": 0.71739692100277, "validation_rows": 19418}` |
| 227 | development | fit | lightgbm | inner:2011-01-09 | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "rows": 15927, "status": "ok", "warnings": []}` |
| 228 | development | candidate | lightgbm | outer:2011-04-09 | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "inner_average_precision": 0.7179249851855412, "validation_rows": 19418}` |
| 229 | development | fit | lightgbm | inner:2011-01-09 | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "rows": 15927, "status": "ok", "warnings": []}` |
| 230 | development | candidate | lightgbm | outer:2011-04-09 | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "inner_average_precision": 0.7160260902465194, "validation_rows": 19418}` |
| 231 | development | calibration | lightgbm | outer:2011-04-09 | `{"candidates": [{"brier": 0.2709257883724041, "kind": "platt", "validation_rows": 8439}, {"brier": 0.26750124918137236, "kind": "isotonic", "validation_rows": 8439}], "selected": "isotonic"}` |
| 232 | development | fit | lightgbm | outer:2011-04-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 28362, "status": "ok", "warnings": []}` |
| 233 | development | outer_result | lightgbm | 2011-04-09 | `{"average_precision": 0.8019440893635457, "calibration": "isotonic", "config": {"min_child_samples": 50, "num_leaves": 7}, "contacts": 1144, "cutoff": "2011-04-09", "profit": 2446.0588}` |
| 234 | development | fit | recency | inner:2011-01-09 | `{"config": {}, "rows": 15927, "status": "ok", "warnings": []}` |
| 235 | development | candidate | recency | outer:2011-04-09 | `{"config": {}, "inner_average_precision": 0.7188389103654703, "validation_rows": 19418}` |
| 236 | development | calibration | recency | outer:2011-04-09 | `{"candidates": [{"brier": 0.25707005746939887, "kind": "platt", "validation_rows": 8439}, {"brier": 0.2583466373007372, "kind": "isotonic", "validation_rows": 8439}], "selected": "platt"}` |
| 237 | development | threshold | recency | outer:2011-04-09 | `{"inner_profit": 20379.103000000003, "k": 30}` |
| 238 | development | threshold | recency | outer:2011-04-09 | `{"inner_profit": 7049.6219, "k": 60}` |
| 239 | development | threshold | recency | outer:2011-04-09 | `{"inner_profit": 0.0, "k": 90}` |
| 240 | development | threshold | recency | outer:2011-04-09 | `{"inner_profit": 0.0, "k": 120}` |
| 241 | development | threshold | recency | outer:2011-04-09 | `{"inner_profit": 0.0, "k": 180}` |
| 242 | development | threshold | recency | outer:2011-04-09 | `{"inner_profit": 0.0, "k": 270}` |
| 243 | development | fit | recency | outer:2011-04-09 | `{"config": {}, "rows": 28362, "status": "ok", "warnings": []}` |
| 244 | development | outer_result | recency | 2011-04-09 | `{"average_precision": 0.7991490168532158, "calibration": "platt", "config": {}, "contacts": 428, "cutoff": "2011-04-09", "profit": 1198.0493000000001}` |
| 245 | development | fit | rfm | inner:2011-01-09 | `{"config": {}, "rows": 15927, "status": "ok", "warnings": []}` |
| 246 | development | candidate | rfm | outer:2011-04-09 | `{"config": {}, "inner_average_precision": 0.7116320605672144, "validation_rows": 19418}` |
| 247 | development | calibration | rfm | outer:2011-04-09 | `{"candidates": [{"brier": 0.2584042204129285, "kind": "platt", "validation_rows": 8439}, {"brier": 0.25884295164787335, "kind": "isotonic", "validation_rows": 8439}], "selected": "platt"}` |
| 248 | development | fit | rfm | outer:2011-04-09 | `{"config": {}, "rows": 28362, "status": "ok", "warnings": []}` |
| 249 | development | outer_result | rfm | 2011-04-09 | `{"average_precision": 0.8168561340868136, "calibration": "platt", "config": {}, "contacts": 1098, "cutoff": "2011-04-09", "profit": 2478.0711}` |
| 250 | development | fit | bgnbd | inner:2011-01-09 | `{"config": {}, "rows": 15927, "status": "ok", "warnings": []}` |
| 251 | development | candidate | bgnbd | outer:2011-04-09 | `{"config": {}, "inner_average_precision": 0.7645182376892298, "validation_rows": 19418}` |
| 252 | development | calibration | bgnbd | outer:2011-04-09 | `{"candidates": [{"brier": 0.22606415045587988, "kind": "platt", "validation_rows": 8439}, {"brier": 0.22585170649702088, "kind": "isotonic", "validation_rows": 8439}], "selected": "isotonic"}` |
| 253 | development | fit | bgnbd | outer:2011-04-09 | `{"config": {}, "rows": 28362, "status": "ok", "warnings": []}` |
| 254 | development | outer_result | bgnbd | 2011-04-09 | `{"average_precision": 0.825738040941689, "calibration": "isotonic", "config": {}, "contacts": 867, "cutoff": "2011-04-09", "profit": 3142.4298}` |
| 255 | development | fit | constant | inner:2011-01-09 | `{"config": {}, "rows": 15927, "status": "ok", "warnings": []}` |
| 256 | development | candidate | constant | outer:2011-04-09 | `{"config": {}, "inner_average_precision": 0.515134481222407, "validation_rows": 19418}` |
| 257 | development | calibration | constant | outer:2011-04-09 | `{"candidates": [{"brier": 0.26341095808437404, "kind": "platt", "validation_rows": 8439}, {"brier": 0.2746781397064018, "kind": "isotonic", "validation_rows": 8439}], "selected": "native"}` |
| 258 | development | fit | constant | outer:2011-04-09 | `{"config": {}, "rows": 28362, "status": "ok", "warnings": []}` |
| 259 | development | outer_result | constant | 2011-04-09 | `{"average_precision": 0.625086625086625, "calibration": "native", "config": {}, "contacts": 1133, "cutoff": "2011-04-09", "profit": 2114.9552000000003}` |
| 260 | development | candidate | logistic | outer:2011-05-09 | `{"config": {"C": 0.01}, "inner_average_precision": 0.730335701072681, "validation_rows": 19418}` |
| 261 | development | candidate | logistic | outer:2011-05-09 | `{"config": {"C": 0.1}, "inner_average_precision": 0.7296195448708759, "validation_rows": 19418}` |
| 262 | development | candidate | logistic | outer:2011-05-09 | `{"config": {"C": 1.0}, "inner_average_precision": 0.7261767501509875, "validation_rows": 19418}` |
| 263 | development | calibration | logistic | outer:2011-05-09 | `{"candidates": [{"brier": 0.285579239238499, "kind": "platt", "validation_rows": 8439}, {"brier": 0.28194172079878255, "kind": "isotonic", "validation_rows": 8439}], "selected": "isotonic"}` |
| 264 | development | fit | logistic | outer:2011-05-09 | `{"config": {"C": 0.01}, "rows": 28362, "status": "ok", "warnings": []}` |
| 265 | development | outer_result | logistic | 2011-05-09 | `{"average_precision": 0.7984072105793523, "calibration": "isotonic", "config": {"C": 0.01}, "contacts": 1319, "cutoff": "2011-05-09", "profit": 948.0938300000001}` |
| 266 | development | candidate | lightgbm | outer:2011-05-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "inner_average_precision": 0.721792294803943, "validation_rows": 19418}` |
| 267 | development | candidate | lightgbm | outer:2011-05-09 | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "inner_average_precision": 0.71739692100277, "validation_rows": 19418}` |
| 268 | development | candidate | lightgbm | outer:2011-05-09 | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "inner_average_precision": 0.7179249851855412, "validation_rows": 19418}` |
| 269 | development | candidate | lightgbm | outer:2011-05-09 | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "inner_average_precision": 0.7160260902465194, "validation_rows": 19418}` |
| 270 | development | calibration | lightgbm | outer:2011-05-09 | `{"candidates": [{"brier": 0.2709257883724041, "kind": "platt", "validation_rows": 8439}, {"brier": 0.26750124918137236, "kind": "isotonic", "validation_rows": 8439}], "selected": "isotonic"}` |
| 271 | development | fit | lightgbm | outer:2011-05-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 28362, "status": "ok", "warnings": []}` |
| 272 | development | outer_result | lightgbm | 2011-05-09 | `{"average_precision": 0.8067727055280492, "calibration": "isotonic", "config": {"min_child_samples": 50, "num_leaves": 7}, "contacts": 1198, "cutoff": "2011-05-09", "profit": 1152.6790300000002}` |
| 273 | development | candidate | recency | outer:2011-05-09 | `{"config": {}, "inner_average_precision": 0.7188389103654703, "validation_rows": 19418}` |
| 274 | development | calibration | recency | outer:2011-05-09 | `{"candidates": [{"brier": 0.25707005746939887, "kind": "platt", "validation_rows": 8439}, {"brier": 0.2583466373007372, "kind": "isotonic", "validation_rows": 8439}], "selected": "platt"}` |
| 275 | development | threshold | recency | outer:2011-05-09 | `{"inner_profit": 20379.103000000003, "k": 30}` |
| 276 | development | threshold | recency | outer:2011-05-09 | `{"inner_profit": 7049.6219, "k": 60}` |
| 277 | development | threshold | recency | outer:2011-05-09 | `{"inner_profit": 0.0, "k": 90}` |
| 278 | development | threshold | recency | outer:2011-05-09 | `{"inner_profit": 0.0, "k": 120}` |
| 279 | development | threshold | recency | outer:2011-05-09 | `{"inner_profit": 0.0, "k": 180}` |
| 280 | development | threshold | recency | outer:2011-05-09 | `{"inner_profit": 0.0, "k": 270}` |
| 281 | development | fit | recency | outer:2011-05-09 | `{"config": {}, "rows": 28362, "status": "ok", "warnings": []}` |
| 282 | development | outer_result | recency | 2011-05-09 | `{"average_precision": 0.792373739336678, "calibration": "platt", "config": {}, "contacts": 532, "cutoff": "2011-05-09", "profit": 985.4617000000002}` |
| 283 | development | candidate | rfm | outer:2011-05-09 | `{"config": {}, "inner_average_precision": 0.7116320605672144, "validation_rows": 19418}` |
| 284 | development | calibration | rfm | outer:2011-05-09 | `{"candidates": [{"brier": 0.2584042204129285, "kind": "platt", "validation_rows": 8439}, {"brier": 0.25884295164787335, "kind": "isotonic", "validation_rows": 8439}], "selected": "platt"}` |
| 285 | development | fit | rfm | outer:2011-05-09 | `{"config": {}, "rows": 28362, "status": "ok", "warnings": []}` |
| 286 | development | outer_result | rfm | 2011-05-09 | `{"average_precision": 0.8169994339339776, "calibration": "platt", "config": {}, "contacts": 1135, "cutoff": "2011-05-09", "profit": 1120.83913}` |
| 287 | development | candidate | bgnbd | outer:2011-05-09 | `{"config": {}, "inner_average_precision": 0.7645182376892298, "validation_rows": 19418}` |
| 288 | development | calibration | bgnbd | outer:2011-05-09 | `{"candidates": [{"brier": 0.22606415045587988, "kind": "platt", "validation_rows": 8439}, {"brier": 0.22585170649702088, "kind": "isotonic", "validation_rows": 8439}], "selected": "isotonic"}` |
| 289 | development | fit | bgnbd | outer:2011-05-09 | `{"config": {}, "rows": 28362, "status": "ok", "warnings": []}` |
| 290 | development | outer_result | bgnbd | 2011-05-09 | `{"average_precision": 0.8273170240971497, "calibration": "isotonic", "config": {}, "contacts": 913, "cutoff": "2011-05-09", "profit": 1955.8540300000004}` |
| 291 | development | candidate | constant | outer:2011-05-09 | `{"config": {}, "inner_average_precision": 0.515134481222407, "validation_rows": 19418}` |
| 292 | development | calibration | constant | outer:2011-05-09 | `{"candidates": [{"brier": 0.26341095808437404, "kind": "platt", "validation_rows": 8439}, {"brier": 0.2746781397064018, "kind": "isotonic", "validation_rows": 8439}], "selected": "native"}` |
| 293 | development | fit | constant | outer:2011-05-09 | `{"config": {}, "rows": 28362, "status": "ok", "warnings": []}` |
| 294 | development | outer_result | constant | 2011-05-09 | `{"average_precision": 0.6188164586222838, "calibration": "native", "config": {}, "contacts": 1167, "cutoff": "2011-05-09", "profit": 766.9128300000002}` |
| 295 | development | fit | logistic | inner:2011-02-09 | `{"config": {"C": 0.01}, "rows": 19923, "status": "ok", "warnings": []}` |
| 296 | development | fit | logistic | inner:2011-03-09 | `{"config": {"C": 0.01}, "rows": 24152, "status": "ok", "warnings": []}` |
| 297 | development | candidate | logistic | outer:2011-06-09 | `{"config": {"C": 0.01}, "inner_average_precision": 0.7471827076554318, "validation_rows": 27932}` |
| 298 | development | fit | logistic | inner:2011-02-09 | `{"config": {"C": 0.1}, "rows": 19923, "status": "ok", "warnings": []}` |
| 299 | development | fit | logistic | inner:2011-03-09 | `{"config": {"C": 0.1}, "rows": 24152, "status": "ok", "warnings": []}` |
| 300 | development | candidate | logistic | outer:2011-06-09 | `{"config": {"C": 0.1}, "inner_average_precision": 0.7463261097905717, "validation_rows": 27932}` |
| 301 | development | fit | logistic | inner:2011-02-09 | `{"config": {"C": 1.0}, "rows": 19923, "status": "ok", "warnings": []}` |
| 302 | development | fit | logistic | inner:2011-03-09 | `{"config": {"C": 1.0}, "rows": 24152, "status": "ok", "warnings": []}` |
| 303 | development | candidate | logistic | outer:2011-06-09 | `{"config": {"C": 1.0}, "inner_average_precision": 0.744160107102684, "validation_rows": 27932}` |
| 304 | development | calibration | logistic | outer:2011-06-09 | `{"candidates": [{"brier": 0.24826348271861712, "kind": "platt", "validation_rows": 16953}, {"brier": 0.24041703645468734, "kind": "isotonic", "validation_rows": 16953}], "selected": "isotonic"}` |
| 305 | development | fit | logistic | outer:2011-06-09 | `{"config": {"C": 0.01}, "rows": 36876, "status": "ok", "warnings": []}` |
| 306 | development | outer_result | logistic | 2011-06-09 | `{"average_precision": 0.8323561351052398, "calibration": "isotonic", "config": {"C": 0.01}, "contacts": 1435, "cutoff": "2011-06-09", "profit": 2452.7269300000003}` |
| 307 | development | fit | lightgbm | inner:2011-02-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 19923, "status": "ok", "warnings": []}` |
| 308 | development | fit | lightgbm | inner:2011-03-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 24152, "status": "ok", "warnings": []}` |
| 309 | development | candidate | lightgbm | outer:2011-06-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "inner_average_precision": 0.7503934024490595, "validation_rows": 27932}` |
| 310 | development | fit | lightgbm | inner:2011-02-09 | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "rows": 19923, "status": "ok", "warnings": []}` |
| 311 | development | fit | lightgbm | inner:2011-03-09 | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "rows": 24152, "status": "ok", "warnings": []}` |
| 312 | development | candidate | lightgbm | outer:2011-06-09 | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "inner_average_precision": 0.7469833036428498, "validation_rows": 27932}` |
| 313 | development | fit | lightgbm | inner:2011-02-09 | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "rows": 19923, "status": "ok", "warnings": []}` |
| 314 | development | fit | lightgbm | inner:2011-03-09 | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "rows": 24152, "status": "ok", "warnings": []}` |
| 315 | development | candidate | lightgbm | outer:2011-06-09 | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "inner_average_precision": 0.7478421001764746, "validation_rows": 27932}` |
| 316 | development | fit | lightgbm | inner:2011-02-09 | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "rows": 19923, "status": "ok", "warnings": []}` |
| 317 | development | fit | lightgbm | inner:2011-03-09 | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "rows": 24152, "status": "ok", "warnings": []}` |
| 318 | development | candidate | lightgbm | outer:2011-06-09 | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "inner_average_precision": 0.7445722911962787, "validation_rows": 27932}` |
| 319 | development | calibration | lightgbm | outer:2011-06-09 | `{"candidates": [{"brier": 0.2339413997042182, "kind": "platt", "validation_rows": 16953}, {"brier": 0.22957400541598677, "kind": "isotonic", "validation_rows": 16953}], "selected": "isotonic"}` |
| 320 | development | fit | lightgbm | outer:2011-06-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 36876, "status": "ok", "warnings": []}` |
| 321 | development | outer_result | lightgbm | 2011-06-09 | `{"average_precision": 0.8349384219013971, "calibration": "isotonic", "config": {"min_child_samples": 50, "num_leaves": 7}, "contacts": 1266, "cutoff": "2011-06-09", "profit": 2776.9287300000005}` |
| 322 | development | fit | recency | inner:2011-02-09 | `{"config": {}, "rows": 19923, "status": "ok", "warnings": []}` |
| 323 | development | fit | recency | inner:2011-03-09 | `{"config": {}, "rows": 24152, "status": "ok", "warnings": []}` |
| 324 | development | candidate | recency | outer:2011-06-09 | `{"config": {}, "inner_average_precision": 0.7445862946478892, "validation_rows": 27932}` |
| 325 | development | calibration | recency | outer:2011-06-09 | `{"candidates": [{"brier": 0.2342917080709602, "kind": "platt", "validation_rows": 16953}, {"brier": 0.23482076870946722, "kind": "isotonic", "validation_rows": 16953}], "selected": "platt"}` |
| 326 | development | threshold | recency | outer:2011-06-09 | `{"inner_profit": 24589.104900000002, "k": 30}` |
| 327 | development | threshold | recency | outer:2011-06-09 | `{"inner_profit": 9990.698199999999, "k": 60}` |
| 328 | development | threshold | recency | outer:2011-06-09 | `{"inner_profit": 0.0, "k": 90}` |
| 329 | development | threshold | recency | outer:2011-06-09 | `{"inner_profit": 0.0, "k": 120}` |
| 330 | development | threshold | recency | outer:2011-06-09 | `{"inner_profit": 0.0, "k": 180}` |
| 331 | development | threshold | recency | outer:2011-06-09 | `{"inner_profit": 0.0, "k": 270}` |
| 332 | development | fit | recency | outer:2011-06-09 | `{"config": {}, "rows": 36876, "status": "ok", "warnings": []}` |
| 333 | development | outer_result | recency | 2011-06-09 | `{"average_precision": 0.8234406808297253, "calibration": "platt", "config": {}, "contacts": 436, "cutoff": "2011-06-09", "profit": 1228.9219300000002}` |
| 334 | development | fit | rfm | inner:2011-02-09 | `{"config": {}, "rows": 19923, "status": "ok", "warnings": []}` |
| 335 | development | fit | rfm | inner:2011-03-09 | `{"config": {}, "rows": 24152, "status": "ok", "warnings": []}` |
| 336 | development | candidate | rfm | outer:2011-06-09 | `{"config": {}, "inner_average_precision": 0.7440790516539508, "validation_rows": 27932}` |
| 337 | development | calibration | rfm | outer:2011-06-09 | `{"candidates": [{"brier": 0.22608390820236854, "kind": "platt", "validation_rows": 16953}, {"brier": 0.22500238585416157, "kind": "isotonic", "validation_rows": 16953}], "selected": "isotonic"}` |
| 338 | development | fit | rfm | outer:2011-06-09 | `{"config": {}, "rows": 36876, "status": "ok", "warnings": []}` |
| 339 | development | outer_result | rfm | 2011-06-09 | `{"average_precision": 0.7943504713943681, "calibration": "isotonic", "config": {}, "contacts": 1289, "cutoff": "2011-06-09", "profit": 2479.5419300000003}` |
| 340 | development | fit | bgnbd | inner:2011-02-09 | `{"config": {}, "rows": 19923, "status": "ok", "warnings": []}` |
| 341 | development | fit | bgnbd | inner:2011-03-09 | `{"config": {}, "rows": 24152, "status": "ok", "warnings": []}` |
| 342 | development | candidate | bgnbd | outer:2011-06-09 | `{"config": {}, "inner_average_precision": 0.7820591658788403, "validation_rows": 27932}` |
| 343 | development | calibration | bgnbd | outer:2011-06-09 | `{"candidates": [{"brier": 0.20777821436919117, "kind": "platt", "validation_rows": 16953}, {"brier": 0.20804725040947786, "kind": "isotonic", "validation_rows": 16953}], "selected": "platt"}` |
| 344 | development | fit | bgnbd | outer:2011-06-09 | `{"config": {}, "rows": 36876, "status": "ok", "warnings": []}` |
| 345 | development | outer_result | bgnbd | 2011-06-09 | `{"average_precision": 0.8613987170169768, "calibration": "platt", "config": {}, "contacts": 1090, "cutoff": "2011-06-09", "profit": 3067.9063300000003}` |
| 346 | development | fit | constant | inner:2011-02-09 | `{"config": {}, "rows": 19923, "status": "ok", "warnings": []}` |
| 347 | development | fit | constant | inner:2011-03-09 | `{"config": {}, "rows": 24152, "status": "ok", "warnings": []}` |
| 348 | development | candidate | constant | outer:2011-06-09 | `{"config": {}, "inner_average_precision": 0.5760029262505056, "validation_rows": 27932}` |
| 349 | development | calibration | constant | outer:2011-06-09 | `{"candidates": [{"brier": 0.2673956809088496, "kind": "platt", "validation_rows": 16953}, {"brier": 0.2592114984485752, "kind": "isotonic", "validation_rows": 16953}], "selected": "native"}` |
| 350 | development | fit | constant | outer:2011-06-09 | `{"config": {}, "rows": 36876, "status": "ok", "warnings": []}` |
| 351 | development | outer_result | constant | 2011-06-09 | `{"average_precision": 0.6392873669597409, "calibration": "native", "config": {}, "contacts": 1297, "cutoff": "2011-06-09", "profit": 2368.03363}` |
| 352 | placebo | candidate | lightgbm | outer:2010-11-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "inner_average_precision": null, "validation_rows": 0}` |
| 353 | placebo | calibration | lightgbm | outer:2010-11-09 | `{"candidates": [{"reason": "no forward predictions"}], "selected": "native"}` |
| 354 | placebo | fit | lightgbm | outer:2010-11-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 8944, "status": "ok", "warnings": []}` |
| 355 | placebo | outer_result | lightgbm | 2010-11-09 | `{"average_precision": 0.5655927787819676, "calibration": "native", "config": {"min_child_samples": 50, "num_leaves": 7}, "contacts": 1604, "cutoff": "2010-11-09", "profit": 26420.23673}` |
| 356 | placebo | candidate | constant | outer:2010-11-09 | `{"config": {}, "inner_average_precision": null, "validation_rows": 0}` |
| 357 | placebo | calibration | constant | outer:2010-11-09 | `{"candidates": [{"reason": "no forward predictions"}], "selected": "native"}` |
| 358 | placebo | fit | constant | outer:2010-11-09 | `{"config": {}, "rows": 8944, "status": "ok", "warnings": []}` |
| 359 | placebo | outer_result | constant | 2010-11-09 | `{"average_precision": 0.5768268268268268, "calibration": "native", "config": {}, "contacts": 1583, "cutoff": "2010-11-09", "profit": 26480.90483}` |
| 360 | placebo | fit | lightgbm | inner:2010-09-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 2760, "status": "ok", "warnings": []}` |
| 361 | placebo | candidate | lightgbm | outer:2010-12-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "inner_average_precision": 0.4190079852089116, "validation_rows": 3337}` |
| 362 | placebo | calibration | lightgbm | outer:2010-12-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "platt"}` |
| 363 | placebo | fit | lightgbm | outer:2010-12-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 12281, "status": "ok", "warnings": []}` |
| 364 | placebo | outer_result | lightgbm | 2010-12-09 | `{"average_precision": 0.6810224491977386, "calibration": "platt", "config": {"min_child_samples": 50, "num_leaves": 7}, "contacts": 1681, "cutoff": "2010-12-09", "profit": 44713.59496}` |
| 365 | placebo | fit | constant | inner:2010-09-09 | `{"config": {}, "rows": 2760, "status": "ok", "warnings": []}` |
| 366 | placebo | candidate | constant | outer:2010-12-09 | `{"config": {}, "inner_average_precision": 0.42163620017980225, "validation_rows": 3337}` |
| 367 | placebo | calibration | constant | outer:2010-12-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "native"}` |
| 368 | placebo | fit | constant | outer:2010-12-09 | `{"config": {}, "rows": 12281, "status": "ok", "warnings": []}` |
| 369 | placebo | outer_result | constant | 2010-12-09 | `{"average_precision": 0.6862142350437456, "calibration": "native", "config": {}, "contacts": 1776, "cutoff": "2010-12-09", "profit": 44966.170260000006}` |
| 370 | placebo | fit | lightgbm | inner:2010-10-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 5770, "status": "ok", "warnings": []}` |
| 371 | placebo | candidate | lightgbm | outer:2011-01-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "inner_average_precision": 0.44774669411740203, "validation_rows": 6983}` |
| 372 | placebo | calibration | lightgbm | outer:2011-01-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "platt"}` |
| 373 | placebo | fit | lightgbm | outer:2011-01-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 15927, "status": "ok", "warnings": []}` |
| 374 | placebo | outer_result | lightgbm | 2011-01-09 | `{"average_precision": 0.6508458365734573, "calibration": "platt", "config": {"min_child_samples": 50, "num_leaves": 7}, "contacts": 1464, "cutoff": "2011-01-09", "profit": 36894.214830000004}` |
| 375 | placebo | fit | constant | inner:2010-10-09 | `{"config": {}, "rows": 5770, "status": "ok", "warnings": []}` |
| 376 | placebo | candidate | constant | outer:2011-01-09 | `{"config": {}, "inner_average_precision": 0.4433519282582873, "validation_rows": 6983}` |
| 377 | placebo | calibration | constant | outer:2011-01-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "native"}` |
| 378 | placebo | fit | constant | outer:2011-01-09 | `{"config": {}, "rows": 15927, "status": "ok", "warnings": []}` |
| 379 | placebo | outer_result | constant | 2011-01-09 | `{"average_precision": 0.6560570071258908, "calibration": "native", "config": {}, "contacts": 1485, "cutoff": "2011-01-09", "profit": 36938.66313}` |
| 380 | placebo | fit | lightgbm | inner:2010-11-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 8944, "status": "ok", "warnings": []}` |
| 381 | placebo | candidate | lightgbm | outer:2011-02-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "inner_average_precision": 0.48298671350561895, "validation_rows": 10979}` |
| 382 | placebo | calibration | lightgbm | outer:2011-02-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "platt"}` |
| 383 | placebo | fit | lightgbm | outer:2011-02-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 19923, "status": "ok", "warnings": []}` |
| 384 | placebo | outer_result | lightgbm | 2011-02-09 | `{"average_precision": 0.6556671675167712, "calibration": "platt", "config": {"min_child_samples": 50, "num_leaves": 7}, "contacts": 1203, "cutoff": "2011-02-09", "profit": 27591.672899999998}` |
| 385 | placebo | fit | constant | inner:2010-11-09 | `{"config": {}, "rows": 8944, "status": "ok", "warnings": []}` |
| 386 | placebo | candidate | constant | outer:2011-02-09 | `{"config": {}, "inner_average_precision": 0.46813308790051245, "validation_rows": 10979}` |
| 387 | placebo | calibration | constant | outer:2011-02-09 | `{"candidates": [{"brier": null, "kind": "platt", "validation_rows": 0}, {"brier": null, "kind": "isotonic", "validation_rows": 0}], "selected": "native"}` |
| 388 | placebo | fit | constant | outer:2011-02-09 | `{"config": {}, "rows": 19923, "status": "ok", "warnings": []}` |
| 389 | placebo | outer_result | constant | 2011-02-09 | `{"average_precision": 0.6459905660377359, "calibration": "native", "config": {}, "contacts": 1171, "cutoff": "2011-02-09", "profit": 27534.3784}` |
| 390 | placebo | fit | lightgbm | inner:2010-12-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 12281, "status": "ok", "warnings": []}` |
| 391 | placebo | candidate | lightgbm | outer:2011-03-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "inner_average_precision": 0.5092929734876672, "validation_rows": 15208}` |
| 392 | placebo | calibration | lightgbm | outer:2011-03-09 | `{"candidates": [{"brier": 0.2830006850052258, "kind": "platt", "validation_rows": 4229}, {"brier": 0.29508426843574725, "kind": "isotonic", "validation_rows": 4229}], "selected": "platt"}` |
| 393 | placebo | fit | lightgbm | outer:2011-03-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 24152, "status": "ok", "warnings": []}` |
| 394 | placebo | outer_result | lightgbm | 2011-03-09 | `{"average_precision": 0.6485680836303925, "calibration": "platt", "config": {"min_child_samples": 50, "num_leaves": 7}, "contacts": 960, "cutoff": "2011-03-09", "profit": 16632.4734}` |
| 395 | placebo | fit | constant | inner:2010-12-09 | `{"config": {}, "rows": 12281, "status": "ok", "warnings": []}` |
| 396 | placebo | candidate | constant | outer:2011-03-09 | `{"config": {}, "inner_average_precision": 0.49762818658781804, "validation_rows": 15208}` |
| 397 | placebo | calibration | constant | outer:2011-03-09 | `{"candidates": [{"brier": 0.2845349861977539, "kind": "platt", "validation_rows": 4229}, {"brier": 0.28532579519953866, "kind": "isotonic", "validation_rows": 4229}], "selected": "native"}` |
| 398 | placebo | fit | constant | outer:2011-03-09 | `{"config": {}, "rows": 24152, "status": "ok", "warnings": []}` |
| 399 | placebo | outer_result | constant | 2011-03-09 | `{"average_precision": 0.6331305568554048, "calibration": "native", "config": {}, "contacts": 917, "cutoff": "2011-03-09", "profit": 16563.539599999996}` |
| 400 | placebo | fit | lightgbm | inner:2011-01-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 15927, "status": "ok", "warnings": []}` |
| 401 | placebo | candidate | lightgbm | outer:2011-04-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "inner_average_precision": 0.5339531518913868, "validation_rows": 19418}` |
| 402 | placebo | calibration | lightgbm | outer:2011-04-09 | `{"candidates": [{"brier": 0.2726886975493961, "kind": "platt", "validation_rows": 8439}, {"brier": 0.27950472705584994, "kind": "isotonic", "validation_rows": 8439}], "selected": "platt"}` |
| 403 | placebo | fit | lightgbm | outer:2011-04-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 28362, "status": "ok", "warnings": []}` |
| 404 | placebo | outer_result | lightgbm | 2011-04-09 | `{"average_precision": 0.6321567567259173, "calibration": "platt", "config": {"min_child_samples": 50, "num_leaves": 7}, "contacts": 1164, "cutoff": "2011-04-09", "profit": 20109.0711}` |
| 405 | placebo | fit | constant | inner:2011-01-09 | `{"config": {}, "rows": 15927, "status": "ok", "warnings": []}` |
| 406 | placebo | candidate | constant | outer:2011-04-09 | `{"config": {}, "inner_average_precision": 0.515134481222407, "validation_rows": 19418}` |
| 407 | placebo | calibration | constant | outer:2011-04-09 | `{"candidates": [{"brier": 0.2634109580844706, "kind": "platt", "validation_rows": 8439}, {"brier": 0.2746781397064018, "kind": "isotonic", "validation_rows": 8439}], "selected": "native"}` |
| 408 | placebo | fit | constant | outer:2011-04-09 | `{"config": {}, "rows": 28362, "status": "ok", "warnings": []}` |
| 409 | placebo | outer_result | constant | 2011-04-09 | `{"average_precision": 0.625086625086625, "calibration": "native", "config": {}, "contacts": 1133, "cutoff": "2011-04-09", "profit": 20113.324699999997}` |
| 410 | placebo | candidate | lightgbm | outer:2011-05-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "inner_average_precision": 0.5339531518913868, "validation_rows": 19418}` |
| 411 | placebo | calibration | lightgbm | outer:2011-05-09 | `{"candidates": [{"brier": 0.2726886975493961, "kind": "platt", "validation_rows": 8439}, {"brier": 0.27950472705584994, "kind": "isotonic", "validation_rows": 8439}], "selected": "platt"}` |
| 412 | placebo | fit | lightgbm | outer:2011-05-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 28362, "status": "ok", "warnings": []}` |
| 413 | placebo | outer_result | lightgbm | 2011-05-09 | `{"average_precision": 0.6240445863127174, "calibration": "platt", "config": {"min_child_samples": 50, "num_leaves": 7}, "contacts": 1204, "cutoff": "2011-05-09", "profit": 16585.2304}` |
| 414 | placebo | candidate | constant | outer:2011-05-09 | `{"config": {}, "inner_average_precision": 0.515134481222407, "validation_rows": 19418}` |
| 415 | placebo | calibration | constant | outer:2011-05-09 | `{"candidates": [{"brier": 0.2634109580844706, "kind": "platt", "validation_rows": 8439}, {"brier": 0.2746781397064018, "kind": "isotonic", "validation_rows": 8439}], "selected": "native"}` |
| 416 | placebo | fit | constant | outer:2011-05-09 | `{"config": {}, "rows": 28362, "status": "ok", "warnings": []}` |
| 417 | placebo | outer_result | constant | 2011-05-09 | `{"average_precision": 0.6188164586222838, "calibration": "native", "config": {}, "contacts": 1167, "cutoff": "2011-05-09", "profit": 16547.954400000002}` |
| 418 | placebo | fit | lightgbm | inner:2011-02-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 19923, "status": "ok", "warnings": []}` |
| 419 | placebo | fit | lightgbm | inner:2011-03-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 24152, "status": "ok", "warnings": []}` |
| 420 | placebo | candidate | lightgbm | outer:2011-06-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "inner_average_precision": 0.5580119527948146, "validation_rows": 27932}` |
| 421 | placebo | calibration | lightgbm | outer:2011-06-09 | `{"candidates": [{"brier": 0.2579190835346234, "kind": "platt", "validation_rows": 16953}, {"brier": 0.26153349392799236, "kind": "isotonic", "validation_rows": 16953}], "selected": "platt"}` |
| 422 | placebo | fit | lightgbm | outer:2011-06-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 36876, "status": "ok", "warnings": []}` |
| 423 | placebo | outer_result | lightgbm | 2011-06-09 | `{"average_precision": 0.6435229106100682, "calibration": "platt", "config": {"min_child_samples": 50, "num_leaves": 7}, "contacts": 1315, "cutoff": "2011-06-09", "profit": 22294.3678}` |
| 424 | placebo | fit | constant | inner:2011-02-09 | `{"config": {}, "rows": 19923, "status": "ok", "warnings": []}` |
| 425 | placebo | fit | constant | inner:2011-03-09 | `{"config": {}, "rows": 24152, "status": "ok", "warnings": []}` |
| 426 | placebo | candidate | constant | outer:2011-06-09 | `{"config": {}, "inner_average_precision": 0.5760029262505056, "validation_rows": 27932}` |
| 427 | placebo | calibration | constant | outer:2011-06-09 | `{"candidates": [{"brier": 0.26739568090889776, "kind": "platt", "validation_rows": 16953}, {"brier": 0.2592114984485752, "kind": "isotonic", "validation_rows": 16953}], "selected": "native"}` |
| 428 | placebo | fit | constant | outer:2011-06-09 | `{"config": {}, "rows": 36876, "status": "ok", "warnings": []}` |
| 429 | placebo | outer_result | constant | 2011-06-09 | `{"average_precision": 0.6392873669597409, "calibration": "native", "config": {}, "contacts": 1297, "cutoff": "2011-06-09", "profit": 22349.539900000003}` |
| 430 | final_fit_before_unseal | fit | logistic | inner:2010-09-09 | `{"config": {"C": 0.01}, "rows": 2760, "status": "ok", "warnings": []}` |
| 431 | final_fit_before_unseal | fit | logistic | inner:2010-10-09 | `{"config": {"C": 0.01}, "rows": 5770, "status": "ok", "warnings": []}` |
| 432 | final_fit_before_unseal | fit | logistic | inner:2010-11-09 | `{"config": {"C": 0.01}, "rows": 8944, "status": "ok", "warnings": []}` |
| 433 | final_fit_before_unseal | fit | logistic | inner:2010-12-09 | `{"config": {"C": 0.01}, "rows": 12281, "status": "ok", "warnings": []}` |
| 434 | final_fit_before_unseal | fit | logistic | inner:2011-01-09 | `{"config": {"C": 0.01}, "rows": 15927, "status": "ok", "warnings": []}` |
| 435 | final_fit_before_unseal | fit | logistic | inner:2011-02-09 | `{"config": {"C": 0.01}, "rows": 19923, "status": "ok", "warnings": []}` |
| 436 | final_fit_before_unseal | fit | logistic | inner:2011-03-09 | `{"config": {"C": 0.01}, "rows": 24152, "status": "ok", "warnings": []}` |
| 437 | final_fit_before_unseal | fit | logistic | inner:2011-04-09 | `{"config": {"C": 0.01}, "rows": 28362, "status": "ok", "warnings": []}` |
| 438 | final_fit_before_unseal | candidate | logistic | final_frozen_fit | `{"config": {"C": 0.01}, "inner_average_precision": 0.7564709430904903, "validation_rows": 32261}` |
| 439 | final_fit_before_unseal | fit | logistic | inner:2010-09-09 | `{"config": {"C": 0.1}, "rows": 2760, "status": "ok", "warnings": []}` |
| 440 | final_fit_before_unseal | fit | logistic | inner:2010-10-09 | `{"config": {"C": 0.1}, "rows": 5770, "status": "ok", "warnings": []}` |
| 441 | final_fit_before_unseal | fit | logistic | inner:2010-11-09 | `{"config": {"C": 0.1}, "rows": 8944, "status": "ok", "warnings": []}` |
| 442 | final_fit_before_unseal | fit | logistic | inner:2010-12-09 | `{"config": {"C": 0.1}, "rows": 12281, "status": "ok", "warnings": []}` |
| 443 | final_fit_before_unseal | fit | logistic | inner:2011-01-09 | `{"config": {"C": 0.1}, "rows": 15927, "status": "ok", "warnings": []}` |
| 444 | final_fit_before_unseal | fit | logistic | inner:2011-02-09 | `{"config": {"C": 0.1}, "rows": 19923, "status": "ok", "warnings": []}` |
| 445 | final_fit_before_unseal | fit | logistic | inner:2011-03-09 | `{"config": {"C": 0.1}, "rows": 24152, "status": "ok", "warnings": []}` |
| 446 | final_fit_before_unseal | fit | logistic | inner:2011-04-09 | `{"config": {"C": 0.1}, "rows": 28362, "status": "ok", "warnings": []}` |
| 447 | final_fit_before_unseal | candidate | logistic | final_frozen_fit | `{"config": {"C": 0.1}, "inner_average_precision": 0.7533095963792743, "validation_rows": 32261}` |
| 448 | final_fit_before_unseal | fit | logistic | inner:2010-09-09 | `{"config": {"C": 1.0}, "rows": 2760, "status": "ok", "warnings": []}` |
| 449 | final_fit_before_unseal | fit | logistic | inner:2010-10-09 | `{"config": {"C": 1.0}, "rows": 5770, "status": "ok", "warnings": []}` |
| 450 | final_fit_before_unseal | fit | logistic | inner:2010-11-09 | `{"config": {"C": 1.0}, "rows": 8944, "status": "ok", "warnings": []}` |
| 451 | final_fit_before_unseal | fit | logistic | inner:2010-12-09 | `{"config": {"C": 1.0}, "rows": 12281, "status": "ok", "warnings": []}` |
| 452 | final_fit_before_unseal | fit | logistic | inner:2011-01-09 | `{"config": {"C": 1.0}, "rows": 15927, "status": "ok", "warnings": []}` |
| 453 | final_fit_before_unseal | fit | logistic | inner:2011-02-09 | `{"config": {"C": 1.0}, "rows": 19923, "status": "ok", "warnings": []}` |
| 454 | final_fit_before_unseal | fit | logistic | inner:2011-03-09 | `{"config": {"C": 1.0}, "rows": 24152, "status": "ok", "warnings": []}` |
| 455 | final_fit_before_unseal | fit | logistic | inner:2011-04-09 | `{"config": {"C": 1.0}, "rows": 28362, "status": "ok", "warnings": []}` |
| 456 | final_fit_before_unseal | candidate | logistic | final_frozen_fit | `{"config": {"C": 1.0}, "inner_average_precision": 0.7447938782229744, "validation_rows": 32261}` |
| 457 | final_fit_before_unseal | calibration | logistic | final_frozen_fit | `{"candidates": [{"brier": 0.23753578401276132, "kind": "platt", "validation_rows": 21282}, {"brier": 0.23241334634993738, "kind": "isotonic", "validation_rows": 21282}], "selected": "isotonic"}` |
| 458 | final_fit_before_unseal | fit | logistic | final_frozen_fit | `{"config": {"C": 0.01}, "rows": 41205, "status": "ok", "warnings": []}` |
| 459 | final_fit_before_unseal | fit | lightgbm | inner:2010-09-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 2760, "status": "ok", "warnings": []}` |
| 460 | final_fit_before_unseal | fit | lightgbm | inner:2010-10-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 5770, "status": "ok", "warnings": []}` |
| 461 | final_fit_before_unseal | fit | lightgbm | inner:2010-11-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 8944, "status": "ok", "warnings": []}` |
| 462 | final_fit_before_unseal | fit | lightgbm | inner:2010-12-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 12281, "status": "ok", "warnings": []}` |
| 463 | final_fit_before_unseal | fit | lightgbm | inner:2011-01-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 15927, "status": "ok", "warnings": []}` |
| 464 | final_fit_before_unseal | fit | lightgbm | inner:2011-02-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 19923, "status": "ok", "warnings": []}` |
| 465 | final_fit_before_unseal | fit | lightgbm | inner:2011-03-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 24152, "status": "ok", "warnings": []}` |
| 466 | final_fit_before_unseal | fit | lightgbm | inner:2011-04-09 | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 28362, "status": "ok", "warnings": []}` |
| 467 | final_fit_before_unseal | candidate | lightgbm | final_frozen_fit | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "inner_average_precision": 0.7599901110936554, "validation_rows": 32261}` |
| 468 | final_fit_before_unseal | fit | lightgbm | inner:2010-09-09 | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "rows": 2760, "status": "ok", "warnings": []}` |
| 469 | final_fit_before_unseal | fit | lightgbm | inner:2010-10-09 | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "rows": 5770, "status": "ok", "warnings": []}` |
| 470 | final_fit_before_unseal | fit | lightgbm | inner:2010-11-09 | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "rows": 8944, "status": "ok", "warnings": []}` |
| 471 | final_fit_before_unseal | fit | lightgbm | inner:2010-12-09 | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "rows": 12281, "status": "ok", "warnings": []}` |
| 472 | final_fit_before_unseal | fit | lightgbm | inner:2011-01-09 | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "rows": 15927, "status": "ok", "warnings": []}` |
| 473 | final_fit_before_unseal | fit | lightgbm | inner:2011-02-09 | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "rows": 19923, "status": "ok", "warnings": []}` |
| 474 | final_fit_before_unseal | fit | lightgbm | inner:2011-03-09 | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "rows": 24152, "status": "ok", "warnings": []}` |
| 475 | final_fit_before_unseal | fit | lightgbm | inner:2011-04-09 | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "rows": 28362, "status": "ok", "warnings": []}` |
| 476 | final_fit_before_unseal | candidate | lightgbm | final_frozen_fit | `{"config": {"min_child_samples": 50, "num_leaves": 15}, "inner_average_precision": 0.756141963734571, "validation_rows": 32261}` |
| 477 | final_fit_before_unseal | fit | lightgbm | inner:2010-09-09 | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "rows": 2760, "status": "ok", "warnings": []}` |
| 478 | final_fit_before_unseal | fit | lightgbm | inner:2010-10-09 | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "rows": 5770, "status": "ok", "warnings": []}` |
| 479 | final_fit_before_unseal | fit | lightgbm | inner:2010-11-09 | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "rows": 8944, "status": "ok", "warnings": []}` |
| 480 | final_fit_before_unseal | fit | lightgbm | inner:2010-12-09 | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "rows": 12281, "status": "ok", "warnings": []}` |
| 481 | final_fit_before_unseal | fit | lightgbm | inner:2011-01-09 | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "rows": 15927, "status": "ok", "warnings": []}` |
| 482 | final_fit_before_unseal | fit | lightgbm | inner:2011-02-09 | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "rows": 19923, "status": "ok", "warnings": []}` |
| 483 | final_fit_before_unseal | fit | lightgbm | inner:2011-03-09 | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "rows": 24152, "status": "ok", "warnings": []}` |
| 484 | final_fit_before_unseal | fit | lightgbm | inner:2011-04-09 | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "rows": 28362, "status": "ok", "warnings": []}` |
| 485 | final_fit_before_unseal | candidate | lightgbm | final_frozen_fit | `{"config": {"min_child_samples": 100, "num_leaves": 15}, "inner_average_precision": 0.7570175484832068, "validation_rows": 32261}` |
| 486 | final_fit_before_unseal | fit | lightgbm | inner:2010-09-09 | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "rows": 2760, "status": "ok", "warnings": []}` |
| 487 | final_fit_before_unseal | fit | lightgbm | inner:2010-10-09 | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "rows": 5770, "status": "ok", "warnings": []}` |
| 488 | final_fit_before_unseal | fit | lightgbm | inner:2010-11-09 | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "rows": 8944, "status": "ok", "warnings": []}` |
| 489 | final_fit_before_unseal | fit | lightgbm | inner:2010-12-09 | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "rows": 12281, "status": "ok", "warnings": []}` |
| 490 | final_fit_before_unseal | fit | lightgbm | inner:2011-01-09 | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "rows": 15927, "status": "ok", "warnings": []}` |
| 491 | final_fit_before_unseal | fit | lightgbm | inner:2011-02-09 | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "rows": 19923, "status": "ok", "warnings": []}` |
| 492 | final_fit_before_unseal | fit | lightgbm | inner:2011-03-09 | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "rows": 24152, "status": "ok", "warnings": []}` |
| 493 | final_fit_before_unseal | fit | lightgbm | inner:2011-04-09 | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "rows": 28362, "status": "ok", "warnings": []}` |
| 494 | final_fit_before_unseal | candidate | lightgbm | final_frozen_fit | `{"config": {"min_child_samples": 100, "num_leaves": 31}, "inner_average_precision": 0.7528942509723053, "validation_rows": 32261}` |
| 495 | final_fit_before_unseal | calibration | lightgbm | final_frozen_fit | `{"candidates": [{"brier": 0.22362351057452073, "kind": "platt", "validation_rows": 21282}, {"brier": 0.2207951363227316, "kind": "isotonic", "validation_rows": 21282}], "selected": "isotonic"}` |
| 496 | final_fit_before_unseal | fit | lightgbm | final_frozen_fit | `{"config": {"min_child_samples": 50, "num_leaves": 7}, "rows": 41205, "status": "ok", "warnings": []}` |
| 497 | final_fit_before_unseal | fit | recency | inner:2010-09-09 | `{"config": {}, "rows": 2760, "status": "ok", "warnings": []}` |
| 498 | final_fit_before_unseal | fit | recency | inner:2010-10-09 | `{"config": {}, "rows": 5770, "status": "ok", "warnings": []}` |
| 499 | final_fit_before_unseal | fit | recency | inner:2010-11-09 | `{"config": {}, "rows": 8944, "status": "ok", "warnings": []}` |
| 500 | final_fit_before_unseal | fit | recency | inner:2010-12-09 | `{"config": {}, "rows": 12281, "status": "ok", "warnings": []}` |
| 501 | final_fit_before_unseal | fit | recency | inner:2011-01-09 | `{"config": {}, "rows": 15927, "status": "ok", "warnings": []}` |
| 502 | final_fit_before_unseal | fit | recency | inner:2011-02-09 | `{"config": {}, "rows": 19923, "status": "ok", "warnings": []}` |
| 503 | final_fit_before_unseal | fit | recency | inner:2011-03-09 | `{"config": {}, "rows": 24152, "status": "ok", "warnings": []}` |
| 504 | final_fit_before_unseal | fit | recency | inner:2011-04-09 | `{"config": {}, "rows": 28362, "status": "ok", "warnings": []}` |
| 505 | final_fit_before_unseal | candidate | recency | final_frozen_fit | `{"config": {}, "inner_average_precision": 0.7531047140846185, "validation_rows": 32261}` |
| 506 | final_fit_before_unseal | calibration | recency | final_frozen_fit | `{"candidates": [{"brier": 0.227839498686377, "kind": "platt", "validation_rows": 21282}, {"brier": 0.22819427053447602, "kind": "isotonic", "validation_rows": 21282}], "selected": "platt"}` |
| 507 | final_fit_before_unseal | threshold | recency | final_frozen_fit | `{"inner_profit": 25787.154199999997, "k": 30}` |
| 508 | final_fit_before_unseal | threshold | recency | final_frozen_fit | `{"inner_profit": 10463.3243, "k": 60}` |
| 509 | final_fit_before_unseal | threshold | recency | final_frozen_fit | `{"inner_profit": 0.0, "k": 90}` |
| 510 | final_fit_before_unseal | threshold | recency | final_frozen_fit | `{"inner_profit": 0.0, "k": 120}` |
| 511 | final_fit_before_unseal | threshold | recency | final_frozen_fit | `{"inner_profit": 0.0, "k": 180}` |
| 512 | final_fit_before_unseal | threshold | recency | final_frozen_fit | `{"inner_profit": 0.0, "k": 270}` |
| 513 | final_fit_before_unseal | fit | recency | final_frozen_fit | `{"config": {}, "rows": 41205, "status": "ok", "warnings": []}` |
| 514 | final_fit_before_unseal | fit | rfm | inner:2010-09-09 | `{"config": {}, "rows": 2760, "status": "ok", "warnings": []}` |
| 515 | final_fit_before_unseal | fit | rfm | inner:2010-10-09 | `{"config": {}, "rows": 5770, "status": "ok", "warnings": []}` |
| 516 | final_fit_before_unseal | fit | rfm | inner:2010-11-09 | `{"config": {}, "rows": 8944, "status": "ok", "warnings": []}` |
| 517 | final_fit_before_unseal | fit | rfm | inner:2010-12-09 | `{"config": {}, "rows": 12281, "status": "ok", "warnings": []}` |
| 518 | final_fit_before_unseal | fit | rfm | inner:2011-01-09 | `{"config": {}, "rows": 15927, "status": "ok", "warnings": []}` |
| 519 | final_fit_before_unseal | fit | rfm | inner:2011-02-09 | `{"config": {}, "rows": 19923, "status": "ok", "warnings": []}` |
| 520 | final_fit_before_unseal | fit | rfm | inner:2011-03-09 | `{"config": {}, "rows": 24152, "status": "ok", "warnings": []}` |
| 521 | final_fit_before_unseal | fit | rfm | inner:2011-04-09 | `{"config": {}, "rows": 28362, "status": "ok", "warnings": []}` |
| 522 | final_fit_before_unseal | candidate | rfm | final_frozen_fit | `{"config": {}, "inner_average_precision": 0.7615015374917032, "validation_rows": 32261}` |
| 523 | final_fit_before_unseal | calibration | rfm | final_frozen_fit | `{"candidates": [{"brier": 0.21807517674860938, "kind": "platt", "validation_rows": 21282}, {"brier": 0.2177931614730129, "kind": "isotonic", "validation_rows": 21282}], "selected": "isotonic"}` |
| 524 | final_fit_before_unseal | fit | rfm | final_frozen_fit | `{"config": {}, "rows": 41205, "status": "ok", "warnings": []}` |
| 525 | final_fit_before_unseal | fit | bgnbd | inner:2010-09-09 | `{"config": {}, "rows": 2760, "status": "ok", "warnings": []}` |
| 526 | final_fit_before_unseal | fit | bgnbd | inner:2010-10-09 | `{"config": {}, "rows": 5770, "status": "ok", "warnings": []}` |
| 527 | final_fit_before_unseal | fit | bgnbd | inner:2010-11-09 | `{"config": {}, "rows": 8944, "status": "ok", "warnings": []}` |
| 528 | final_fit_before_unseal | fit | bgnbd | inner:2010-12-09 | `{"config": {}, "rows": 12281, "status": "ok", "warnings": []}` |
| 529 | final_fit_before_unseal | fit | bgnbd | inner:2011-01-09 | `{"config": {}, "rows": 15927, "status": "ok", "warnings": []}` |
| 530 | final_fit_before_unseal | fit | bgnbd | inner:2011-02-09 | `{"config": {}, "rows": 19923, "status": "ok", "warnings": []}` |
| 531 | final_fit_before_unseal | fit | bgnbd | inner:2011-03-09 | `{"config": {}, "rows": 24152, "status": "ok", "warnings": []}` |
| 532 | final_fit_before_unseal | fit | bgnbd | inner:2011-04-09 | `{"config": {}, "rows": 28362, "status": "ok", "warnings": []}` |
| 533 | final_fit_before_unseal | candidate | bgnbd | final_frozen_fit | `{"config": {}, "inner_average_precision": 0.7883166981797933, "validation_rows": 32261}` |
| 534 | final_fit_before_unseal | calibration | bgnbd | final_frozen_fit | `{"candidates": [{"brier": 0.20186774862961435, "kind": "platt", "validation_rows": 21282}, {"brier": 0.20217921506733352, "kind": "isotonic", "validation_rows": 21282}], "selected": "platt"}` |
| 535 | final_fit_before_unseal | fit | bgnbd | final_frozen_fit | `{"config": {}, "rows": 41205, "status": "ok", "warnings": []}` |
| 536 | final_fit_before_unseal | fit | constant | inner:2010-09-09 | `{"config": {}, "rows": 2760, "status": "ok", "warnings": []}` |
| 537 | final_fit_before_unseal | fit | constant | inner:2010-10-09 | `{"config": {}, "rows": 5770, "status": "ok", "warnings": []}` |
| 538 | final_fit_before_unseal | fit | constant | inner:2010-11-09 | `{"config": {}, "rows": 8944, "status": "ok", "warnings": []}` |
| 539 | final_fit_before_unseal | fit | constant | inner:2010-12-09 | `{"config": {}, "rows": 12281, "status": "ok", "warnings": []}` |
| 540 | final_fit_before_unseal | fit | constant | inner:2011-01-09 | `{"config": {}, "rows": 15927, "status": "ok", "warnings": []}` |
| 541 | final_fit_before_unseal | fit | constant | inner:2011-02-09 | `{"config": {}, "rows": 19923, "status": "ok", "warnings": []}` |
| 542 | final_fit_before_unseal | fit | constant | inner:2011-03-09 | `{"config": {}, "rows": 24152, "status": "ok", "warnings": []}` |
| 543 | final_fit_before_unseal | fit | constant | inner:2011-04-09 | `{"config": {}, "rows": 28362, "status": "ok", "warnings": []}` |
| 544 | final_fit_before_unseal | candidate | constant | final_frozen_fit | `{"config": {}, "inner_average_precision": 0.5921390460591156, "validation_rows": 32261}` |
| 545 | final_fit_before_unseal | calibration | constant | final_frozen_fit | `{"candidates": [{"brier": 0.28520397283907867, "kind": "platt", "validation_rows": 21282}, {"brier": 0.2546470053760454, "kind": "isotonic", "validation_rows": 21282}], "selected": "native"}` |
| 546 | final_fit_before_unseal | fit | constant | final_frozen_fit | `{"config": {}, "rows": 41205, "status": "ok", "warnings": []}` |
