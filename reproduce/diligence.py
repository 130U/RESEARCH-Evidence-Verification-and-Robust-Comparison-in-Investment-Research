"""Sections 1-6: evidence uncertainty, robust comparison and the value of verification.

1. Interval coverage under a common reporting bias, and the widened interval after verification.
2. Attribution magnitude vs verification value for a linear score.
3. Shared-error cancellation: separate company intervals vs the joint support-function bound.
4. Minimax-regret query selection on the eight-scenario example.
5. The empirical Rashomon set: Hoeffding + union bound keeps the best model with prob >= 1 - alpha.
6. Taylor bound for a smooth nonlinear score difference.
7. Shapley efficiency: attribution changes add up to the score change.
"""

from __future__ import annotations

import itertools
import math
import random
from statistics import NormalDist

N01 = NormalDist()
Z975 = N01.inv_cdf(0.975)


# ------------------------------------------------------------------ 1. coverage under common bias


def coverage_with_bias(n, b=0.2, sigma=1.0, extra_halfwidth=0.0):
    """P{ mu in [Xbar - h, Xbar + h] } with Xbar ~ N(mu + b, sigma^2 / n), h = z sigma/sqrt(n) + extra."""
    se = sigma / math.sqrt(n)
    h = Z975 * se + extra_halfwidth
    # mu in interval  <=>  |Xbar - mu| <= h  <=>  -h <= b + eps <= h with eps ~ N(0, se^2)
    return N01.cdf((h - b) / se) - N01.cdf((-h - b) / se)


def coverage_by_sampling(n=100, b=0.2, sigma=1.0, reps=200_000, seed=13, extra=0.0):
    rng = random.Random(seed)
    se = sigma / math.sqrt(n)
    h = Z975 * se + extra
    hits = 0
    for _ in range(reps):
        xbar = b + rng.gauss(0.0, se)   # mu = 0 without loss of generality
        hits += abs(xbar) <= h
    return hits / reps


# ------------------------------------------------------------------ 2. attribution vs verification value


def attribution_vs_verification():
    """Linear score f(x) = sum beta_j x_j with a background mean. Feature 0 is audited (d = 0) with a
    large attribution; feature 1 is self-reported near the sector mean (attribution ~ 0) with a
    wide unresolved error band."""
    beta = (1.5, 2.0, 0.5)
    x = (3.0, 1.02, 0.4)
    background_mean = (1.0, 1.0, 0.5)
    d = (0.0, 0.6, 0.1)
    phi = [bj * (xj - mj) for bj, xj, mj in zip(beta, x, background_mean)]
    sensitivity = [abs(bj) * dj for bj, dj in zip(beta, d)]
    worst = max(abs(sum(bj * sj * dj for bj, sj, dj in zip(beta, signs, d)))
                for signs in itertools.product((-1, 1), repeat=3))
    return {"attribution": phi, "verification_sensitivity": sensitivity,
            "worst_case_change": worst, "formula": sum(sensitivity)}


# ------------------------------------------------------------------ 3. joint vs separate bounds


def shared_error_example(nominal_gap=0.6, shared_halfwidth=1.0):
    """Both companies load identically on one shared benchmark error u in [-1, 1]."""
    separate = (nominal_gap - 2 * shared_halfwidth, nominal_gap + 2 * shared_halfwidth)
    # joint: Delta(u) = m + a u with a = (B_i - B_k)^T beta = 0
    a = 1.0 - 1.0
    joint = (nominal_gap - shared_halfwidth * abs(a), nominal_gap + shared_halfwidth * abs(a))
    return {"separate": separate, "joint": joint}


def support_function_box(a, halfwidths):
    return sum(abs(ai) * hi for ai, hi in zip(a, halfwidths))


def support_function_ellipsoid(a, C, r):
    ct_a = [sum(C[i][j] * a[i] for i in range(len(a))) for j in range(len(C[0]))]
    return r * math.sqrt(sum(v * v for v in ct_a))


def support_functions_exact(trials=2_000, seed=14):
    """Box: compare with vertex enumeration. Ellipsoid: no sampled point exceeds h_U, and the
    maximizer z = r C^T a / ||C^T a|| attains it."""
    rng = random.Random(seed)
    for _ in range(trials):
        k = rng.randint(1, 4)
        a = [rng.uniform(-2, 2) for _ in range(k)]
        hw = [rng.uniform(0, 1) for _ in range(k)]
        best = max(sum(ai * si * hi for ai, si, hi in zip(a, s, hw)) for s in itertools.product((-1, 1), repeat=k))
        if abs(best - support_function_box(a, hw)) > 1e-12:
            return False
        C = [[rng.uniform(-1, 1) for _ in range(k)] for _ in range(k)]
        r = rng.uniform(0.1, 2)
        h = support_function_ellipsoid(a, C, r)
        ct_a = [sum(C[i][j] * a[i] for i in range(k)) for j in range(k)]
        norm = math.sqrt(sum(v * v for v in ct_a))
        if norm > 0:
            z = [r * v / norm for v in ct_a]
            u = [sum(C[i][j] * z[j] for j in range(k)) for i in range(k)]
            if abs(sum(ai * ui for ai, ui in zip(a, u)) - h) > 1e-9:
                return False
        for _ in range(20):
            z = [rng.gauss(0, 1) for _ in range(k)]
            zn = math.sqrt(sum(v * v for v in z)) or 1.0
            z = [r * v / zn * rng.random() for v in z]
            u = [sum(C[i][j] * z[j] for j in range(k)) for i in range(k)]
            if sum(ai * ui for ai, ui in zip(a, u)) > h + 1e-9:
                return False
    return True


# ------------------------------------------------------------------ 4. minimax regret


SCENARIOS = [(theta, z1, z2) for theta in (-1, 1) for z1 in (-0.4, 0.4) for z2 in (-0.2, 0.2)]


def score_gap(theta, z1, z2):
    """Example 3: Delta_theta = 0.15 theta + z1 + 0.3 theta z2, with theta indexing the two Rashomon models."""
    return 0.15 * theta + z1 + 0.3 * theta * z2


def minimax_regret(scenarios):
    """Actions: select company i (utility Delta) or company k (utility 0). Regret in score units."""
    def worst(action):
        return max(max(0.0, -score_gap(*w)) if action == "i" else max(0.0, score_gap(*w)) for w in scenarios)
    return min(worst("i"), worst("k"))


def query_values():
    base = minimax_regret(SCENARIOS)
    queries = {
        "recheck_verified_high_shap_field": lambda w: 0,   # already verified: the answer is known
        "verify_z2": lambda w: w[2],
        "verify_z1": lambda w: w[1],
    }
    out = {"baseline_regret": base}
    for name, observe in queries.items():
        outcomes = {observe(w) for w in SCENARIOS}
        remaining = max(minimax_regret([w for w in SCENARIOS if observe(w) == o]) for o in outcomes)
        out[name] = {"remaining_regret": remaining, "value": base - remaining}
    return out


# ------------------------------------------------------------------ 5. empirical Rashomon set


def rashomon_inclusion(models=20, n=500, alpha=0.1, reps=4_000, seed=15):
    """Bernoulli losses with true means spread in [0.2, 0.4]; the best model must be retained."""
    rng = random.Random(seed)
    t_n = math.sqrt(math.log(2 * models / alpha) / (2 * n))
    true = [0.2 + 0.2 * j / (models - 1) for j in range(models)]
    best = min(range(models), key=lambda j: true[j])
    kept = 0
    excess_ok = 0
    for _ in range(reps):
        emp = [rng.binomialvariate(n, p) / n for p in true]
        cut = min(emp) + 2 * t_n
        retained = [j for j in range(models) if emp[j] <= cut]
        kept += best in retained
        excess_ok += all(true[j] - true[best] <= 4 * t_n for j in retained)
    return {"t_n": t_n, "inclusion_rate": kept / reps, "target": 1 - alpha, "excess_within_4t": excess_ok / reps}


# ------------------------------------------------------------------ 6. Taylor bound


def taylor_bound_holds(trials=50_000, seed=16):
    """Delta(u) = m + a.u + 0.25 cos(u1 + u2) - 0.25. Its Hessian is -0.25 cos(u1 + u2) [[1, 1], [1, 1]],
    with operator norm at most 0.5 =: K everywhere; Delta(0) = m and grad Delta(0) = a, so the
    bound |Delta(u) - m - a.u| <= K r^2 / 2 must hold on the ball of radius r."""
    rng = random.Random(seed)
    m, a, K = 0.3, (0.5, -0.2), 0.5
    def delta(u):
        return m + a[0] * u[0] + a[1] * u[1] + 0.25 * math.cos(u[0] + u[1]) - 0.25
    # gradient at 0 of the cosine term is 0, so the linearization at 0 is m + a.u
    for _ in range(trials):
        r = rng.uniform(0.01, 2.0)
        ang = rng.uniform(0, 2 * math.pi)
        rad = r * math.sqrt(rng.random())
        u = (rad * math.cos(ang), rad * math.sin(ang))
        if abs(delta(u) - m - a[0] * u[0] - a[1] * u[1]) > 0.5 * K * r * r + 1e-12:
            return False
    return True


# ------------------------------------------------------------------ 7. Shapley efficiency


def shapley(f, x, background):
    """Exact interventional Shapley values with a single background point (3 features)."""
    d = len(x)
    phi = [0.0] * d
    for j in range(d):
        others = [k for k in range(d) if k != j]
        for size in range(d):
            for subset in itertools.combinations(others, size):
                w = math.factorial(size) * math.factorial(d - size - 1) / math.factorial(d)
                with_j = [x[k] if (k in subset or k == j) else background[k] for k in range(d)]
                without = [x[k] if k in subset else background[k] for k in range(d)]
                phi[j] += w * (f(with_j) - f(without))
    return phi


def shapley_efficiency_holds(trials=500, seed=17):
    rng = random.Random(seed)
    def f(v):
        return 1.2 * v[0] + max(0.0, v[1] - 0.5) * 2.0 + 0.7 * v[0] * v[2]   # threshold and interaction
    for _ in range(trials):
        bg = [rng.uniform(0, 1) for _ in range(3)]
        x = [rng.uniform(0, 2) for _ in range(3)]
        x2 = [v + rng.uniform(-0.5, 0.5) for v in x]
        p1, p2 = shapley(f, x, bg), shapley(f, x2, bg)
        if abs(sum(p2) - sum(p1) - (f(x2) - f(x))) > 1e-9:
            return False
        if abs(f(bg) + sum(p1) - f(x)) > 1e-9:
            return False
    return True


if __name__ == "__main__":
    import json

    print(json.dumps({
        "coverage": {"n100": coverage_with_bias(100), "n1000": coverage_with_bias(1000),
                     "widened_n100": coverage_with_bias(100, extra_halfwidth=0.2)},
        "attribution": attribution_vs_verification(),
        "shared": shared_error_example(),
        "support": support_functions_exact(200),
        "regret": query_values(),
        "rashomon": rashomon_inclusion(reps=500),
        "taylor": taylor_bound_holds(5_000),
        "shapley": shapley_efficiency_holds(50),
    }, indent=2))
