# Results

Every figure in the article, recomputed from the stated inputs of each worked example.

48 of 48 figures agree with the article

## Attribution, common bias and when to stop collecting (Section 1, Example 1)

| Quantity | Recomputed | Article | Where | Agrees |
| --- | ---: | ---: | --- | :---: |
| Worst-case score change equals Σ\|β_j\| d_j, against a search over the vertices | 1.2500 | equal | §1 | ✓ |
| The field with the largest attribution has no verification value, and a field with near-zero attribution has the largest |  | holds | §1 | ✓ |
| Coverage of a nominal 95% interval, bias 0.2, 100 records (%) | 48.4000 | 48.4 | §6, Example 1 | ✓ |
| Coverage of a nominal 95% interval, bias 0.2, 1,000 records (%) | 0.000637 | 0.000637 | §6, Example 1 | ✓ |
| The same coverage at 100 records by direct sampling (%) | 48.5575 | 48.4 | §6, Example 1 | ✓ |
| Coverage falls as the sample grows under a fixed bias (10 to 10,000 records) |  | holds | §1 | ✓ |
| Coverage after widening by the verified bound, 100 records (%) | 97.5000 | 97.5 | §6, Example 1 | ✓ |
| Widened half-width 0.2 + 1.96/√n at 100 records | 0.3960 | 0.396 | §6, Example 1 | ✓ |
| Bias-aware half-width at 100 records | 0.3645 | 0.3645 | §6, Example 1 | ✓ |
| Coverage of the bias-aware interval at the bound (%) | 95.0000 | 95 | §6, Example 1 | ✓ |
| Bias-aware interval shorter by (%) | 7.9574 | 8 | §6, Example 1 | ✓ |
| Records past which verification beats collection, n* | 67.6386 | 68 | §1, §6 | ✓ |

## Joint uncertainty over models and evidence (Section 2)

| Quantity | Recomputed | Article | Where | Agrees |
| --- | ---: | ---: | --- | :---: |
| The best model is retained with frequency 1.000, at least 1 − α = 0.9 |  | ≥ 0.9 | §2 | ✓ |
| Every retained model is within 4t of the best, frequency 1.000 |  | ≥ 0.9 | §2 | ✓ |
| Certificates needed to select five of twenty companies | 75 | 75 | §2 | ✓ |
| All pairs among twenty companies | 190 | 190 | §2 | ✓ |

## Comparison bounds (Section 3, Examples 2 and 5)

| Quantity | Recomputed | Article | Where | Agrees |
| --- | ---: | ---: | --- | :---: |
| Separate company intervals: lower bound on the difference | -1.4000 | -1.4 | §6, Example 2 | ✓ |
| Separate company intervals: upper bound | 2.6000 | 2.6 | §6, Example 2 | ✓ |
| Joint bound: lower | 0.6000 | 0.6 | §6, Example 2 | ✓ |
| Joint bound: upper | 0.6000 | 0.6 | §6, Example 2 | ✓ |
| Support functions of the box and the ellipsoid, against direct search on 2,000 random cases |  | holds | §3 | ✓ |
| Taylor bound on 50,000 random points |  | holds | §3 | ✓ |
| Example 5: sum of the six swings | 1.5000 | 1.5 | §6, Example 5 | ✓ |
| Example 5: sum of the two largest swings | 0.7000 | 0.7 | §6, Example 5 | ✓ |
| Example 5: sum of the three largest swings | 1.0000 | 1 | §6, Example 5 | ✓ |
| Example 5: the box bound does not certify the ranking |  | holds | §6, Example 5 | ✓ |
| Example 5: misstatement tolerance Γ* | 2 | 2 | §6, Example 5 | ✓ |
| Γ* agrees with a search over every subset of misstated fields |  | holds | §3 | ✓ |

## Verification by the regret it removes (Section 4, Examples 3 and 4)

| Quantity | Recomputed | Article | Where | Agrees |
| --- | ---: | ---: | --- | :---: |
| Example 3: worst-case regret before any query | 0.6100 | 0.61 | §6, Example 3 | ✓ |
| Example 3: guaranteed regret reduction, recheck the verified field with a large attribution | 0 | 0 | §6 table | ✓ |
| Example 3: regret remaining, recheck the verified field with a large attribution | 0.6100 | 0.61 | §6 table | ✓ |
| Example 3: guaranteed regret reduction, verify the smaller unresolved variable | 0 | 0 | §6 table | ✓ |
| Example 3: regret remaining, verify the smaller unresolved variable | 0.6100 | 0.61 | §6 table | ✓ |
| Example 3: guaranteed regret reduction, verify the variable that sets the sign | 0.6100 | 0.61 | §6 table | ✓ |
| Example 3: regret remaining, verify the variable that sets the sign | 0 | 0 | §6 table | ✓ |
| Closed form for the remaining regret against an exact search, largest gap on 300 random instances | 0.0000 | 0 | §4 | ✓ |
| Example 4: total swing | 2.3000 | 2.3 | §6, Example 4 | ✓ |
| Example 4: worst-case regret before verification | 1.7000 | 1.7 | §6, Example 4 | ✓ |
| Example 4: guaranteed value of the first field alone | 0.3000 | 0.3 | §6, Example 4 | ✓ |
| Example 4: largest guaranteed value of any other single field | 0 | 0 | §6, Example 4 | ✓ |
| Example 4: guaranteed value of the second and third fields together | 0.3000 | 0.3 | §6, Example 4 | ✓ |
| Example 4: largest swing first verifies field [1] |  | field 1 | §6 table | ✓ |
| Example 4: regret remaining, largest swing first | 1.4000 | 1.4 | §6 table | ✓ |
| Example 4: swing per hour verifies fields [2, 3, 4] |  | fields 2, 3, 4 | §6 table | ✓ |
| Example 4: regret remaining, swing per hour | 1.1000 | 1.1 | §6 table | ✓ |
| Example 4: the swing-per-hour plan is the optimum over all plans within the budget |  | holds | §6, Example 4 | ✓ |
| Example 4: regret left by the plan against largest swing first (% less) | 21.4286 | 21 | §6, Example 4 | ✓ |

## Propagating corrections (Section 5)

| Quantity | Recomputed | Article | Where | Agrees |
| --- | ---: | ---: | --- | :---: |
| Attribution changes add up to the score change for a nonlinear score, 500 exact cases |  | holds | §5 | ✓ |
