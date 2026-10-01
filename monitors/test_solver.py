"""Exact checks for cached swap arithmetic, ties, and solver edge cases."""
import itertools
import random
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from adapters.mine import MySolver, best_swap


class SolverTests(unittest.TestCase):
    def test_swap_against_exhaustive_recalculation(self):
        rng = random.Random(29)
        for _ in range(120):
            n, m = rng.randrange(1, 15), rng.randrange(2, 11)
            k = rng.randrange(1, m)
            matrix = [[rng.randrange(5) * 10 for _ in range(m)] for _ in range(n)]
            columns = [[(i, row[s]) for i, row in enumerate(matrix) if row[s]] for s in range(m)]
            opened = rng.sample(range(m), k)
            exact = lambda sites: sum(max(row[s] for s in sites) for row in matrix)
            value, gain, move = best_swap(opened, columns, n)
            target = max(exact(opened[:p] + [s] + opened[p + 1:]) for p in range(k) for s in range(m) if s not in opened)
            self.assertEqual(value, exact(opened))
            self.assertEqual(gain, max(0, target - value))
            if move is not None:
                changed = opened[:]
                changed[move[0]] = move[1]
                self.assertEqual(exact(changed), value + gain)

    def test_edge_cases_and_short_budget(self):
        for k, table in [(1, [[10, 10, 10], [10, 10, 10]]), (1, [[1, 2, 8], [9, 2, 8]]), (3, [[1, 2, 3], [3, 2, 1]])]:
            instance = SimpleNamespace(k=k, size=2, sites=tuple(range(3)), weights=(1, 2), penalty=10)
            costs = []
            def submit(plan):
                sites = plan["sites"]
                self.assertEqual(len(sites), k)
                self.assertEqual(len(set(sites)), k)
                self.assertTrue(all(type(s) is int and 0 <= s < 3 for s in sites))
                cost = sum(w * min(row[s] for s in sites) for w, row in zip(instance.weights, table))
                costs.append(cost)
                return {"cost": cost, "remaining_s": .18, "accepted": True}
            with patch("adapters.mine.dist_table", return_value=table):
                plan = MySolver().solve(instance, submit)
            expected = min(sum(w * min(row[s] for s in sites) for w, row in zip(instance.weights, table)) for sites in itertools.combinations(range(3), k))
            submit(plan)
            self.assertEqual(costs[-1], expected)


if __name__ == "__main__":
    unittest.main()
