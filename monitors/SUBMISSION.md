# Monitor Placement submission

Submit `adapters/mine.py`, class `MySolver`. The adapter specification is
`adapters.mine:MySolver`. It uses only Python's standard library and the
provided `adapter.py`. No installation, API key, network access, or model
call is required during evaluation.

## Run on the organizer's Linux environment

From the `monitors` directory:

```sh
python self_check.py --adapter adapters.mine:MySolver
python run.py --adapter adapters.mine:MySolver --out report.json
```

## Run locally on Windows

The supplied runner calls Unix-only process functions. The separate local
launcher adapts only those missing functions:

```powershell
python run_windows.py --adapter adapters.mine:MySolver --out report.json
python -m unittest test_solver -v
python check_fresh.py --count 12 --out fresh_report.json
```

The Windows launcher uses the original process-based runner, validator,
five-second budget, checkpoint calculation, anchors, and score aggregation.
It does not provide Linux privilege dropping or memory/process-group isolation.
Use it only to test trusted code. All organizer-provided files are unchanged.
The launcher is not part of the solver submission.

## Algorithm

The objective is rewritten as maximizing population-weighted savings relative
to leaving every demand point uncovered. Each candidate stores only the demand
points within its coverage radius, making the calculations sparse.

1. Submit a valid fallback immediately.
2. Construct a greedy solution using exact marginal savings.
3. Evaluate every single-site exchange using nearest and second-nearest savings.
   Removal losses and incoming-site recoveries give exact exchange gains.
4. Apply the best improving exchange until no exchange helps.
5. Escape local optima through random exchanges, partial destruction followed
   by greedy repair, and restarts from a small pool of good solutions.
6. Submit each new global improvement. Return the best solution with a safety
   margin of 0.15 seconds before the parent-reported deadline.

Distances are the evaluator's integer, radius-capped distances. The solver
does not inspect instance names, generator seeds, public reference files,
stored answers, or private data. The fixed random seed makes the sequence of
search decisions reproducible; the time-limited endpoint can vary by machine.

## Verification

`test_solver.py` checks the exchange arithmetic against exhaustive exact
recalculation on 120 randomized small cases, including ties and zero savings.
It also checks one-site, all-sites, uncovered, and short-budget cases.

`check_fresh.py` compares the solver to the supplied baseline on 12 new
generated instances across both families. These are local holdout cases,
not the organizer's hidden private suite; private scores cannot be inferred
from them.

See `RESULTS.md` and the JSON reports for measured results. Public reference
costs are scoring targets, not proofs of global optimality. A public score
of 100 does not guarantee 100 on private instances or a different machine.
