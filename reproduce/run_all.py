"""Recompute every figure in the article and compare it with the text.

    python reproduce/run_all.py            # full sizes
    python reproduce/run_all.py --quick    # smaller sample sizes for the sampling checks

Writes reproduce/results.md and exits with status 1 if any figure disagrees.
Standard library only (Python 3.12+).
"""

from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import diligence as d  # noqa: E402
import verification_plan as plan  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    q = parser.parse_args().quick
    sections: list[tuple[str, list]] = []
    rows: list = []

    def section(title: str) -> None:
        nonlocal rows
        rows = []
        sections.append((title, rows))

    def check(label, value, article, tol, where, shown=None):
        rows.append((label, value, shown if shown is not None else article, where, abs(value - article) <= tol))

    def check_true(label, ok, where, shown="holds"):
        rows.append((label, None, shown, where, bool(ok)))

    vp = plan.run()
    bias = vp["bias_aware"]

    # ------------------------------------------------------------------ Sections 1 and 6.1
    section("Attribution, common bias and when to stop collecting (Section 1, Example 1)")
    av = d.attribution_vs_verification()
    check("Worst-case score change equals Σ|β_j| d_j, against a search over the vertices", av["worst_case_change"], av["formula"], 1e-12, "§1", shown="equal")
    check_true("The field with the largest attribution has no verification value, and a field with near-zero attribution has the largest",
               av["verification_sensitivity"][0] == 0 and abs(av["attribution"][1]) < 0.05
               and av["verification_sensitivity"][1] == max(av["verification_sensitivity"]), "§1")
    check("Coverage of a nominal 95% interval, bias 0.2, 100 records (%)", round(100 * d.coverage_with_bias(100), 2), 48.40, 1e-9, "§6, Example 1")
    check("Coverage of a nominal 95% interval, bias 0.2, 1,000 records (%)", round(100 * d.coverage_with_bias(1000), 6), 0.000637, 1e-9, "§6, Example 1")
    reps = 50_000 if q else 200_000
    sampled = d.coverage_by_sampling(reps=reps)
    four_se = 4 * (0.484 * 0.516 / reps) ** 0.5 * 100
    check("The same coverage at 100 records by direct sampling (%)", 100 * sampled, 48.40, four_se, "§6, Example 1")
    check_true("Coverage falls as the sample grows under a fixed bias (10 to 10,000 records)",
               all(d.coverage_with_bias(n) > d.coverage_with_bias(n * 10) for n in (10, 100, 1000)), "§1")
    check("Coverage after widening by the verified bound, 100 records (%)", round(100 * d.coverage_with_bias(100, extra_halfwidth=0.2), 2), 97.50, 1e-9, "§6, Example 1")
    check("Widened half-width 0.2 + 1.96/√n at 100 records", bias["widened_half_width"], 0.396, 0.0005, "§6, Example 1")
    check("Bias-aware half-width at 100 records", bias["shortest_half_width"], 0.3645, 0.00005, "§6, Example 1")
    check("Coverage of the bias-aware interval at the bound (%)", 100 * bias["shortest_coverage"], 95, 1e-6, "§6, Example 1")
    check("Bias-aware interval shorter by (%)", 100 * bias["shorter_by"], 8.0, 0.05, "§6, Example 1")
    check("Records past which verification beats collection, n*", bias["verify_threshold_n"], 68, 0.5, "§1, §6")

    # ------------------------------------------------------------------ Section 2
    section("Joint uncertainty over models and evidence (Section 2)")
    rs = d.rashomon_inclusion(reps=1_000 if q else 4_000)
    check_true(f"The best model is retained with frequency {rs['inclusion_rate']:.3f}, at least 1 − α = 0.9", rs["inclusion_rate"] >= 0.9, "§2", shown="≥ 0.9")
    check_true(f"Every retained model is within 4t of the best, frequency {rs['excess_within_4t']:.3f}", rs["excess_within_4t"] >= 0.9, "§2", shown="≥ 0.9")
    check("Certificates needed to select five of twenty companies", vp["top_k_pairs"]["needed"], 75, 0, "§2")
    check("All pairs among twenty companies", vp["top_k_pairs"]["all_pairs"], 190, 0, "§2")

    # ------------------------------------------------------------------ Section 3
    section("Comparison bounds (Section 3, Examples 2 and 5)")
    sh = d.shared_error_example()
    check("Separate company intervals: lower bound on the difference", sh["separate"][0], -1.4, 1e-12, "§6, Example 2")
    check("Separate company intervals: upper bound", sh["separate"][1], 2.6, 1e-12, "§6, Example 2")
    check("Joint bound: lower", sh["joint"][0], 0.6, 1e-12, "§6, Example 2")
    check("Joint bound: upper", sh["joint"][1], 0.6, 1e-12, "§6, Example 2")
    check_true("Support functions of the box and the ellipsoid, against direct search on 2,000 random cases", d.support_functions_exact(), "§3")
    check_true("Taylor bound on 50,000 random points", d.taylor_bound_holds(), "§3")
    swings5 = (0.4, 0.3, 0.3, 0.2, 0.2, 0.1)
    check("Example 5: sum of the six swings", sum(swings5), 1.5, 1e-12, "§6, Example 5")
    check("Example 5: sum of the two largest swings", sum(sorted(swings5, reverse=True)[:2]), 0.7, 1e-12, "§6, Example 5")
    check("Example 5: sum of the three largest swings", sum(sorted(swings5, reverse=True)[:3]), 1.0, 1e-12, "§6, Example 5")
    check_true("Example 5: the box bound does not certify the ranking", not vp["tolerance_example"]["box_bound_certifies"], "§6, Example 5")
    check("Example 5: misstatement tolerance Γ*", vp["tolerance_example"]["tolerance"], 2, 0, "§6, Example 5")
    check_true("Γ* agrees with a search over every subset of misstated fields", vp["tolerance_example"]["check"], "§3")

    # ------------------------------------------------------------------ Section 4
    section("Verification by the regret it removes (Section 4, Examples 3 and 4)")
    qv = d.query_values()
    check("Example 3: worst-case regret before any query", qv["baseline_regret"], 0.61, 1e-12, "§6, Example 3")
    for key, label, value in (("recheck_verified_high_shap_field", "recheck the verified field with a large attribution", 0.0),
                              ("verify_z2", "verify the smaller unresolved variable", 0.0),
                              ("verify_z1", "verify the variable that sets the sign", 0.61)):
        check(f"Example 3: guaranteed regret reduction, {label}", qv[key]["value"], value, 1e-12, "§6 table")
        check(f"Example 3: regret remaining, {label}", qv[key]["remaining_regret"], 0.61 - value, 1e-12, "§6 table")
    check("Closed form for the remaining regret against an exact search, largest gap on 300 random instances", vp["closed_form_max_gap"], 0, 1e-9, "§4", shown="0")
    ex = vp["example"]
    check("Example 4: total swing", ex["total_swing"], 2.3, 1e-9, "§6, Example 4")
    check("Example 4: worst-case regret before verification", ex["regret_before"], 1.7, 1e-9, "§6, Example 4")
    check("Example 4: guaranteed value of the first field alone", ex["single_field_values"][0], 0.3, 1e-9, "§6, Example 4")
    check("Example 4: largest guaranteed value of any other single field", max(ex["single_field_values"][1:]), 0, 1e-12, "§6, Example 4")
    check("Example 4: guaranteed value of the second and third fields together", ex["pair_fields_2_and_3"], 0.3, 1e-9, "§6, Example 4")
    check_true(f"Example 4: largest swing first verifies field {ex['largest_swing_first_fields']}", ex["largest_swing_first_fields"] == [1], "§6 table", shown="field 1")
    check("Example 4: regret remaining, largest swing first", ex["largest_swing_first_regret"], 1.4, 1e-9, "§6 table")
    check_true(f"Example 4: swing per hour verifies fields {ex['density_order_fields']}", ex["density_order_fields"] == [2, 3, 4], "§6 table", shown="fields 2, 3, 4")
    check("Example 4: regret remaining, swing per hour", ex["density_order_regret"], 1.1, 1e-9, "§6 table")
    check_true("Example 4: the swing-per-hour plan is the optimum over all plans within the budget", ex["best_plan_fields"] == ex["density_order_fields"] and abs(ex["best_plan_regret"] - ex["density_order_regret"]) < 1e-12, "§6, Example 4")
    check("Example 4: regret left by the plan against largest swing first (% less)", 100 * (1 - ex["density_order_regret"] / ex["largest_swing_first_regret"]), 21, 0.5, "§6, Example 4")

    # ------------------------------------------------------------------ Section 5
    section("Propagating corrections (Section 5)")
    check_true("Attribution changes add up to the score change for a nonlinear score, 500 exact cases", d.shapley_efficiency_holds(), "§5")

    total = sum(len(r) for _, r in sections)
    failed = sum(1 for _, r in sections for row in r if not row[4])

    def fmt(x):
        if x is None:
            return ""
        if isinstance(x, float):
            if x != 0 and abs(x) < 1e-9:
                return "0.0000"
            return f"{x:.6f}".rstrip("0").rstrip(".") if abs(x) < 0.001 else f"{x:.4f}"
        return f"{x:,}" if isinstance(x, int) else str(x)

    def art(x):
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            return str(x)
        return format(x, ",.10g")

    lines = [
        "# Results",
        "",
        "Every figure in the article, recomputed from the stated inputs of each worked example.",
        "",
        f"{total - failed} of {total} figures agree with the article" + (" · quick run" if q else ""),
    ]
    for title, section_rows in sections:
        lines += ["", f"## {title}", "", "| Quantity | Recomputed | Article | Where | Agrees |", "| --- | ---: | ---: | --- | :---: |"]
        for label, value, shown, where, ok in section_rows:
            lines.append(f"| {label.replace(chr(124), chr(92) + chr(124))} | {fmt(value)} | {art(shown)} | {where} | {'✓' if ok else '✗'} |")
    report = "\n".join(lines) + "\n"
    (HERE / "results.md").write_text(report, encoding="utf-8", newline="\n")
    sys.stdout.reconfigure(encoding="utf-8")
    print(report)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
