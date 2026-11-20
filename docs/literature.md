# Where this work sits

Due diligence has more facts to check than analyst time to check them. Explainable AI says what a scoring model
cares about. Robust optimization bounds a decision over a set of inputs. Preference elicitation chooses questions
by the regret they remove. The ESG literature documents how unreliable the inputs are. None of these says which
fact to verify next when the facts themselves are the open question and several companies share their sources.
This page records what each line establishes, where it stops, and what the article adds. The complete list of 172
sources is in the [bibliography](bibliography.md).

## The short version

| Line of work | What it establishes | Where it stops | What the article adds |
| --- | --- | --- | --- |
| Feature attribution: SHAP, conditional Shapley, impossibility theorems | An additive account of a prediction; proof that attribution cannot predict behavior under changed inputs | The inputs are taken as given | Verification value as swing against the margin, with attribution kept for explanation |
| Model multiplicity: Rashomon sets, hacking intervals, consensus orders | Statements that hold across every near-optimal model | Uncertainty is on the model side only | A joint set over models and evidence, with errors shared across companies |
| Robust optimization and robust ordinal regression: Ben-Tal and Nemirovski, Bertsimas and Sim, Greco et al. | Tractable worst-case bounds; preferences that hold for every compatible value function | Inputs known, or a single decision | A certified partial order over companies and a tolerance per ranking |
| Certain predictions and data cleaning: Karlaš et al. | Predictions that hold for every completion of incomplete data, and which row to clean next | Worlds independent across rows; selection by counting worlds | Shared errors that cancel, and a plan with no prior over worlds |
| Query selection by minimax regret: Boutilier et al., Vayanos et al. | Questions chosen by the worst-case regret they remove | The questions elicit a decision maker's preferences | Queries that are facts about companies, with an exact solution for affine scores |
| ESG measurement and assurance: Berg et al., Aswani et al., Duflo et al. | Ratings diverge mostly through measurement; a vendor's estimates can drive a published result; paid auditors report favorably | Diagnosis | An error model that carries shared sources and assurance tiers into the plan |
| Common bias: Bradley et al., Armstrong and Kolesár | A large biased sample is worth a tiny random one; bias-aware critical values | Inference, not scheduling | The sample size past which verification beats collection |

## Timing

The framework dates from late 2023. SHAP, Rashomon sets, robust optimization, robust ordinal regression and
minimax-regret elicitation precede it. The impossibility theorems for attribution and the re-examination of the
carbon-return relationship were published while the work was under way, and both support its starting point: what
a model attends to and what is still open in the evidence are different questions.

## Key sources

### What attribution can and cannot say

<a id="lundberg2017"></a>
**Lundberg and Lee (2017), "A Unified Approach to Interpreting Model Predictions."** [arXiv](https://arxiv.org/abs/1705.07874)
Shapley values are the unique additive attribution with local accuracy, missingness and consistency. For a linear
model the attribution of a feature is its coefficient times its distance from the background mean. That formula is
the first half of D1; the second half is that verification value depends on a different quantity, the width of the
unresolved error.

<a id="kumar2020"></a>
**Kumar, Venkatasubramanian, Scheidegger and Friedler (2020), "Problems with Shapley-Value-Based Explanations as Feature Importance Measures."** [PMLR](https://proceedings.mlr.press/v119/kumar20e.html)
A Shapley value does not say which change to an input would move the outcome. The paper states the gap for
explanation in general. Diligence needs the answer for one kind of change, the correction of a misreported fact,
which the swing supplies.

<a id="bilodeau2024"></a>
**Bilodeau, Jaques, Koh and Kim (2024), "Impossibility Theorems for Feature Attribution."** [arXiv](https://arxiv.org/abs/2212.11870)
For expressive model classes, complete and linear attribution methods do no better than random guessing at
inferring how a model behaves under changed inputs, and the remedy is to evaluate the model directly on the
changes of interest. The bounds of Sections 2 to 4 are that remedy, applied to the set of admissible corrections.

### Statements that hold across many models

<a id="marx2023"></a>
**Marx et al. (2023), "But Are You Sure? An Uncertainty-Aware Perspective on Explainable AI."** [PMLR](https://proceedings.mlr.press/v206/marx23a.html)
Under uniform convergence the best model lies within a stated distance of the empirical minimum, and explanations
are reported as ranges over that set. Section 2 takes the construction and adds the finite-class radius and the
excess-loss bound. The paper's set is over models; the inputs are fixed.

<a id="coker2021"></a>
**Coker, Rudin and King (2021), "A Theory of Statistical Inference for Ensuring the Robustness of Scientific Results."** [arXiv](https://arxiv.org/abs/1804.08646)
Hacking intervals report the range of a statistic over all defensible analysis choices. This is the closest
antecedent of a worst case over admissible analyses. It varies the analysis; the joint set of Section 2 varies the
evidence as well, and keeps the dependence of errors across companies.

<a id="laberge2023"></a>
**Laberge et al. (2023), "Partial Order in Chaos: Consensus on Feature Attributions in the Rashomon Set."** [JMLR](https://www.jmlr.org/papers/v24/23-0149.html)
Only the attribution statements on which every near-optimal model agrees are reported, which gives a partial order
of features. The certificate of Section 2 has the same form, a partial order of what holds everywhere, with
companies in the place of features and unverified evidence inside the set.

<a id="watsondaniels2023"></a>
**Watson-Daniels, Barocas, Hofman and Chouldechova (2023), "Multi-Target Multiplicity."** [arXiv](https://arxiv.org/abs/2306.13738)
Points whose selection does not change across the Rashomon set are certified under a resource constraint. The
paper certifies selections over models. It has no unverified inputs and no account of which input to check.

### Decisions over sets

<a id="bental1998"></a>
**Ben-Tal and Nemirovski (1998), "Robust Convex Optimization."** [pdf](https://www2.isye.gatech.edu/~nemirovs/MOR_RCO_1998.pdf)
The foundation of robust convex optimization, with tractable counterparts for ellipsoidal uncertainty. The support
functions of Section 3 are its basic tool. I use them on the difference of two companies' scores, where a shared
source drops out.

<a id="bertsimas2004"></a>
**Bertsimas and Sim (2004), "The Price of Robustness."** [RePEc](https://ideas.repec.org/a/inm/oropre/v52y2004i1p35-53.html)
A budget on the number of coefficients that deviate at once controls the conservatism of a robust solution. The
paper uses the budget to tune a solution. I read it in the other direction, as the largest number of simultaneous
misstatements a ranking survives, and report that number.

<a id="greco2008"></a>
**Greco, Mousseau and Słowiński (2008), "Ordinal Regression Revisited."** [RePEc](https://ideas.repec.org/a/eee/ejores/v191y2008i2p416-436.html)
The necessary preference relation holds for every value function compatible with a decision maker's stated
judgments, and it grows with information. A certified ranking is a necessary preference over the joint set. In
robust ordinal regression the inputs are known and all uncertainty is in the value function.

<a id="karlas2020"></a>
**Karlaš et al. (2020), "Nearest Neighbor Classifiers over Incomplete Information."** [arXiv](https://arxiv.org/abs/2005.05117)
A certain prediction holds for every classifier trained on every completion of an incomplete data set, and a
companion rule chooses which row a person should clean next. This is the closest work in structure: a certificate
and a choice of what to fix. Its possible worlds are independent across rows, so an error shared by two units
cannot cancel, and its rule counts worlds, which is a uniform prior over them.

<a id="mogstad2024"></a>
**Mogstad, Romano, Shaikh and Wilhelm (2024), "Inference for Ranks."** [NBER](https://www.nber.org/papers/w26883)
Simultaneous confidence sets for ranks under sampling error. The sets pay for simultaneity and treat each unit's
estimate as a noisy draw. A certified partial order pays nothing for the number of pairs, because one inclusion
event covers them all, and it carries unverified inputs.

### Choosing what to ask

<a id="boutilier2006"></a>
**Boutilier, Patrascu, Poupart and Schuurmans (2006), "Constraint-Based Optimization and Utility Elicitation Using the Minimax Decision Criterion."** [abstract](https://www.cs.toronto.edu/~cebly/Papers/BPPS-aij06-abs.html)
Minimax regret as the decision criterion under set-based uncertainty about utilities, and queries chosen to reduce
it. The criterion of Section 4 is theirs. Their queries ask a person about preferences; mine are facts about
companies, whose answers move the inputs of every retained model and cost analyst hours.

<a id="vayanos2020"></a>
**Vayanos et al. (2020), "Robust Active Preference Elicitation."** [arXiv](https://arxiv.org/abs/2003.01899)
Pairwise comparison queries chosen to minimize worst-case regret over a polyhedral set of utility weights, solved
by mixed-integer programming. The general problem needs a solver. For an affine score with interval evidence the
verification problem has the closed form of D9, and the plan is a knapsack.

### Evidence that is wrong together

<a id="berg2022"></a>
**Berg, Kölbel and Rigobon (2022), "Aggregate Confusion: The Divergence of ESG Ratings."** [Review of Finance](https://academic.oup.com/rof/article/26/6/1315/6590670)
Ratings from six agencies diverge widely, and measurement accounts for more of the divergence than scope or
weights, with a rater effect that correlates a rater's errors across categories. The inputs to an ESG score are
uncertain and their errors have structure, which is the case for a joint error model.

<a id="aswani2024"></a>
**Aswani, Raghunandan and Rajgopal (2024), "Are Carbon Emissions Associated with Stock Returns?"** [doi](https://doi.org/10.1093/rof/rfad013)
The association between emissions and returns reported in earlier work traces to emissions that a data vendor
estimated from financial fundamentals, with minimal evidence of it in the emissions firms disclosed themselves. A
shared third-party estimate moved a published conclusion, the error structure the joint set is built to carry.

<a id="duflo2013"></a>
**Duflo, Greenstone, Pande and Ryan (2013), "Truth-Telling by Third-Party Auditors and the Response of Polluting Firms."** [RePEc](https://ideas.repec.org/a/oup/qjecon/v128y2013i4p1499-1545.html)
Auditors chosen and paid by the plants they audited reported readings just below the regulatory standard. A check
is not a fact. Section 4 lets a verified field keep a fraction of its allowance according to the standing of the
source.

<a id="lyon2011"></a>
**Lyon and Maxwell (2011), "Greenwash: Corporate Environmental Disclosure under Threat of Audit."** [RePEc](https://ideas.repec.org/a/bla/jemstr/v20y2011i1p3-41.html)
Firms disclose selectively in response to the audits they expect. A verification rule the scored companies can
anticipate invites embellishment where checks are unlikely, so the plan is held inside the diligence team and
mixed with random checks.

<a id="bradley2021"></a>
**Bradley et al. (2021), "Unrepresentative Big Surveys Significantly Overestimated US Vaccine Uptake."** [arXiv](https://arxiv.org/abs/2106.05818)
A survey with about 250,000 responses a week overestimated uptake by 17 percentage points, no more accurate than a
simple random sample of size 10. Under a shared bias the interval shrinks and the error does not. The paper
measures the problem; Section 1 gives the sample size past which the next hour belongs to verification.

<a id="armstrong2020"></a>
**Armstrong and Kolesár (2020), "Simple and Honest Confidence Intervals in Nonparametric Regression."** [doi](https://doi.org/10.3982/QE1199)
Critical values that account for a bounded bias give the shortest fixed-length intervals with honest coverage.
The bias there is a smoothing bias. I use the same critical value for a reporting bias bounded by verification,
and read off the threshold $`n^*`$.
