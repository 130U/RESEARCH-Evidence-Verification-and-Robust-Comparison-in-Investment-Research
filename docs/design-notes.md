# Design notes

Why each piece of the design is the way it is, what it was chosen over, and what the diligence workflow has to
supply for the guarantees to hold. Proofs are in [derivations](derivations.md); figures are recomputed in
[results](../reproduce/results.md).

## Choices and the alternatives they beat

| Choice | Alternative | Why | When I would switch |
| --- | --- | --- | --- |
| **Verify by swing against the margin** | Verify the fields with the largest attributions | Attribution measures where a feature sits relative to the background; verification value depends on how much unresolved error it carries ([D1](derivations.md#d1-attribution-magnitude-is-not-verification-value)). A field has guaranteed value only when its swing exceeds the margin ([D9](derivations.md#d9-the-exact-plan-for-affine-scores)) | No case: attribution stays in the workflow as explanation, not as a work list |
| **One joint evidence state for all companies** | An interval per company, subtracted | A shared source cancels exactly in a pairwise comparison; separate intervals count it twice ([D5](derivations.md#d5-support-functions-and-the-cancellation-of-shared-errors)) | Companies with no common sources, where the two coincide |
| **Set-based evidence, no prior** | A probability that each disclosure is exaggerated | Nobody can defend such a probability to an investment committee, and the guarantees do not need it ([D8](derivations.md#d8-the-value-of-a-query-is-nonnegative)) | A field with a calibrated error history, which narrows its interval |
| **A set of near-optimal models** | The single best model | The certificate holds for every retained model, and the best model of the class is retained with probability $`1 - \alpha`$ ([D3](derivations.md#d3-the-empirical-rashomon-set-keeps-the-best-model)) | No case |
| **A certified partial order** | A full ranking with a score per company | One inclusion event certifies every pair, nothing is paid for the number of comparisons, and verification can only extend the order ([D4](derivations.md#d4-one-event-certifies-every-pair)) | No case |
| **Misstatement tolerance as the reported number** | The width of an interval | "This ranking holds against any two unverified fields being wrong at once" is a sentence a committee can act on ([D6](derivations.md#d6-misstatement-tolerance)) | No case |
| **A plan over sets of fields** | Score one query at a time | Fields that are worthless alone are valuable together, and the best plan is a knapsack on swing per analyst hour | A single remaining field |
| **A verified field keeps part of its allowance** | Treat a checked field as exact | Assurance differs by source, and an auditor paid by the audited party reports favorably; the swing removed is $`(1-\lambda_j)s_j`$ | Primary documents, where $`\lambda_j = 0`$ |
| **A bias-aware interval after verification** | A wider sample | Past $`n^*`$ records the bias bound is the larger part of the half-width ([D2](derivations.md#d2-common-bias-the-bias-aware-interval-and-when-to-stop-collecting)) | Below $`n^*`$, where collection still pays |
| **Versioned recomputation with an efficiency check** | Recompute explanations on demand | A change caused by a factual correction is told apart from one caused by a model or background update ([D10](derivations.md#d10-corrections-propagate-through-attributions)) | No case |

## What the committee receives

| Output | Meaning | Where it comes from |
| --- | --- | --- |
| The certified partial order | Every pairwise ranking that holds whatever the unverified evidence turns out to be, across every retained model | $`\underline\Delta_{ik} > 0`$ |
| A tolerance per ranking | The number of simultaneous worst-case misstatements the ranking survives | $`\Gamma^*_{ik}`$ |
| The verification plan | The fields to check with the analyst hours available, and the regret that remains | The knapsack on $`(1-\lambda_j)s_j/c_j`$ |
| The share of pairs certified | Progress of the diligence, per analyst hour | The partial order before and after |

## Assurance tiers

A check narrows an allowance and seldom removes it. The fraction $`\lambda_j`$ of the half-width that survives a
check is set by the standing of the source.

| Source after the check | What remains of the allowance |
| --- | --- |
| Self-reported, restated by management | Most of it |
| Limited assurance | A reduced allowance |
| Reasonable assurance | A small allowance |
| Primary document: contract, utility bill, regulatory filing | None |

## What the guarantees need from the workflow

1. **Models fixed before validation.** The candidate set $`ℱ_0`$, the prediction target, the input
   definitions and the output scale are specified before the validation data is examined.
2. **A calibrated evidence set.** $`𝒳(E)`$ contains the true inputs with probability at least
   $`1 - \beta`$ at the certification stage, and for certification repeated over stages $`\beta`$ is calibrated
   jointly.
3. **Shared sources modeled as shared.** A sector benchmark or a vendor estimate used by several companies is one
   coordinate of $`u`$ with a loading per company, never an independent error per company.
4. **Identifiers on every update.** Field version, evidence document, model version, background and rubric
   version are recorded with each change.
5. **A plan the scored companies cannot anticipate.** The plan stays inside the diligence team and is combined
   with a share of checks drawn at random.

## What to monitor

- **Share of company pairs certified**, before and after each round of verification.
- **Pairs near the boundary.** Computation is spent first on pairs whose bounds are close to zero.
- **Efficiency residuals** of approximate attributions against the bound $`\eta + \eta'`$.
- **Realized corrections against allowances.** A correction larger than its field's half-width means the
  allowance for that source was set too tight.

## Extensions

1. **Tree ensembles at scale.** Exact bounds for large ensembles through leaf-region partitioning or
   mixed-integer programming, with anytime bounds for pairs far from the boundary.
2. **Plans over several rounds.** The closed form covers one round of verification. A plan that adapts to each
   answer is the sequential version of the same knapsack.
3. **Shortlists.** A certified top-$`K`$ of $`N`$ companies needs $`K(N-K)`$ certificates; the next step is the smallest set of
   fields whose verification completes them.
