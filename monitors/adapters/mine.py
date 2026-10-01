"""Dependency-free, anytime weighted facility-location search.

Uses only the supplied instance; no public anchors or stored solutions.
Sparse exact swap evaluation followed by iterated local search.
"""

from random import Random
from time import perf_counter

from adapter import Solver, dist_table


def state(opened, columns, n):
    first, second, owner = [0] * n, [0] * n, [-1] * n
    for pos, site in enumerate(opened):
        for i, value in columns[site]:
            if value > first[i]:
                second[i] = first[i]
                first[i], owner[i] = value, pos
            elif value > second[i]:
                second[i] = value
    loss = [0] * len(opened)
    for i, pos in enumerate(owner):
        if pos >= 0:
            loss[pos] += first[i] - second[i]
    return first, second, owner, loss


def best_swap(opened, columns, n):
    """Exact best single exchange in O(nonzero table entries + m*k)."""
    first, second, owner, loss = state(opened, columns, n)
    occupied = set(opened)
    best_gain, move = 0, None
    for site, col in enumerate(columns):
        if site in occupied:
            continue
        recovery = [0] * len(opened)
        gain = 0
        for i, value in col:
            a, b = first[i], second[i]
            if value > a:
                gain += value - a
                if owner[i] >= 0:
                    recovery[owner[i]] += a - b
            elif value > b:
                recovery[owner[i]] += value - b
        for pos, removal in enumerate(loss):
            delta = gain + recovery[pos] - removal
            if delta > best_gain:
                best_gain, move = delta, (pos, site)
    return sum(first), best_gain, move


class MySolver(Solver):
    def solve(self, instance, submit_candidate):
        k, m, n = instance.k, len(instance.sites), instance.size
        # This cheap feasible fallback protects the first checkpoint even on
        # unusually slow hardware. Time is synchronized with parent receipts.
        best = list(range(k))
        receipt = submit_candidate({"sites": best[:]})
        deadline = perf_counter() + max(0.0, receipt["remaining_s"] - 0.15)
        if perf_counter() >= deadline or k == m:
            return {"sites": best}
        table = dist_table(instance)
        penalty = instance.penalty
        columns = [[] for _ in range(m)]
        for i, (weight, row) in enumerate(zip(instance.weights, table)):
            for site, distance in enumerate(row):
                if distance < penalty:
                    columns[site].append((i, weight * (penalty - distance)))
        total = penalty * sum(instance.weights)
        best_value = total - receipt["cost"]
        rng = Random(20261001)

        def publish(opened, value):
            nonlocal best, best_value, deadline
            if value > best_value:
                best, best_value = opened[:], value
                r = submit_candidate({"sites": best[:]})
                deadline = min(deadline, perf_counter() + max(0.0, r["remaining_s"] - 0.15))

        def greedy(seed):
            opened = seed[:]
            current = [0] * n
            for site in opened:
                for i, value in columns[site]:
                    if value > current[i]:
                        current[i] = value
            closed = set(range(m)) - set(opened)
            while len(opened) < k:
                chosen = max(closed, key=lambda s: sum(v - current[i] for i, v in columns[s] if v > current[i]))
                opened.append(chosen)
                closed.remove(chosen)
                for i, value in columns[chosen]:
                    if value > current[i]:
                        current[i] = value
            return opened, sum(current)

        opened, value = greedy([])
        publish(opened, value)
        elite = []
        seen = set()
        iteration = 0
        while perf_counter() < deadline:
            value, gain, move = best_swap(opened, columns, n)
            if move is not None:
                opened[move[0]] = move[1]
                publish(opened, value + gain)
                continue
            publish(opened, value)
            key = tuple(sorted(opened))
            if key not in seen:
                seen.add(key)
                elite.append((value, opened[:]))
                elite.sort(key=lambda item: item[0], reverse=True)
                del elite[12:]
            iteration += 1
            if iteration % 9 == 0:
                opened, value = greedy(rng.sample(range(m), min(k, 1 + iteration % 3)))
                publish(opened, value)
            else:
                base = best if iteration % 3 else rng.choice(elite)[1]
                # Destroy varying-size subsets and repair, alternating with
                # random exchanges to escape greedy reconstruction basins.
                count = min(k, m - k, 2 + iteration % max(2, k // 2))
                opened = base[:]
                positions = rng.sample(range(k), count)
                if iteration % 2:
                    replacements = rng.sample([s for s in range(m) if s not in opened], count)
                    for pos, site in zip(positions, replacements):
                        opened[pos] = site
                else:
                    removed = set(positions)
                    opened, value = greedy([s for pos, s in enumerate(opened) if pos not in removed])
                    publish(opened, value)
        return {"sites": best}
