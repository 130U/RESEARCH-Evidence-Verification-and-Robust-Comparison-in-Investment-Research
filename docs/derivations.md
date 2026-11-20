# Derivations

Full proofs of the article's results, in its notation. Section numbers (§) refer to the
[article](../manuscript/evidence-verification-and-robust-comparison-in-investment-research.md); every figure
quoted here is recomputed in [results](../reproduce/results.md).

| | Result | Section |
| --- | --- | --- |
| [D1](#d1-attribution-magnitude-is-not-verification-value) | Attribution magnitude is not verification value | §1 |
| [D2](#d2-common-bias-the-bias-aware-interval-and-when-to-stop-collecting) | Common bias, the bias-aware interval and when to stop collecting | §1 |
| [D3](#d3-the-empirical-rashomon-set-keeps-the-best-model) | The empirical Rashomon set keeps the best model | §2 |
| [D4](#d4-one-event-certifies-every-pair) | One event certifies every pair | §2 |
| [D5](#d5-support-functions-and-the-cancellation-of-shared-errors) | Support functions and the cancellation of shared errors | §3 |
| [D6](#d6-misstatement-tolerance) | Misstatement tolerance | §3 |
| [D7](#d7-smooth-nonlinear-scores) | Smooth nonlinear scores | §3 |
| [D8](#d8-the-value-of-a-query-is-nonnegative) | The value of a query is nonnegative | §4 |
| [D9](#d9-the-exact-plan-for-affine-scores) | The exact plan for affine scores | §4 |
| [D10](#d10-corrections-propagate-through-attributions) | Corrections propagate through attributions | §5 |

---

## D1. Attribution magnitude is not verification value

For a linear score $`f(x) = \beta_0 + \sum_j \beta_j x_j`$ and a fixed marginal background $`Q`$, the Shapley value
of feature $`j`$ is $`\phi_j = \beta_j(x_j - E_Q X_j)`$: every coalition gains exactly that amount when $`j`$
joins. If the feature's factual error satisfies $`\left\vert\delta_j\right\vert \le d_j`$, then

```math
\sup_{\left\vert\delta_j\right\vert\le d_j}\left\vert f(x+\delta) - f(x)\right\vert = \sup\Big|\sum_j\beta_j\delta_j\Big| = \sum_j\left\vert\beta_j\right\vert d_j , \qquad (D1.1)
```

with the upper bound from the triangle inequality, attained at $`\delta_j = \mathrm{sign}(\beta_j)d_j`$. ∎
$`\phi_j`$ depends on where $`x_j`$ sits relative to the background, and $`\left\vert\beta_j\right\vert d_j`$ depends on how wide the
unresolved error is. An audited field with a large attribution has $`d_j = 0`$ and no verification value. A
self-reported field at the sector mean has $`\phi_j \approx 0`$ and can have the most.

## D2. Common bias, the bias-aware interval and when to stop collecting

**Coverage under a common bias.** With $`X_i = \mu + b + \varepsilon_i`$,
$`\bar X \sim 𝒩(\mu + b, \sigma^2/n)`$, and

```math
P\{\left\vert\bar X - \mu\right\vert \le z\sigma/\sqrt n\} = \Phi\big(z - b\sqrt n/\sigma\big) - \Phi\big(-z - b\sqrt n/\sigma\big) \to 0 \quad (n\to\infty,\ b\ne 0). \quad ∎ \qquad (D2.1)
```

The bootstrap resamples the same biased records, so its distribution is centered at $`\mu + b`$ too. At
$`b = 0.2`$ and $`\sigma = 1`$ the coverage is 48.40% at $`n = 100`$ and 0.000637% at $`n = 1{,}000`$.

**The widened interval.** If verification establishes $`\left\vert b\right\vert \le \bar b`$, the interval
$`\bar X \pm (\bar b + z\sigma/\sqrt n)`$ covers $`\mu`$ with probability at least 95% for every admissible bias:
for every such $`b`$ the event $`\left\vert\bar\varepsilon\right\vert \le z\sigma/\sqrt n`$ implies coverage. At $`b = \bar b = 0.2`$ and
$`n = 100`$ its coverage is 97.50%, more than was asked for.

**The shortest valid interval.** For a symmetric interval $`\bar X \pm c`$, the coverage
$`P(\left\vert 𝒩(b\sqrt n/\sigma, 1)\right\vert \le c\sqrt n/\sigma)`$ is decreasing in $`\left\vert b\right\vert`$, so the worst admissible bias
is $`\left\vert b\right\vert = \bar b`$ and the shortest interval with 95% coverage for every $`\left\vert b\right\vert \le \bar b`$ has

```math
c = \mathrm{cv}_{0.95}\!\Big(\frac{\bar b\sqrt n}{\sigma}\Big)\frac{\sigma}{\sqrt n}, \qquad
\mathrm{cv}_{0.95}(t) = \text{the 95\% quantile of } \left\vert 𝒩(t,1)\right\vert . \qquad (D2.2)
```

For large $`t`$ the lower tail of $`\left\vert 𝒩(t,1)\right\vert`$ is negligible and $`\mathrm{cv}_{0.95}(t) \approx t + 1.645`$,
so $`c \approx \bar b + 1.645\,\sigma/\sqrt n`$. ∎ At $`\bar b = 0.2`$ and $`n = 100`$, $`c = 0.3645`$ against
$`0.396`$ for the widened interval, 8.0% shorter at exactly 95%.

**When to stop collecting.** The half-width has a bias part $`\bar b`$ and a sampling part
$`1.645\,\sigma/\sqrt n`$. The bias part is the larger one when $`n > n^* = (1.645\,\sigma/\bar b)^2`$. Past that
point halving the bound removes $`\bar b/2`$, at least half the sampling part, while doubling the sample removes
$`1 - 1/\sqrt2`$ of it, less than a third. At $`\bar b = 0.2`$ and $`\sigma = 1`$, $`n^* \approx 68`$.

## D3. The empirical Rashomon set keeps the best model

Hoeffding's inequality gives $`P(\left\vert\hat L_n(f) - L(f)\right\vert > t) \le 2e^{-2nt^2}`$ for losses in $`[0,1]`$, and a union
bound over $`M`$ models with $`t_n = \sqrt{\log(2M/\alpha)/(2n)}`$ makes all deviations at most $`t_n`$ with
probability at least $`1 - \alpha`$. On that event:

- $`\hat L_n(f^*) \le L(f^*) + t_n \le L(g) + t_n \le \hat L_n(g) + 2t_n`$ for every $`g`$, so
  $`f^* \in ℱ_\alpha`$;
- for any retained $`f`$:
  $`L(f) \le \hat L_n(f) + t_n \le \min_g\hat L_n(g) + 3t_n \le \hat L_n(f^*) + 3t_n \le L(f^*) + 4t_n`$. ∎

The models are specified before the validation data is examined, which is what lets the union bound cover them.

## D4. One event certifies every pair

If $`\underline\Delta_{ik} = \inf_{(f,X)\in\Omega(E)}[f(x_i) - f(x_k)] > 0`$, the ordering $`i \succ k`$ holds for
every retained model and every admissible resolution of the evidence, by definition of the infimum. Let
$`ℰ`$ be the event that $`f^* \in ℱ_\alpha`$ and the true inputs lie in $`𝒳(E)`$. By
D3 and the calibration of $`𝒳(E)`$, a union bound gives $`P(ℰ) \ge 1 - \alpha - \beta`$, with
no independence required between the two.

**Simultaneity.** On $`ℰ`$ the pair $`(f^*, X_{\text{true}})`$ is a point of $`\Omega(E)`$, so for every
pair with $`\underline\Delta_{ik} > 0`$ at once, $`f^*(x_i) - f^*(x_k) \ge \underline\Delta_{ik} > 0`$. All
certified orderings are correct together with probability at least $`1 - \alpha - \beta`$, whatever the number of
pairs. ∎

**Monotonicity.** If verification replaces $`E`$ by $`E'`$ with $`𝒳(E') \subseteq 𝒳(E)`$, each
infimum is taken over a smaller set and cannot fall. Certified pairs stay certified and the partial order can only
grow.

**Selection.** Choosing $`K`$ of $`N`$ companies is justified by the $`K(N-K)`$ certificates that place each
selected company above each rejected one: 75 for five of twenty, against 190 pairs in all.

## D5. Support functions and the cancellation of shared errors

For an affine score, $`\Delta_f(u) = m_f + a_f^\top u`$ with $`a_f = (B_i - B_k)^\top\beta_f`$. Then
$`\sup_{u\in U}\Delta_f(u) = m_f + h_U(a_f)`$ and $`\inf_{u\in U}\Delta_f(u) = m_f - h_U(-a_f)`$ by the definition
$`h_U(a) = \sup_{u\in U}a^\top u`$.

- **Ellipsoid.** For $`U = \{Cz : \|z\|_2 \le r\}`$, $`a^\top Cz = (C^\top a)^\top z \le r\|C^\top a\|_2`$ by
  Cauchy-Schwarz, attained at $`z = rC^\top a/\|C^\top a\|_2`$.
- **Box.** For $`\left\vert u_j\right\vert \le d_j`$, $`a^\top u \le \sum_j\left\vert a_j\right\vert d_j`$, attained at
  $`u_j = \mathrm{sign}(a_j)d_j`$. ∎

**Cancellation.** If the two companies load identically on the coordinates in $`S`$, then
$`(B_i - B_k)_{:,S} = 0`$ and $`(a_f)_S = 0`$: those coordinates do not appear in $`\Delta_f`$ at all. Subtracting
intervals built separately for each company lets a shared source take opposite values in the two, and adds its
half-width twice. With a nominal difference of 0.6 and a shared error in $`[-1, 1]`$ the separate bound is
$`[0.6 - 2,\ 0.6 + 2] = [-1.4, 2.6]`$ and the joint bound is $`[0.6, 0.6]`$.

## D6. Misstatement tolerance

Let at most $`\Gamma`$ of the unresolved fields be misstated at once, each within its half-width. The set is
$`U_\Gamma = \{u : \left\vert u_j\right\vert \le d_j,\ \text{at most } \Gamma \text{ coordinates nonzero}\}`$, and

```math
h_{U_\Gamma}(a) = \max_{\left\vert J\right\vert \le \Gamma}\ \sum_{j\in J}\left\vert a_j\right\vert d_j = \sum_{j\le\Gamma}s_{(j)}, \qquad (D6.1)
```

the sum of the $`\Gamma`$ largest swings, since the adversary chooses which fields to move and moves each to its
worst endpoint. The ordering survives $`\Gamma`$ misstatements exactly when $`m_f - \sum_{j\le\Gamma}s_{(j)} > 0`$,
which gives $`\Gamma^*_{ik} = \max\{\Gamma : \sum_{j\le\Gamma}s_{(j)} < m_f\}`$. ∎ With margin 1.0 and swings
0.4, 0.3, 0.3, 0.2, 0.2, 0.1 the box bound fails, because the swings sum to 1.5. The two largest sum to 0.7 and the
three largest to 1.0, so $`\Gamma^* = 2`$. The code confirms the value by searching over every subset of misstated
fields.

## D7. Smooth nonlinear scores

Set $`m_f = \Delta_f(0)`$ and $`a_f = \nabla\Delta_f(0)`$. If $`\Delta_f`$ is twice continuously differentiable on
$`\|u\|_2 \le r`$ with Hessian operator norm at most $`K_f`$, Taylor's theorem with the Lagrange remainder gives
$`\left\vert\Delta_f(u) - m_f - a_f^\top u\right\vert \le \tfrac12K_f\|u\|^2 \le \tfrac12K_fr^2 = \kappa_f`$. Combining with D5 on the
ball of radius $`r`$, $`\underline\Delta_f \ge m_f - r\|a_f\|_2 - \kappa_f`$. ∎

## D8. The value of a query is nonnegative

For a fixed action $`a`$, the worst-case regret $`\sup_{\omega\in\Omega'}[\max_bW(b,\omega) - W(a,\omega)]`$ is
nondecreasing in the scenario set $`\Omega'`$. Every observation restricts the scenarios to
$`\Omega_{q,o} \subseteq \Omega`$, so $`R^*(\Omega_{q,o}) \le R^*(\Omega)`$ after minimizing over actions, and
$`V(q) = R^*(\Omega) - \sup_oR^*(\Omega_{q,o}) \ge 0`$. ∎ The calculation uses the set of compatible scenarios and
no probability over them.

## D9. The exact plan for affine scores

**Setup.** Two actions, advance company $`i`$ or company $`k`$. The regret of advancing $`i`$ in a scenario with
difference $`\Delta`$ is $`(-\Delta)_+`$, and of advancing $`k`$ it is $`\Delta_+`$. The difference is
$`\Delta(u) = m + \sum_ja_ju_j`$ with $`\left\vert u_j\right\vert \le d_j`$, swings $`s_j = \left\vert a_j\right\vert d_j`$ and total swing
$`h = \sum_js_j`$. Take $`m \ge 0`$ without loss of generality.

**Before verification.** Advancing $`i`$ has worst-case regret $`(h - m)_+`$ and advancing $`k`$ has $`h + m`$, so
$`R_\varnothing = (h - \left\vert m\right\vert)_+`$.

**After verifying a set $`J`$.** The values $`u_J`$ become known. The margin moves to
$`m' = m + \sum_{j\in J}a_ju_j`$, which can be any point of $`[m - s_J,\ m + s_J]`$, and the remaining swing is
$`h - s_J`$. The action is chosen again, so the regret after the observation is $`(h - s_J - \left\vert m'\right\vert)_+`$. The worst
observation makes $`\left\vert m'\right\vert`$ as small as possible:

- if $`s_J \ge \left\vert m\right\vert`$, the margin can be driven to zero and the regret is $`(h - s_J)_+`$;
- if $`s_J < \left\vert m\right\vert`$, the smallest margin is $`\left\vert m\right\vert - s_J`$ and the regret is
  $`(h - s_J - \left\vert m\right\vert + s_J)_+ = (h - \left\vert m\right\vert)_+`$.

```math
R_J = \big(h - \max(s_J, \left\vert m\right\vert)\big)_+, \qquad V(J) = R_\varnothing - R_J = (s_J - \left\vert m\right\vert)_+ \quad\text{when } h > \left\vert m\right\vert . \quad ∎ \qquad (D9.1)
```

Verification acts twice: it removes $`s_J`$ of swing and it can move the margin by $`s_J`$ against the current
leader. Until $`s_J`$ exceeds $`\left\vert m\right\vert`$ the two cancel in the worst case. The code checks the closed form against an
exact search on 300 random instances.

**Consequences.**

1. *Pivot rule.* For a single field, $`V = (s_j - \left\vert m\right\vert)_+`$: positive only if that field alone could reverse the
   decision.
2. *Complementarity.* $`V(J)`$ depends on the fields through their sum, so two fields with $`s_j < \left\vert m\right\vert`$ each and
   $`s_1 + s_2 > \left\vert m\right\vert`$ are worth nothing alone and $`s_1 + s_2 - \left\vert m\right\vert`$ together.
3. *Knapsack.* $`R_J`$ is nonincreasing in $`s_J`$, so with costs $`c_j`$ and a budget the plan that leaves the
   least regret maximizes $`\sum_{j\in J}s_j`$ subject to $`\sum_{j\in J}c_j \le`$ budget. Ordering by
   $`s_j/c_j`$ solves the relaxation.
4. *Shared sources.* A coordinate with $`a_j = 0`$ has zero swing and never enters the plan.
5. *Assurance tiers.* If a check leaves a fraction $`\lambda_j`$ of the half-width, the swing it removes is
   $`(1-\lambda_j)s_j`$, and that quantity replaces $`s_j`$ in the knapsack.

**Example 4.** $`m = 0.6`$, swings 0.9, 0.5, 0.4, 0.3, 0.2 and costs 4, 1, 2, 1, 1 hours. $`h = 2.3`$ and
$`R_\varnothing = 1.7`$. Only the first field passes the pivot rule, with value 0.3; the second and third together
are worth 0.3. With four hours, the largest swing first verifies field 1 and leaves 1.4. Ordering by swing per
hour verifies fields 2, 4 and 3, removes 1.2 of swing and leaves 1.1, which an exhaustive search confirms as the
optimum.

## D10. Corrections propagate through attributions

Shapley efficiency states $`f(x) = \phi_0 + \sum_j\phi_j(f,Q,x)`$ for a fixed background $`Q`$. Writing it at
$`x`$ and at $`x'`$ and subtracting gives $`\sum_j[\phi_j(f,Q,x') - \phi_j(f,Q,x)] = f(x') - f(x)`$. ∎ For
approximate attributions with efficiency residuals at most $`\eta`$ and $`\eta'`$ under the same baseline, the
triangle inequality gives $`\left\vert\sum_j\Delta\phi_j - \Delta f\right\vert \le \eta + \eta'`$, the recomputation check every
update passes before its explanations are shown.
