"""Compare on new generated instances; these are NOT organizer private tests."""
import run_windows  # Windows OS compatibility only, no scoring modifications.
import argparse
import json
from dataclasses import asdict

import data
import metrics
from benchkit import SuiteEntry
from benchkit.runner import run_instance


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="fresh_report.json")
    parser.add_argument("--count", type=int, default=12)
    args = parser.parse_args()
    results = []
    for i in range(args.count):
        template = data.PUBLIC_SUITE[i % len(data.PUBLIC_SUITE)]
        profile = {**template.profile, "attempt": 0}
        entry = SuiteEntry(f"fresh-{i + 1:02d}", 907001 + i * 137, profile)
        baseline = run_instance(metrics.BENCH, entry, "adapters.baseline:BaselineSolver")
        mine = run_instance(metrics.BENCH, entry, "adapters.mine:MySolver")
        improvement = 100 * (baseline.final_cost - mine.final_cost) / baseline.final_cost
        clean = not (mine.crashed or mine.overrun or mine.rejected) and mine.checkpoint_costs[0] is not None
        print(f"{entry.name} {profile['family']}: baseline={baseline.final_cost}, mine={mine.final_cost}, reduction={improvement:.2f}%, clean={clean}", flush=True)
        results.append({"baseline": asdict(baseline), "mine": asdict(mine), "reduction_percent": improvement, "clean": clean})
    with open(args.out, "w") as stream:
        json.dump({"note": "Fresh local generated cases, not the organizer private suite; no reference scores are available.", "results": results}, stream, indent=2)
    assert all(r["clean"] and r["mine"]["final_cost"] <= r["baseline"]["final_cost"] for r in results)


if __name__ == "__main__":
    main()
