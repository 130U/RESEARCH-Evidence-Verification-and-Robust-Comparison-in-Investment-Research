"""Sections 1 to 4: what to verify next, and how many misstatements a ranking survives.

For an affine score difference D(u) = m + sum_j a_j u_j with each unresolved quantity in
an interval |u_j| <= d_j, field j has swing s_j = |a_j| d_j and the total swing is
h = sum_j s_j. The script evaluates the closed forms of Section 4 and confirms each by
exhaustive search.
"""

from __future__ import annotations

import itertools
import math
import random


# ----------------------------------------------------------------- regret after verification
def residual_regret(m: float, swings, verified=()) -> float:
    """Worst-case regret that remains after verifying the fields in `verified`, with the
    action chosen again once their values are known: (h - max(s_J, |m|))_+ ."""
    h = sum(swings)
    s_j = sum(swings[j] for j in verified)
    return max(0.0, h - max(s_j, abs(m)))


def guaranteed_value(m: float, swings, verified) -> float:
    return residual_regret(m, swings) - residual_regret(m, swings, verified)


def search_regret(m: float, swings, verified, points: int = 20_001) -> float:
    """The same quantity by search. Only the sum t of the verified coordinates matters,
    and it ranges over [-s_J, s_J]; the worst t is found on a fine grid that includes the
    point where the revised margin is smallest."""
    s_j = sum(swings[j] for j in verified)
    rest = sum(swings) - s_j
    candidates = [-s_j + 2 * s_j * i / (points - 1) for i in range(points)] if s_j > 0 else [0.0]
    candidates.append(max(-s_j, min(s_j, -m)))
    worst = 0.0
    for t in candidates:
        margin = m + t
        worst = max(worst, min(max(0.0, rest - margin), max(0.0, rest + margin)))
    return worst


def check_closed_form(trials: int = 300, seed: int = 11) -> float:
    """Largest gap between the closed form and the search over random instances and all
    subsets of four fields."""
    rng = random.Random(seed)
    gap = 0.0
    for _ in range(trials):
        swings = [round(rng.uniform(0.05, 0.6), 2) for _ in range(4)]
        m = round(rng.uniform(-0.8, 0.8), 2)
        for r in range(5):
            for subset in itertools.combinations(range(4), r):
                gap = max(gap, abs(residual_regret(m, swings, subset) - search_regret(m, swings, subset)))
    return gap


# ----------------------------------------------------------------------- budgeted plans
def best_plan(m: float, swings, costs, budget: float):
    """Verification set within the budget that leaves the least residual regret
    (exhaustive over subsets; ties go to the cheaper set)."""
    best = (residual_regret(m, swings), 0.0, ())
    for r in range(1, len(swings) + 1):
        for subset in itertools.combinations(range(len(swings)), r):
            cost = sum(costs[j] for j in subset)
            if cost <= budget:
                cand = (residual_regret(m, swings, subset), cost, subset)
                if cand[:2] < best[:2]:
                    best = cand
    return best


def greedy_by_density(swings, costs, budget: float):
    """Fields in decreasing order of swing per unit cost, skipping what does not fit."""
    chosen, left = [], budget
    for j in sorted(range(len(swings)), key=lambda j: -swings[j] / costs[j]):
        if costs[j] <= left:
            chosen.append(j)
            left -= costs[j]
    return tuple(sorted(chosen))


def largest_swing_first(swings, costs, budget: float):
    chosen, left = [], budget
    for j in sorted(range(len(swings)), key=lambda j: -swings[j]):
        if costs[j] <= left:
            chosen.append(j)
            left -= costs[j]
    return tuple(sorted(chosen))


# ------------------------------------------------------------------ misstatement tolerance
def misstatement_tolerance(m: float, swings) -> int:
    """Largest number of simultaneous worst-case misstatements the ordering survives:
    the largest G with the G largest swings summing to less than m."""
    total, count = 0.0, 0
    for s in sorted(swings, reverse=True):
        if total + s < m - 1e-12:
            total, count = total + s, count + 1
        else:
            break
    return count


def check_tolerance(m: float, swings) -> bool:
    """Exhaustive: every set of G* fields at worst case leaves the margin positive, and
    some set of G* + 1 fields does not."""
    g = misstatement_tolerance(m, swings)
    for subset in itertools.combinations(range(len(swings)), g):
        if m - sum(swings[j] for j in subset) <= 0:
            return False
    if g < len(swings):
        if all(m - sum(swings[j] for j in subset) > 1e-12 for subset in itertools.combinations(range(len(swings)), g + 1)):
            return False
    return True


# ------------------------------------------------------------------- bias-aware intervals
def phi(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def coverage(half_width: float, bias: float, n: int, sigma: float = 1.0) -> float:
    t = bias * math.sqrt(n) / sigma
    z = half_width * math.sqrt(n) / sigma
    return phi(z - t) - phi(-z - t)


def shortest_half_width(bias_bound: float, n: int, level: float = 0.95, sigma: float = 1.0) -> float:
    """Shortest half-width with coverage `level` for every bias up to the bound."""
    lo, hi = 0.0, bias_bound + 10 * sigma / math.sqrt(n)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if coverage(mid, bias_bound, n, sigma) < level else (lo, mid)
    return hi


def verify_threshold(bias_bound: float, sigma: float = 1.0, z: float = 1.6448536269514722) -> float:
    """Sample size beyond which the bias bound is the larger part of the half-width."""
    return (z * sigma / bias_bound) ** 2


def run() -> dict:
    # Example 4: margin 0.6 score points, five unresolved fields.
    m, swings, costs, budget = 0.6, (0.9, 0.5, 0.4, 0.3, 0.2), (4, 1, 2, 1, 1), 4
    plan = best_plan(m, swings, costs, budget)
    greedy = greedy_by_density(swings, costs, budget)
    big_first = largest_swing_first(swings, costs, budget)
    # Example 5: misstatement tolerance at margin 1.0, six unresolved fields.
    m2, swings2 = 1.0, (0.4, 0.3, 0.3, 0.2, 0.2, 0.1)
    n = 100
    widened = 0.2 + 1.959963984540054 / math.sqrt(n)
    shortest = shortest_half_width(0.2, n)
    return {
        "closed_form_max_gap": check_closed_form(),
        "example": {
            "total_swing": sum(swings),
            "regret_before": residual_regret(m, swings),
            "single_field_values": [guaranteed_value(m, swings, (j,)) for j in range(5)],
            "pair_fields_2_and_3": guaranteed_value(m, swings, (1, 2)),
            "best_plan_fields": [j + 1 for j in plan[2]],
            "best_plan_regret": plan[0],
            "density_order_fields": [j + 1 for j in greedy],
            "density_order_regret": residual_regret(m, swings, greedy),
            "largest_swing_first_fields": [j + 1 for j in big_first],
            "largest_swing_first_regret": residual_regret(m, swings, big_first),
        },
        "tolerance_example": {
            "box_bound_certifies": sum(swings2) < m2,
            "tolerance": misstatement_tolerance(m2, swings2),
            "check": check_tolerance(m2, swings2),
        },
        "top_k_pairs": {"n": 20, "k": 5, "needed": 5 * 15, "all_pairs": math.comb(20, 2)},
        "bias_aware": {
            "widened_half_width": widened,
            "shortest_half_width": shortest,
            "shortest_coverage": coverage(shortest, 0.2, n),
            "shorter_by": 1 - shortest / widened,
            "verify_threshold_n": verify_threshold(0.2),
        },
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run(), indent=2))
