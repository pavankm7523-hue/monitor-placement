# Monitor Placement

A Python solver for the **Algo Ranabhoomi Phase 1 — Monitor Placement**
optimization challenge. Choose exactly `k` permitted air-quality monitor sites
to minimize population-weighted distance, with a penalty for uncovered demand.

**Measured public benchmark: 100/100 in two full local runs.**

| Component | Score |
|---|---:|
| Quality | 70/70 |
| Robustness | 20/20 |
| Engineering | 10/10 |

All six public instances reached their reference cost before the first
checkpoint in both runs. On 12 additional generated cases, the solver beat
the supplied baseline eight times and tied four times, with no invalid
submissions, crashes, or overruns.

These measurements were made on Windows with Python 3.14.3 using a compatibility
launcher for the supplied runner's Unix-only process controls. The original
validator, scoring, anchors, and timing code are unchanged. Hidden private
scores and results on other machines are not guaranteed.

## Submission

The submission file is **[monitors/adapters/mine.py](monitors/adapters/mine.py)**.
Place it in the organizer's `monitors/adapters/` directory and use adapter
specification `adapters.mine:MySolver`.

Python standard library only. No API keys, external packages, network calls,
or AI model calls are required to run the solver.

## Run

```sh
git clone https://github.com/pavankm7523-hue/monitor-placement.git
cd monitor-placement/monitors
```

Linux / organizer environment:

```sh
python self_check.py --adapter adapters.mine:MySolver
python run.py --adapter adapters.mine:MySolver --out report.json
```

Windows:

```powershell
python run_windows.py --adapter adapters.mine:MySolver --out report.json
```

Correctness tests and additional generated cases:

```sh
python -m unittest test_solver -v
python check_fresh.py --count 12 --out fresh_report.json
```

## How it works

The solver represents each site's benefit as population-weighted savings
relative to leaving demand uncovered. Sparse coverage lists accelerate exact
swap evaluation using each demand point's best and second-best selected site.
A greedy construction is improved by repeated best swaps, randomized exchanges,
partial destruction and greedy repair, and restarts from good previous solutions.
Every new best solution is submitted immediately, with a margin before the
five-second deadline.

The solver does not read reference costs, instance names, stored solutions,
or private data. It uses only the instance supplied to `solve`.

## Evidence and documentation

- [Measured results and limitations](monitors/RESULTS.md)
- [First public benchmark report](monitors/public_report.json)
- [Repeat public benchmark report](monitors/public_report_repeat.json)
- [Fresh-instance comparison report](monitors/fresh_report.json)
- [Submission instructions and algorithm details](monitors/SUBMISSION.md)
- [Original problem statement](monitors/README.md)
- [Original evaluation boundary](monitors/SECURITY.md)

The original challenge files are preserved from the provided
`Algo-Ranabhoomi-Phase_1-main.zip`. The custom solver, tests, Windows launcher,
and submission documentation are additions. No new license is asserted over
the organizer-provided files.
