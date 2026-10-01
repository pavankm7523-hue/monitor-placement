# Measured results — 1 October 2026

## Public benchmark: 100 / 100 in two full runs

| Component | Run 1 | Run 2 |
|---|---:|---:|
| Quality | 70 / 70 | 70 / 70 |
| Robustness | 20 / 20 | 20 / 20 |
| Engineering | 10 / 10 | 10 / 10 |
| Total | **100 / 100** | **100 / 100** |

All six instances matched the public reference at all four scoring
checkpoints in both runs. No crashes, overruns, or rejected submissions.

| Instance | Family | Solver cost (both runs) | Reference cost |
|---|---|---:|---:|
| monitors-01 | uniform | 2,965,159 | 2,965,159 |
| monitors-02 | uniform | 4,230,218 | 4,230,218 |
| monitors-03 | uniform | 5,302,031 | 5,302,031 |
| monitors-04 | uniform | 6,442,771 | 6,442,771 |
| monitors-05 | clustered | 232,180 | 232,180 |
| monitors-06 | clustered | 309,586 | 309,586 |

Evidence: `public_report.json` and `public_report_repeat.json` contain
full histories, checkpoint costs, validation counts, timing, and scores.

## Fresh generated cases

12 new cases: eight uniform and four clustered, using the published
generator with new seeds. The solver improved on the supplied baseline
in eight cases and tied it in four. It lost none. Mean cost reduction
was 2.30%, with a maximum of 6.46%. All 12 had valid early submissions
and no rejected candidates, crashes, or overruns.

Evidence: `fresh_report.json`. There are no private reference anchors for
these cases, so no score out of 100 is claimed for them.

## Correctness checks

Both test methods passed. The swap test compares cached gains against
exhaustive recalculation on 120 randomized cases, including ties and
zero savings. Edge tests cover one selected site, selecting all sites,
uncovered points, and a short remaining time budget.

## Environment and limitations

Windows, Python 3.14.3, standard library only. Tests ran sequentially
through `run_windows.py`, which adapts the supplied runner's Unix-only
process-control calls. The solver runs in a spawned child process; the
original parent performs validation, timing, and scoring. All original
organizer files, including the validator, runner, anchors, and scoring,
were checked to be byte-for-byte unchanged.

The original Linux launch path has not been run on this machine because
its WSL installation is unavailable. The solver itself uses portable
Python. Re-run the original `run.py` in the organizer's Linux environment
before submission if available. Hidden private scores and performance
on a different machine remain unverified.
