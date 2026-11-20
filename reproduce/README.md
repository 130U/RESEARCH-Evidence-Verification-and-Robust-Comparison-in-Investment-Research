# Reproduce

```bash
python reproduce/run_all.py           # every figure in the article, a few seconds
python reproduce/run_all.py --quick   # smaller sample sizes for the sampling checks
```

Python 3.12 or later, standard library only. `run_all.py` recomputes every figure in the article from the stated
inputs of each worked example, compares each with the text, writes [`results.md`](results.md) and exits with
status 1 if any figure disagrees. The same command runs on every push.

| Script | Article | What it computes |
| --- | --- | --- |
| [`diligence.py`](diligence.py) | §1 to §5, Examples 1 to 3 | Interval coverage under a common bias, in closed form and by direct sampling; attribution magnitude against verification value for a linear score; the shared-error example; support functions of the box and the ellipsoid against direct search; the Taylor bound; minimax-regret query values on the eight-scenario example; retention of the best model in the empirical Rashomon set; Shapley efficiency on exact attributions |
| [`verification_plan.py`](verification_plan.py) | §1 to §4, Examples 1, 4 and 5 | The closed form for the regret that remains after verifying a set of fields, checked against an exact search; the pivot rule and complementarity; the best plan within a budget by exhaustive search, by swing per hour and by largest swing first; misstatement tolerance, checked over every subset of fields; the bias-aware half-width and the threshold $`n^*`$; the number of certificates a selection needs |

**Exact search behind the closed form.** For a set of verified fields the worst observation is found by a search
over the revealed margin, which is one-dimensional because the remaining regret depends on the verified values
only through their sum. The closed form and the search agree to rounding error on 300 random instances.

**Exact attributions.** Shapley values are computed by enumerating every coalition, so the efficiency identity of
Section 5 is checked with no sampling error.
