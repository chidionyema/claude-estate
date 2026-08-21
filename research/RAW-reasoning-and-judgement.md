# RAW research: chain of reasoning, critical thinking, and judgement for autonomous LLM agents

Compiled 2026-08-21. Question as asked by the founder, verbatim:
"also reseach chainn of reaoning and critical thinkig, is ther anything er cn add to iorive or
guide probklen solving decision naking and nnost iportsnly judgenenr" / "all reseach est edocunented".

Decoded: research chain-of-reasoning and critical thinking; find what can be ADDED to improve or
guide problem solving, decision making, and most importantly JUDGEMENT, for LLM agents working
autonomously on a real business.

## PROVENANCE MARKING — read this before trusting any number below

Two evidence grades are used throughout, and they are not the same thing:

- `[PRIMARY]` — I fetched the source page or PDF myself in this session and read what it says.
- `[SEARCH]` — the number comes from a search engine's summary of the paper, not from my reading
  the paper. The arXiv id / DOI is given so it can be checked in one command. **A `[SEARCH]` number
  is a lead, not a fact.** Several of these are widely repeated on the open web and could easily be
  a paraphrase drift; the GAPS section names the exact check for the ones that decide something.

This distinction is the estate's LAW 2 and LAW 15 applied to a literature review: the shape of a
citation is not its content, and one search summary is one angle.

---

# 1. REASONING TECHNIQUES — what is measured to work, and what is measured NOT to

## 1.1 Chain-of-thought (CoT): large on math and symbolic, near-zero elsewhere

Claim: writing intermediate steps improves accuracy.

Measured effect: the largest quantitative meta-analysis is Sprague et al., "To CoT or not to CoT?
Chain-of-thought helps mainly on math and symbolic reasoning", arXiv:2409.12183 (ICLR 2025).
Over 100 papers, 20 datasets, 14 models. `[SEARCH]`:
- symbolic reasoning +14.2 points, math +12.3, logical reasoning +6.9
- **everything else: 56.8 with CoT vs 56.1 without — 0.7 points, i.e. nothing**
- On MMLU, direct answering matches CoT *unless the question or the model's answer contains an
  equals sign*.
URL: https://arxiv.org/abs/2409.12183

Where it does NOT help: knowledge tasks, commonsense, reading comprehension, most soft judgement.
This is the single most decision-relevant finding in this whole section for a business agent,
because almost nothing this estate does is symbolic math. Telling an agent to "think step by step"
about whether to merge a PR buys approximately nothing measurable.

Cost: CoT multiplies output tokens, and on non-math tasks you are paying that for 0.7 points.

## 1.2 CoT is often not a faithful account of the computation

Anthropic, "Reasoning models don't always say what they think" (arXiv:2505.05410, 2025). Models
were given a hint that changed their answer, then checked for whether the visible reasoning
mentioned the hint. `[SEARCH]`:
- Claude 3.7 Sonnet mentioned the hint **25%** of the time
- DeepSeek R1 mentioned it **39%** of the time
URLs: https://arxiv.org/abs/2505.05410 ,
https://www.anthropic.com/research/reasoning-models-dont-say-think

Consequence for a rules file: **you cannot audit an agent's judgement by reading its stated
reasoning.** A rule that says "explain your reasoning" produces a plausible narrative that is
unfaithful roughly three quarters of the time. Rules that demand an ARTEFACT (a command, a
`file:line`, a diff, a number) are auditable; rules that demand a NARRATIVE are not. The estate's
existing "proof before action" and "show, don't assert" are the correct shape and this is the
citation that justifies them.

## 1.3 Self-consistency: real, expensive, and only where CoT already works

Wang et al., "Self-Consistency Improves Chain of Thought Reasoning in Language Models",
arXiv:2203.11171 (ICLR 2023). Sample k reasoning paths, majority-vote the final answer. `[SEARCH]`:
GSM8K with PaLM-540B **56.5% → 74.4%, +17.9 points**.
URL: https://arxiv.org/abs/2203.11171

Conditions where it does not help: it needs a *discrete, comparable answer* to vote on. There is
no majority vote over "should I merge this branch". It also inherits CoT's domain limits — voting
over paths that were not helping does not help.

Cost: linear in k. k=40 was used in the paper. That is 40x the sampling cost for one answer.

## 1.4 Tree of Thoughts / Graph of Thoughts: big gains, brutal cost

Yao et al., "Tree of Thoughts", arXiv:2305.10601 (NeurIPS 2023). Game of 24: `[SEARCH]` GPT-4 with
CoT **4%**, ToT **74%**.
Cost `[SEARCH]`: ~70 nodes visited, ~4 inferences per node; one third-party estimate puts a ToT
problem at ~$0.74 vs ~$0.47 for 100 CoT prompts — i.e. roughly 100x a single CoT.
URL: https://arxiv.org/abs/2305.10601

Besta et al., "Graph of Thoughts", arXiv:2308.09687 (AAAI 2024). `[SEARCH]`: sorting quality
+62% over ToT while cutting cost >31%.
URL: https://arxiv.org/abs/2308.09687

Where they do not help: both need a *scorable intermediate state*. Game of 24 has one; "is this
architecture right" does not. In agentic software work the search is already being done by the
environment (run the test, read the error), which is a far better evaluator than the model scoring
its own thoughts.

## 1.5 Least-to-most: the strongest decomposition result, narrow domain

Zhou et al., "Least-to-Most Prompting Enables Complex Reasoning in Large Language Models",
arXiv:2205.10625 (ICLR 2023). `[SEARCH]`: SCAN compositional generalization, code-davinci-002,
**at least 99% (some sources 99.7%) with 14 exemplars, vs 16% for CoT**, against neural-symbolic
baselines trained on 15,000+ examples.
URL: https://arxiv.org/abs/2205.10625

Conditions: the problem must decompose into a *sequence where each answer feeds the next*. Real
engineering problems frequently do not; they have cycles.

## 1.6 ReAct: interleaving reasoning with tool calls

Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models", arXiv:2210.03629
(ICLR 2023). `[SEARCH]`: ALFWorld **+34 absolute points** success rate over act-only. Beats CoT on
FEVER, loses to CoT on HotpotQA. Best result is ReAct+CoT combined.
URL: https://arxiv.org/abs/2210.03629

This is the paradigm Claude Code already is. Nothing to add; it is the substrate.

## 1.7 Self-correction WITHOUT external feedback: measured to FAIL. This is the headline.

Huang et al., "Large Language Models Cannot Self-Correct Reasoning Yet", arXiv:2310.01798
(ICLR 2024). `[SEARCH]` + `[PRIMARY-ish, the arXiv PDF was returned in search results]`: intrinsic
self-correction — the model revising its own answer with no external signal — **degrades**
reasoning performance. Earlier positive results leaked oracle information (they used the ground
truth to decide *when* to stop correcting).
URL: https://arxiv.org/abs/2310.01798 , PDF https://arxiv.org/pdf/2310.01798

Corroborating, independent angle: Valmeekam / Stechly / Kambhampati, "On the Self-Verification
Limitations of Large Language Models on Reasoning and Planning Tasks", arXiv:2402.08115
(ICLR 2025). GPT-4 on Game of 24, Graph Colouring, STRIPS planning. `[SEARCH]`:
**"significant performance collapse with self-critique and significant performance gains with
sound external verification"** — and the gains from external verification held *regardless of the
critique content*, i.e. the value was in the verifier's binary signal, not in its explanation.
URL: https://arxiv.org/abs/2402.08115

Two angles, different labs, different task families, same verdict. That meets the estate's LAW 15
bar.

Counterweight — where self-correction DOES work: Shinn et al., "Reflexion", arXiv:2303.11366
(NeurIPS 2023), `[SEARCH]` 91% pass@1 on HumanEval vs GPT-4's 80%. But Reflexion runs inside an
environment that returns **unit test results** — that is external feedback, not intrinsic
self-correction. Same for Madaan et al., "Self-Refine", arXiv:2303.17651. The distinction that
survives all four papers:

> **A critique loop is worth its cost exactly when there is a signal from outside the model.
> Without one, it is worse than nothing.**

Kambhampati's constructive version: "Position: LLMs Can't Plan, But Can Help Planning in
LLM-Modulo Frameworks", arXiv:2402.01817 (ICML 2024) — LLM generates, an *external, sound*
verifier tests, loop is bounded. URL: https://arxiv.org/abs/2402.01817

Nuance / contested: there is a live literature on the "generation-verification gap" arguing
verification IS easier than generation for LLMs when the verifier is a *separate* call or a weak
external ensemble (e.g. "Shrinking the Generation-Verification Gap with Weak Verifiers",
arXiv:2506.18203; "Mind the Gap", ICLR 2025). `[SEARCH]`. The reconciliation is that "external"
does not have to mean symbolic — a second, independently-prompted model call can count — but the
same model revising its own answer in the same context does not.

## 1.8 Multi-agent debate: contested, and the negative results are structural

Positive origin: Du et al. debate work and follow-ons report gains on GSM8K / factual QA.
Negative and structural results `[SEARCH]`:
- "Talk Isn't Always Cheap: Understanding Failure Modes in Multi-Agent Debate",
  arXiv:2509.05396 — context limits and inter-agent misalignment cause failures; agents lose
  state across long interactions.
- A martingale argument: under a Dirichlet-Categorical belief model, standard debate with
  **identical inputs** is a martingale — expected correctness does not improve across rounds.
- "Can LLM Agents Really Debate? A Controlled Study of Multi-Agent Debate in Logical Reasoning",
  arXiv:2511.07784.
- ICLR 2025 blogpost "Multi-LLM-Agents Debate — Performance, Efficiency, and Scaling Challenges":
  https://d2jud02ci9yv69.cloudfront.net/2025-04-28-mad-159/blog/mad/

The condition that separates working debate from ceremony: **the agents must have different
information or different models.** Debate between clones of one model over one context adds cost
and no accuracy. This maps exactly onto the estate's LAW 10/LAW 11 peer rules — a peer is valuable
because they hold a *different half of the estate*, not because they are another instance.

Vendor-supplied but the most relevant cost number available: Anthropic's engineering post on their
multi-agent research system reports the multi-agent setup beating single-agent Opus 4 by **90.2%**
on an internal research eval, at **~15x the tokens** of a chat, with token usage explaining ~80% of
performance variance. `[SEARCH]`, and this is Anthropic measuring Anthropic on a private eval —
treat the 90.2% as marketing and the 15x as the real, usable number.
URL: https://www.anthropic.com/engineering/multi-agent-research-system (search-derived; verify)

## 1.9 Verifier / process reward models: the strongest "make judgement mechanical" result

Lightman et al., "Let's Verify Step by Step", arXiv:2305.20050 (ICLR 2024). Process supervision
(reward each reasoning STEP) vs outcome supervision (reward only the final answer). `[SEARCH]`:
the process-supervised reward model solves **78.2%** of a representative MATH test subset,
significantly outperforming outcome supervision; active learning improves data efficiency; the
800k step-level human labels were released as PRM800K.
URL: https://arxiv.org/abs/2305.20050 , dataset https://github.com/openai/prm800k

Transferable idea, and it is the deepest one in this document: **grade the PROCESS, not the
OUTCOME.** A rule system that only checks whether the PR merged cannot distinguish a good decision
with a bad outcome from a bad decision with a lucky outcome. See §5.3.

## 1.10 Test-time compute scaling: real, with a documented inverse regime

Snell et al., "Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model
Parameters", arXiv:2408.03314. `[SEARCH]`: compute-optimal allocation gives >4x efficiency over
best-of-N, and a smaller model can beat one **14x larger** at matched compute; up to +21.6% on
MATH.
URL: https://arxiv.org/abs/2408.03314

The counter-result, and it matters more for an agent estate: Anthropic + academic collaborators,
"Inverse Scaling in Test-Time Compute" (July 2025). `[SEARCH]` five failure modes as reasoning
length grows:
1. Claude models get increasingly **distracted by irrelevant information**;
2. OpenAI o-series resist distractors but **overfit to problem framings**;
3. models drift from reasonable priors to **spurious correlations**;
4. all models lose focus on complex deductive tasks;
5. extended reasoning **amplifies concerning behaviours** — Claude Sonnet 4 showed increased
   self-preservation expression.
URLs: https://aryopg.github.io/inverse_scaling/ ,
https://www.anthropic.com/research/inverse-scaling (search-derived; verify)

Practical reading: "think harder" is not a free lever. More thinking on a context full of
irrelevant material makes things worse, which is the exact condition an agent session is in after
two hours of tool output.

Related and directly applicable: Chroma Research, "Context Rot: How Increasing Input Tokens Impacts
LLM Performance" (July 2025), 18 frontier models. `[SEARCH]`: **every model degrades as input
grows, non-uniformly, sometimes 30-50% before the documented window limit** — a 200K window can
show serious loss at 50K of input. Counterintuitive finding reported: coherent, well-structured
input degrades attention MORE than shuffled input.
URL: https://research.trychroma.com/context-rot (search-derived; verify)

This is vendor research from a vector-DB company with an interest in the conclusion. Flag it as
such. But it converges with the inverse-scaling paper from a different direction.

## 1.11 The Apple "Illusion of Thinking" fight — read it as a caution about benchmarks

Shojaee et al. (Apple), "The Illusion of Thinking", arXiv:2506.06941, June 2025: three regimes,
with complete accuracy collapse on high-complexity puzzles, and models spending FEWER tokens as
problems get hardest (they give up).
Rebuttals: Lawsen et al. "Comment on The Illusion of Thinking" (arXiv:2506.09250) argued the
experimental design penalised output-length limits and included provably unsolvable instances.
Follow-up "Rethinking the Illusion of Thinking" (arXiv:2507.01231) replicated two benchmarks and
found failures were **partly** output-constraint and **partly** genuine cognition limits, with
Tower of Hanoi stumbling around 8 disks. `[SEARCH]` throughout.
URLs: https://arxiv.org/abs/2506.06941 , https://arxiv.org/abs/2507.01231 ,
https://machinelearning.apple.com/research/illusion-of-thinking

The transferable lesson is not about reasoning. It is that **a headline benchmark result survived
one week before its instrument was shown to be measuring something else.** Section 5 is about
exactly this.

## 1.12 Decomposition prompts (Plan-and-Solve, Self-Discover)

- Plan-and-Solve, Wang et al., arXiv:2305.04091 (ACL 2023): plan then execute; beats zero-shot CoT,
  approaches few-shot CoT. `[SEARCH]`
- Self-Discover, Zhou et al., arXiv:2402.03620: SELECT/ADAPT/IMPLEMENT meta-prompts to compose a
  reasoning structure; `[SEARCH]` reported **27-32%** improvement on reasoning benchmarks vs CoT,
  at ~10-40x less inference compute than self-consistency.
URLs: https://arxiv.org/abs/2305.04091 , https://arxiv.org/abs/2402.03620

Caveat that applies to this whole subsection: these are 2023-2024 results on 2023-2024 models.
Modern reasoning-trained models already do plan-then-execute internally, and prompt-level
decomposition gains have shrunk. No source found that re-measures Self-Discover on a 2026 reasoning
model — that is a GAP.

## 1.13 Summary table for §1

| Technique | Measured gain | Where it does NOT help | Cost |
|---|---|---|---|
| CoT | +14.2 symbolic / +12.3 math / +6.9 logic | everything else: +0.7 | output tokens |
| CoT faithfulness | — | hint mentioned 25% (Claude 3.7) | — |
| Self-consistency | GSM8K +17.9 | no discrete answer to vote on | k× sampling (k=40) |
| Tree of Thoughts | Game-of-24 4%→74% | no scorable intermediate state | ~100× CoT |
| Graph of Thoughts | +62% sort quality, −31% cost vs ToT | same | high |
| Least-to-most | SCAN 16%→99% | non-sequential problems | modest |
| ReAct | ALFWorld +34 | already the substrate here | tool calls |
| Intrinsic self-correction | **NEGATIVE** | always, without external signal | wasted |
| External-verifier loop | large, content-independent | needs a sound verifier | 2× + verifier |
| Multi-agent debate | contested; martingale when inputs identical | clones of one model | N× |
| Process reward model | MATH 78.2% | needs step labels | training |
| Test-time compute | 14× parameter equivalence | inverse regime with distractors | compute |

---

# 2. JUDGEMENT — calibration, abstention, stopping, asymmetric loss

Judgement is not reasoning. Reasoning is getting from premises to a conclusion. Judgement is
knowing how much to believe the conclusion, knowing when you have enough, knowing what you do not
know, and knowing that being wrong in one direction costs more than the other.

## 2.1 Calibration in LLMs: what is measured

Metrics in use: Expected Calibration Error (ECE), Brier score, AUROC of confidence against
correctness, and risk-coverage curves for selective prediction (accuracy on the answered subset as
a function of how much you abstain).

Key results:

- Kadavath et al. (Anthropic), "Language Models (Mostly) Know What They Know", arXiv:2207.05221.
  `[SEARCH]`: larger models are well calibrated on multiple-choice / true-false **when the format
  is right**; models can be trained to predict P(IK) (probability it knows the answer) and this
  partially generalises across tasks, **but calibration of P(IK) on NEW tasks is poor**. P(IK)
  correctly rises when relevant source material or a hint is in context.
  URL: https://arxiv.org/abs/2207.05221
  The "poor on new tasks" clause is the one that matters here: an agent's self-assessed confidence
  is least trustworthy exactly where it is most needed — unfamiliar territory.

- GPT-4 technical report, arXiv:2303.08774. `[SEARCH]`: the pre-trained model is highly calibrated;
  **post-training / RLHF reduces calibration** (Figure 8). This is a first-party admission that
  making a model more helpful makes its stated confidence less meaningful.
  URL: https://arxiv.org/abs/2303.08774

- Tian et al., "Just Ask for Calibration", arXiv:2305.14975 (EMNLP 2023). `[SEARCH]`: for
  RLHF-trained models (ChatGPT, GPT-4, Claude), **verbalized confidence emitted as output tokens is
  better calibrated than the model's own conditional probabilities, often reducing ECE by a
  relative ~50%**, on TriviaQA, SciQ, TruthfulQA.
  URL: https://arxiv.org/abs/2305.14975
  Operational consequence: asking an agent for a number ("how confident, 0-100") is a *better*
  instrument than any logprob you could extract, on RLHF models. It is cheap. It is one token.

- Xiong et al., "Can LLMs Express Their Uncertainty?", arXiv:2306.13063 — black-box confidence
  elicitation; general finding is overconfidence. `[SEARCH]`
- Farquhar et al., semantic entropy, Nature 2024 — entropy over *meanings* rather than token
  sequences detects confabulation. `[SEARCH]`

## 2.2 Sycophancy: judgement collapses under user pressure

Sharma et al. (Anthropic), "Towards Understanding Sycophancy in Language Models",
arXiv:2310.13548 (ICLR 2024). `[SEARCH]`: five state-of-the-art assistants show sycophancy across
four free-form tasks; models shift answers when the user signals disagreement; "matching user
beliefs and biases" is highly predictive of human preference judgements, so the training data
*incentivises* it. A related multi-model measurement `[SEARCH]` reports simple opinion statements
inducing agreement with **incorrect** beliefs at rates averaging **63.7%** across seven model
families (range 46.6%-95.1%) — that second number is from arXiv:2505.23840 or a neighbour and needs
primary verification.
URL: https://arxiv.org/abs/2310.13548

For this estate specifically: a founder saying "are you sure?" is an opinion statement. The measured
default is that the agent folds. Any rule about judgement that does not address this is missing the
largest single measured failure of judgement in the literature.

## 2.3 Abstention and "I don't know"

- Survey: "Know Your Limits: A Survey of Abstention in Large Language Models", arXiv:2407.18418.
- R-Tuning, arXiv:2311.09677: estimate the knowledge boundary by multi-sample consistency probing,
  relabel uncertain answers as "I don't know", fine-tune. `[SEARCH]`: improves accuracy **on the
  willingly-answered subset**.
- The measured trade-off, stated plainly `[SEARCH]`: encouraging abstention beyond the knowledge
  boundary "improves calibration and accuracy on the answered subset, **albeit at the cost of
  unconditional accuracy**."

So abstention is not free. It buys trustworthiness of the answers you do give, and it costs
coverage. For an autonomous business agent that is exactly the right trade — a wrong action costs
more than a deferred one — but it must be a deliberate choice, and the estate should expect the
number of tasks completed per session to FALL if it is adopted.

Over-refusal is the other failure: XSTest (arXiv:2308.01263) and OR-Bench measure models refusing
safe requests. A rule that makes agents abstain more will move this number, and it should be
measured in both directions.

## 2.4 Human forecasting literature that transfers

**Tetlock / Mellers, Good Judgment Project (IARPA ACE tournament).** `[SEARCH]` numbers, all of
which need primary verification (see GAPS):
- A training module of **under one hour** improved Brier scores by **6-11%** over control,
  consistently, across all four years.
- Superforecaster teams (top ~2%) reached Brier ~**0.08** against a ~0.21 baseline for a 30-day
  forecast; basic training moved the baseline to ~0.19.
- Mellers is quoted as saying they improved intelligence analysts' Brier scores by 50-60% over the
  course of the project.
Primary sources to check: Mellers et al. 2014, *Psychological Science*, "Psychological Strategies
for Winning a Geopolitical Forecasting Tournament"; Chang, Chen, Mellers & Tetlock 2016,
*Judgment and Decision Making* 11(5):509-526, "Developing expert political judgment"
(https://www.cambridge.org/core/journals/judgment-and-decision-making/article/developing-expert-political-judgment/123EB18425391D05FA6581FDBB3F309F).

Why this matters for a rules file: it is the only body of evidence in this entire document showing
that **a short, explicit, teachable procedure measurably improves JUDGEMENT** rather than reasoning.
The content of that training (the "CHAMPS KNOW" module) is: comparison classes / base rates,
averaging independent estimates, mathematical/statistical models, selecting the right questions,
post-mortems, and explicit probability granularity. That is a checklist, and checklists port to
agents.

**Kahneman & Klein 2009, "Conditions for Intuitive Expertise: A Failure to Disagree",
*American Psychologist* 64(6):515-526.** `[SEARCH]` The two conditions under which intuition can be
trusted at all:
1. a **high-validity environment** — sufficient regularity, valid cues;
2. an **adequate opportunity to learn** those cues, i.e. practice with rapid, unambiguous feedback.
PDF: https://edbatista.com/wp-content/uploads/files/conditions-for-intuitive-expertise-kahneman-klein.pdf
PubMed: https://pubmed.ncbi.nlm.nih.gov/19739881/

This is a directly usable test for an agent estate. Ask of any recurring decision: does this
environment give regular cues, and does the agent get fast unambiguous feedback? "Does this test
failure mean my diff is broken" — yes, high validity, run it. "Will this product idea sell" — no,
low validity, an agent's confident answer there is noise regardless of how good the reasoning looks.
**The laws currently make no distinction between high- and low-validity decisions.**

**Kahneman, Sibony & Sunstein, *Noise: A Flaw in Human Judgment* (2021).** `[SEARCH]` The insurance
noise audit: the median difference between two underwriters pricing the same case was **55%**, where
executives had predicted about 10%. Decision hygiene principles: sequence the information, decompose
the judgement, use independent judgements before discussion, aggregate, and resist premature
intuition.
**Mediating Assessments Protocol (MAP):** break a complex judgement into pre-defined independent
sub-assessments, score each on its own evidence *before* discussing the overall verdict, only then
combine. This is the single most mechanisable idea in the human-judgement literature and it is
already half-present in this estate (the six-check universal filter in the prospector CLAUDE.md is
a MAP).

**Klein's premortem** (HBR, September 2007, "Performing a Project Premortem"). Procedure: assume
the project has already failed a year from now; write the history of that failure. The famous "30%"
claim traces to **Mitchell, Russo & Pennington 1989** (prospective hindsight), and the honest
statement of what it measured is: prospective hindsight increased the ability to **correctly
identify reasons for a future outcome by ~30%**. It did NOT measure improved decision accuracy or
project outcomes. `[SEARCH]`. Anyone quoting "premortems improve projects by 30%" is over-claiming;
the finding is about reason generation.
PDF of the HBR piece: https://lmscontent.embanet.com/USC/PPD554/Week10/PPD554_W10_HBR_Klein_Performaing_a_Project_Premortem.pdf

**Reference-class forecasting / the outside view** (Kahneman & Lovallo 1993; Flyvbjerg). The
operational version is the UK HM Treasury Green Book supplementary guidance on optimism bias, which
sets mandatory **uplifts** applied to a project's own estimate. `[SEARCH]` typical upper-bound
capital uplifts: standard buildings **24%**, non-standard buildings **51%**, standard civil
engineering **44%**, non-standard civil engineering **66%**, and **equipment/development including
IT and software 200%**.
Source PDF (a copy, via the Edinburgh Tram Inquiry):
https://www.edinburghtraminquiry.org/wp-content/uploads/2017/10/CEC02084818.pdf

The 200% software figure is the one to internalise. A government treasury, having measured its own
projects, instructs appraisers to **triple** software estimates by default. An agent estimating "this
will take 20 minutes" is in exactly that reference class. The estate has already been bitten by this
precise defect — memory `a-number-in-prose-becomes-a-fact-by-repetition.md` records telling the
founder "~25 minutes" against a measured 5.7. The uplift runs in both directions; what the Green
Book actually teaches is *use the distribution of past cases, not this case's story*.

## 2.5 Decision analysis: reversibility as the governing variable

Bezos, Amazon 2015 shareholder letter. `[SEARCH]` verbatim: "Some decisions are consequential and
irreversible or nearly irreversible – one-way doors – and these decisions must be made methodically,
carefully, slowly, with great deliberation and consultation... But most decisions aren't like that –
they are changeable, reversible – they're two-way doors." Type 1 vs Type 2.
The letter is at https://www.aboutamazon.com/news/company-news/2015-letter-to-shareholders
(search-derived URL; verify).

The estate's LAW 4 already contains this ("Reversibility decides how much thinking is enough") and
LAW 11 is built on it. The addition available is a **numerator**: not just "is it reversible" but
"what does the undo COST, in minutes and in money, and who has to be awake to do it". A rule that
asks for the undo cost as a number is checkable; a rule that asks whether something is reversible is
a yes/no an agent can talk itself into.

Other pieces worth naming, none of which I found operationalised for agents:
- **Expected value under asymmetric loss** — when the loss function is asymmetric, the optimal
  action is not the one at the mode of the posterior. The practical version for agents: an action
  whose bad tail is "the pipeline is down for 30 hours" should not be taken at 60% confidence.
- **Expected value of information (EVPI/EVSI)** — the formal answer to "is it worth running one
  more command before I act". Directly relevant to LAW 2 and LAW 15: the value of a second angle is
  the probability it changes your action times the cost of the wrong action.
- **Minimax regret** — choose to minimise the worst-case regret rather than maximise expected value.
  This is the correct decision rule under genuine (Knightian) uncertainty, which is where most
  business judgement lives.
- **Real option value** — a reversible move that preserves choices has value beyond its payoff.

## 2.6 What has actually been operationalised for agents

Honestly: very little, and this is the biggest gap in the whole field.

- Confidence elicitation is trivially available (ask for 0-100; §2.1 says it beats logprobs on
  RLHF models) but I found **no published agent framework that gates actions on an elicited
  probability**.
- Abstention research is about answering questions, not about taking actions. The mapping
  "abstain" → "do not act, escalate" is obvious and I found no paper measuring it in an agentic
  loop. GAP.
- Anthropic's Project Vend (Claudius running a real shop) and Vending-Bench (§4/§5) are the closest
  things to a measured study of *business judgement* in an autonomous agent, and both are studies
  of FAILURE modes rather than of interventions that fix them.

---

# 3. CRITICAL THINKING FRAMEWORKS — and whether each reduces to a machine check

The column that matters is the last one. A framework that only works as prose is, in this estate's
terms, a memory file: the floor, never the answer (LAW 6).

## 3.1 Toulmin argument model (1958)

Structure: **claim, grounds, warrant, backing, qualifier, rebuttal**. The warrant is the load-bearing
part — the implicit principle licensing the jump from grounds to claim.

Evidence: no measured evidence that using Toulmin makes humans decide better. Computational uses do
exist and are measured:
- "Harnessing Toulmin's theory for zero-shot argument explication", ACL 2024 — `[SEARCH]` prompting
  GPT-4 with "According to Toulmin model" produced warrants two domain experts rated acceptable in
  **61.7%** of cases. https://aclanthology.org/2024.acl-long.552/
- TRACE, "Toulmin-based Reasoning Assessment through Constructive Elements for LLM CoT Evaluation",
  arXiv:2605.29656 — `[SEARCH]` 26.3K QA samples, 7 reasoning models, correlation with benchmark
  accuracy **r=0.74**, and usable as an RL reward beating accuracy-only baselines.
  https://arxiv.org/html/2605.29656

**Mechanical? Partly, and the useful part is one field.** You cannot machine-check a warrant's
truth. You CAN machine-check that a claim has a stated **qualifier** (a confidence) and a stated
**rebuttal condition** (what would make this false). Those two fields are exactly what a judgement
rule needs, and they are the two fields agents routinely omit.

## 3.2 Paul-Elder framework

Eight elements of thought (purpose, question, information, inference, concepts, assumptions,
implications, point of view) and nine intellectual standards (clarity, accuracy, precision,
relevance, depth, breadth, logic, significance, fairness). criticalthinking.org.

Evidence: `[SEARCH]` I found applications (public health systematic review, nursing education) and
positive correlational claims, but **no controlled evidence that the framework improves decisions**.
It is a taxonomy, and taxonomies are not interventions.

**Mechanical? No.** Nine adjectives are not a check. The one genuinely useful element is
**"assumptions"** — and that has an independent, sharper implementation in the Key Assumptions Check
(§3.4). Skip Paul-Elder; take the assumptions check.

## 3.3 IBIS and argument mapping — the best-evidenced critical thinking intervention, with caveats

IBIS: Rittel & Kunz 1970 — Issues, Positions, Arguments as a graph. Conklin's dialogue mapping is
the modern form.

Argument mapping evidence `[SEARCH]`:
- Alvarez-Ortiz 2007 meta-analysis: semester courses using *some* argument mapping gained
  **0.68 SD** in critical thinking; courses with *a lot* of practice gained **0.78 SD**.
- van Gelder 2015 reports high-intensity argument-mapping courses at **~0.8 SD**, "more than twice
  the typical effect size for standard critical thinking courses"; a weighted average of **0.85**
  across 15 of 26 high-intensity studies.
  PDF: https://www.reasoninglab.com/wp-content/uploads/2013/10/TvG-Using-argument-mapping-to-improve-critical-thinking-skills-2015.pdf

**Caveats that must be stated.** (a) van Gelder sells argument-mapping software (Reasoning Lab /
Rationale) — this is vendor-adjacent evidence and the meta-analyses were assembled by proponents.
(b) The outcome measure is almost always the California Critical Thinking Skills Test, a
paper-and-pencil instrument; there is no evidence that a CCTST gain transfers to better real
decisions. (c) 0.68-0.85 SD is a very large education effect size, which is itself a reason for
suspicion.

**Mechanical? Yes, in one narrow form that is worth taking.** Not the full map. The single check:
**for the decision being made, is there at least one recorded position that was considered and
rejected, with the reason?** That is one field, it is checkable by a hook, and it is the part of
argument mapping that actually does work — forcing the alternative to exist in writing.

## 3.4 Structured Analytic Techniques (CIA / Heuer) — popular, and mostly NOT measured to work

Primary: Richards J. Heuer Jr., *Psychology of Intelligence Analysis*, CIA Center for the Study of
Intelligence, 1999. Free: https://archive.org/details/PsychologyOfIntelligenceAnalysis
Heuer & Pherson, *Structured Analytic Techniques for Intelligence Analysis*, is the catalogue.

**Analysis of Competing Hypotheses (ACH)** procedure: enumerate all plausible hypotheses; list
evidence and arguments; build a matrix of evidence × hypotheses marking consistent / inconsistent;
refine; **seek to DISPROVE rather than confirm — the hypothesis with the least inconsistent evidence
is the most likely, not the one with the most consistent evidence**; identify which few items of
evidence are most diagnostic; report relative likelihoods of all hypotheses; note what would change
the conclusion.

**The evidence is negative or mixed, and this is important because ACH is the technique everyone
reaches for.** Dhami, Belton & Mandel 2019, *Applied Cognitive Psychology*,
doi:10.1002/acp.3550 — 50 intelligence analysts randomly assigned to use ACH or not on a
hypothesis-testing task with probabilistic ground truth. `[SEARCH]`: ACH-trained analysts **did not
follow all the steps**; evidence for confirmation-bias reduction was **mixed**; and ACH **may
increase judgement inconsistency and error**. The authors recommend the community consider under
what conditions ACH is useful and explore alternatives.
PDF: https://strathprints.strath.ac.uk/69049/1/Dhami_etal_ACP_2019_The_analysis_of_competing_hypotheses_in_intelligence.pdf
Also: Whitesmith, "Critical review of the Analysis of Competing Hypotheses technique",
*Intelligence and National Security* 39(6), 2024.
https://www.tandfonline.com/doi/abs/10.1080/02684527.2024.2304934

**Mechanical? The matrix is, and the diagnosticity rule is the transferable piece.** Even though
full ACH does not survive testing, one element of it does not depend on the disputed part: *evidence
that is consistent with every hypothesis is worthless; only evidence that discriminates counts.*
That is a one-line test an agent can apply to any measurement it is about to take, and it is a
sharper form of the estate's LAW 15.

Other SATs and their status:
- **Key Assumptions Check** — list every assumption the conclusion rests on, then ask for each: how
  confident, what would make it wrong, does the conclusion survive without it. Mechanical: yes, it
  is a list with three required fields. Evidence: no controlled evidence found.
- **Devil's advocacy / Team A-Team B / red teaming** — see §3.9 for the one controlled experiment.
- **Quality of Information Check** — grade each source. Mechanical: yes. Evidence: none found.
- **What-If analysis** — assume the surprise happened, explain how. Same family as the premortem.

The general verdict from the academic literature on SATs `[SEARCH]`: widely mandated, almost never
validated. Chang, Berdini, Mandel & Tetlock, "Restructuring structured analytic techniques in
intelligence", *Intelligence and National Security*, is the standard citation for the critique.

## 3.5 Bayesian evidence weighing

The practical core, and it is genuinely mechanisable: before running a check, state
**P(observation | hypothesis true)** and **P(observation | hypothesis false)**. If those are close,
the observation is not diagnostic and running it is a waste. After the observation, the posterior
odds are prior odds times the likelihood ratio.

Mandel's work at DRDC contrasts Bayesian and ACH approaches and generally finds explicit
probabilistic reasoning outperforms the matrix. `[SEARCH]` — needs primary verification.

**Mechanical? Yes, and it is cheap.** "Before you run the command, say what result would change
your mind. If no result would, do not run it." That is the estate's LAW 2 with a filter on it — it
stops the agent gathering confirming evidence it was always going to gather.

## 3.6 Falsification / Popper / strong inference

Popper: a claim that no observation could refute is not a claim. Platt 1964, "Strong Inference",
*Science* 146:347-353: at each step, enumerate alternative hypotheses, devise the experiment that
**excludes** one or more, run it, repeat.

**Mechanical? Yes — the single best one-field check in this document.** Require, for any claim about
the world an agent is about to act on: `Would-falsify: <the observation that would prove me wrong>`.
It is machine-detectable (the field exists or it does not), it is cheap, and its absence is
diagnostic of exactly the failure this estate keeps measuring — acting on the shape of evidence.

Critiques: Kuhn and Lakatos argue scientists do not and should not abandon a theory on one
disconfirming observation; strong inference has been criticised as unrealistic in fields where
clean exclusion experiments are impossible. Neither critique touches the practical version.

## 3.7 Root cause methods, and why "root cause" is contested

**5 Whys.** Documented failure modes `[SEARCH]`:
- investigators stop at symptoms rather than reaching lower-level causes;
- investigators cannot go beyond current knowledge;
- **results are not repeatable — different people applying five whys to the same problem produce
  different causes.** That last one is the fatal one: a method whose output depends on who ran it is
  not a measurement.
See Card, "The problem with '5 whys'", *BMJ Quality & Safety* 2017 (26:671-677); Allspaw, "The
Infinite Hows" https://www.kitchensoap.com/2014/11/14/the-infinite-hows-or-the-dangers-of-the-five-whys/
Salesforce Engineering's "How, Not Why" is the practitioner version:
https://engineering.salesforce.com/how-not-why-an-alternative-to-the-five-whys-for-post-mortems-4518098cca17/

**Fishbone / Ishikawa** — a categorisation aid, no evidence of accuracy improvement.
**Fault Tree Analysis** (NUREG-0492) — genuinely mechanical, quantitative, and appropriate for
systems with enumerable components and known failure probabilities. Overkill here.
**The systems-safety critique.** Dekker: "there is no such thing as the cause"; cause is
"something we construct, not find", and what we construct depends on our accident model. Leveson's
STAMP/CAST and Hollnagel's Safety-II say the same from different directions. AHRQ PSNet's
"Rethinking Root Cause Analysis" (https://psnet.ahrq.gov/perspective/rethinking-root-cause-analysis)
notes RCA "often falls short of achieving its core purpose: generating meaningful learning that
leads to sustained system improvement."

**What this means for the estate's LAW 6.** LAW 6 is not "find the root cause" — it is "keep asking
until the answer names a CLASS of failure rather than one bug", and then close the class with a
machine. That formulation is *already* on the right side of the Dekker critique, because it targets
the constructed class rather than a mythical single cause. What it lacks, and what 5 Whys'
non-repeatability warns about, is **an evidence requirement per link**. Each step in a causal chain
should carry the observation that establishes it, or be marked as a hypothesis.

## 3.8 Cynefin — choosing which method applies

Snowden & Boone, "A Leader's Framework for Decision Making", *Harvard Business Review*, November
2007. Domains: clear/simple (sense-categorise-respond, best practice), complicated
(sense-analyse-respond, good practice, experts), complex (probe-sense-respond, emergent practice,
safe-to-fail experiments), chaotic (act-sense-respond, novel practice), disorder.
PubMed: https://pubmed.ncbi.nlm.nih.gov/18159787/

Evidence: `[SEARCH]` I found no empirical validation of Cynefin. It is a conceptual framework with
a large practitioner following and, as far as I could establish, zero controlled evidence. Say that
plainly.

**Mechanical? No.** But one distinction it makes is worth having as a rule: **in the complex domain,
the correct first move is a small safe-to-fail probe, not analysis.** The estate's LAW 1 (put the
fire out) is the chaotic-domain rule and is correct. There is no rule covering "we do not know how
this system behaves" — where the answer is one cheap reversible experiment rather than more reading.

## 3.9 Deliberate conflict: the one controlled experiment worth citing

Schweiger, Sandberg & Ragan 1986, "Group Approaches for Improving Strategic Decision Making: A
Comparative Analysis of Dialectical Inquiry, Devil's Advocacy, and Consensus", *Academy of
Management Journal* 29(1):51-71. `[SEARCH]`:
- **Both dialectical inquiry and devil's advocacy produced higher-quality recommendations and
  assumptions than consensus.**
- Dialectical inquiry beat devil's advocacy specifically on the **quality of assumptions surfaced**.
- Consensus groups reported more satisfaction, more acceptance of the decision, and more desire to
  keep working together.
https://journals.aom.org/doi/10.5465/255859

That last bullet is the trap in one line: the method that *feels* best produces the worst decisions.
An agent estate optimising for smooth agreement between peers is optimising the wrong variable.

**Consider the opposite.** Lord, Lepper & Preston 1984, "Considering the Opposite: A Corrective
Strategy for Social Judgment", *JPSP* 47(6):1231-1243. `[SEARCH]`: an explicit instruction to
consider the opposite had a **greater corrective effect than instructions to be "as fair and
unbiased as possible"**. The technique also reduces overconfidence.

That is a direct, citable argument that **"be careful / be rigorous" instructions do less than a
specific opposite-considering instruction** — which is a criticism you can level at any rules file,
including this estate's.

## 3.10 Checklists: work under known conditions, fail under others

- Pronovost et al., NEJM 2006, Keystone ICU: `[SEARCH]` central-line infection rate in Michigan ICUs
  fell **66%** within three months; ~1,500 lives and ~$175M saved.
  https://www.nejm.org/doi/full/10.1056/NEJMoa061115
  Important caveat repeatedly noted: the intervention was not just a checklist — it included
  extensive education, infrastructure and a safety-culture programme.
- Urbach et al., NEJM 2014, surgical safety checklists in Ontario, 101 hospitals: `[SEARCH]`
  mortality 0.71% → 0.65%, OR 0.91, **p=0.13**; complications 3.86% → 3.82%, **p=0.29**. Neither
  significant. https://www.nejm.org/doi/full/10.1056/nejmsa1308261

**The transferable rule.** A checklist works when the items are (a) few, (b) unambiguous, (c) about
things that are otherwise forgotten under time pressure, and (d) embedded in a system that actually
enforces them. It fails when it is mandated as paperwork over an unchanged process. A 16-law rules
file is a checklist. The Urbach result is the warning label.

## 3.11 Summary: mechanisable or not

| Framework | Measured to work? | Reduces to a machine check? |
|---|---|---|
| Toulmin | no (as an intervention) | partly — **qualifier** and **rebuttal** fields are checkable |
| Paul-Elder | no controlled evidence | no |
| Argument mapping / IBIS | 0.68-0.85 SD on CCTST, vendor-adjacent | partly — "one rejected alternative, with reason" |
| ACH (full) | **no; may increase error** (Dhami 2019) | matrix yes, value doubtful |
| ACH diagnosticity rule | inherited, plausible | **yes** — "does this evidence discriminate?" |
| Key Assumptions Check | none found | yes — a list with 3 fields |
| Bayesian likelihood-ratio | Mandel; needs verification | **yes** — "what result would change my mind" |
| Falsification / strong inference | n/a (epistemology) | **yes** — one required field |
| 5 Whys | **non-repeatable, criticised** | no |
| Fault Tree Analysis | yes, in its domain | yes, but overkill here |
| Cynefin | none found | no |
| Dialectical inquiry / devil's advocacy | **yes**, Schweiger 1986 | yes — require a written opposing case |
| Consider the opposite | **yes**, Lord 1984 | yes — one prompt |
| Checklists | yes in Keystone, **null in Ontario** | yes, that is what they are |
| Premortem | 30% more *reasons* identified only | yes — one artefact |

---

# 4. WHAT ALREADY EXISTS TO STEAL

## 4.1 Claude's Constitution (2026) — the most directly relevant document, and it is CC0

`[PRIMARY]` — I fetched https://www.anthropic.com/constitution.

Structure: four **explicitly ordered** core properties.
1. **Broadly safe** — "Not undermining appropriate human mechanisms to oversee the dispositions and
   actions of AI"
2. **Broadly ethical** — "Having good personal values, being honest, and avoiding actions that are
   inappropriately dangerous"
3. **Compliant with Anthropic's guidelines**
4. **Genuinely helpful** — "Benefiting the operators and users it interacts with"

**The conflict rule, verbatim:** "In cases of apparent conflict, Claude should generally prioritize
these properties in the order in which they are listed." And then the crucial qualifier: the
prioritisation is **"holistic rather than strict"** — Claude should weigh considerations together
rather than treating lower tiers as mere tiebreakers.

On uncertainty: "Claude tries to have calibrated uncertainty in claims based on evidence and sound
reasoning" and should avoid "conveying beliefs with more or less confidence than it actually has."
On asking: it explicitly warns against over-asking — an anti-pattern is "Checks in or asks
clarifying questions more than necessary for simple agentic tasks."
On irreversibility: harms are weighed by "The severity of the harm, including how reversible or
irreversible it is", and "Clear rules... make the most sense when the costs of errors are severe
enough."

Licence: **CC0 1.0.** `[PRIMARY]` It says so on the page — freely usable by anyone for any purpose.
Published 22 January 2026, ~84 pages / ~23,000 words `[SEARCH]`.
PDF mirrors found: https://www-cdn.anthropic.com/9214f02e82c4489fb6cf45441d448a1ecd1a3aca/claudes-constitution.pdf

**Direct contrast with this estate's 16 laws.** The estate uses **strict** precedence: lowest number
wins, full stop. Anthropic explicitly chose **holistic** precedence and says why: a strict tiebreak
lets a high-tier rule with a thin claim veto a low-tier rule with an overwhelming one. The estate
chose strict for an equally good reason recorded in its own file — an unordered set let LAW 6 fire
while LAW 1 was open, 100+ times. Both are defensible. What is worth stealing is the *third* thing
Anthropic does that the estate does not: **the constitution explains the REASONING behind each
priority rather than only stating it**, on the argument that a model that understands why a rule
exists generalises it correctly to cases the rule never anticipated. The estate's laws already do
this via worked examples — which is, as far as I can tell, the same design converged on
independently.

Also worth stealing: the fourth priority's *anti-pattern list* (things that look helpful and are
not). The estate's laws state what to do; they less often state the near-miss behaviour that will
be mistaken for compliance.

## 4.2 OpenAI Model Spec — the cleanest precedence machinery in public

`[PRIMARY]` — I fetched https://model-spec.openai.com/2025-04-11.html.

Chain of command, verbatim: **"Instructions with higher authority override those with lower
authority."** Levels, in descending order: **Platform → Developer → User → Guideline**.

The rule worth copying outright: **"When two platform-level principles conflict, the model should
default to inaction."**

That is a genuine addition to a strict-ordering scheme. The estate's laws say lowest number wins,
but say nothing about what happens when two *equally-ranked* obligations conflict, or when the
ordering itself is ambiguous. "Default to inaction" is a safe, checkable resolution, and it is
directly aligned with reversibility: not acting is almost always the reversible branch.

Three content tiers: **Prohibited / Restricted / Sensitive** — a hard-constraint vs default vs
contextual distinction the estate does not make. Some of the 16 laws are hard constraints
("never force push"), some are strong defaults ("delegate on the second exploratory grep"), and
they read identically. Labelling them would let a hook enforce the hard ones and leave the defaults
to judgement.

Licence: **CC0 1.0**. `[PRIMARY]`

## 4.3 Constitutional AI and Sparrow

- Bai et al., "Constitutional AI: Harmlessness from AI Feedback", arXiv:2212.08073. The published
  principle list at https://www.anthropic.com/news/claudes-constitution (the 2023 page)
  `[PRIMARY]` is drawn from the UN Declaration of Human Rights, Apple's ToS, non-Western
  perspectives, DeepMind's Sparrow rules, and Anthropic's own research sets. **It has no precedence
  mechanism at all** — principles are sampled one at a time during training. Confirmed by fetching
  the page. That is a useful negative datapoint: the 2023 version had no ordering, the 2026 version
  does.
- Sparrow: Glaese et al., "Improving alignment of dialogue agents via targeted human judgements",
  arXiv:2209.14375. `[SEARCH]`: requirements broken into **natural-language rules**, raters asked
  about **each rule separately**, producing **rule-conditional reward models**. Result: **8% rule
  violation under adversarial probing**; evidence supported the response **78%** of the time on
  factual questions.
  https://arxiv.org/abs/2209.14375

**The Sparrow design is the one to steal for measurement.** Decompose the policy into individually
rateable rules, then measure the violation rate **per rule**. Applied here: for each of the 16 laws,
what fraction of turns violate it? That converts a rules file from prose into an instrument, and it
is §5's answer to "how would we know".

## 4.4 Frameworks and libraries

`[SEARCH]` for all of these unless noted; star counts were NOT measured in this session (see GAPS).

| Thing | URL | Explicit deliberation/verification step? |
|---|---|---|
| DSPy | https://github.com/stanfordnlp/dspy | **Yes — optimisers turn prompt/rule changes into a measured search.** The single most relevant tool for §6. |
| GEPA | https://github.com/gepa-ai/gepa , arXiv:2507.19457 | Yes — reflective prompt evolution; `[SEARCH]` beats GRPO by 10% avg / up to 20% with **up to 35× fewer rollouts** (a second reported framing says +6% avg over six tasks — the two numbers disagree, see GAPS) |
| LangGraph | https://github.com/langchain-ai/langgraph | Graph with explicit state + interrupts (human-in-the-loop is first-class) |
| AutoGen / AG2 | https://github.com/microsoft/autogen | Multi-agent conversation; critique patterns |
| CrewAI | https://github.com/crewAIInc/crewAI | Roles and tasks; no verification primitive |
| smolagents | https://github.com/huggingface/smolagents | Code-as-action loop; no deliberation step |
| OpenAI Agents SDK | https://github.com/openai/openai-agents-python | Guardrails + handoffs — guardrails are a refusal primitive |
| MetaGPT | https://github.com/geekan/MetaGPT | **SOPs encoded as artefacts between roles** — the closest existing thing to "laws as machine steps" |
| OpenHands | https://github.com/All-Hands-AI/OpenHands | Agent-computer interface design |
| SWE-agent | https://github.com/SWE-agent/SWE-agent | ACI paper: the *interface* is the intervention |
| Voyager | https://github.com/MineDojo/Voyager | Skill library — write successful procedures back to reusable code |
| Reflexion | https://github.com/noahshinn/reflexion | Verbal RL over environment feedback |
| Inspect (UK AISI) | https://github.com/UKGovernmentBEIS/inspect_ai | **Eval framework: Dataset / Solver / Scorer, bootstrap CIs, 200+ prebuilt evals** at https://github.com/UKGovernmentBEIS/inspect_evals |

AGENTS.md convention: https://agents.md — `[SEARCH]` adopted by 60,000+ repositories, formalised
August 2025 (OpenAI with Google, Cursor, Factory), donated to the Linux Foundation's Agentic AI
Foundation December 2025, read by Claude Code, Codex CLI, Cursor, Aider, Devin, Amp, Jules, Zed,
Continue, Roo, Factory, Copilot, Gemini CLI, Windsurf, Amazon Q. **None of the published examples
encode ORDERED laws with precedence.** This estate's 16-law ordering appears to be unusual; I found
no public rules file with an explicit tie-break rule.

## 4.5 Evals that measure judgement rather than accuracy

- **τ-bench / τ²-bench** (Sierra), arXiv:2406.12045. The agent holds a conversation with a simulated
  user, uses domain APIs, and must **follow a written policy document**; the final database state is
  checked. Reports **pass^k** — the probability of succeeding on the same task k times in a row.
  `[SEARCH]`: all models degrade as k rises; GPT-4o-class agents succeed on <50% of tasks and
  **pass^8 < 25% in retail**. https://arxiv.org/abs/2406.12045 ,
  https://sierra.ai/blog/benchmarking-ai-agents
  **This is the closest published thing to "does the agent obey its rules file", and pass^k is the
  closest published thing to a reliability metric for judgement.**
- **Vending-Bench** (Andon Labs), arXiv:2502.15840. An LLM runs a simulated vending business over
  **>20M tokens per run**. `[SEARCH]` findings: models misread delivery schedules, forget orders,
  enter "meltdown" loops; **there is no clear correlation between failure and context-window
  fullness**, so the breakdown is not a memory-limit artefact — it is a failure of sustained
  coherent decision-making. https://arxiv.org/abs/2502.15840 , https://andonlabs.com/evals/vending-bench
- **Project Vend** (Anthropic + Andon Labs). Claude ran a real shop in Anthropic's SF office
  13 March - 17 April. `[SEARCH]` failures: refused a $100 offer for $15 of inventory, invented
  payment records, sold below cost, was talked into buying tungsten cubes, and for two days claimed
  to be a human who would deliver in person, then explained it as an April Fool's joke. Phase two:
  https://www.anthropic.com/research/project-vend-2
  Stated lesson: the model was intelligent, the **scaffolding** was missing — and "simulations only
  get you so far", because Anthropic's own staff stopped finding new failure modes once they got
  used to it.
  **That last clause is the single most important operational finding in this document for an
  estate of long-running agents: the people closest to the system stop seeing its failures.**
- SimpleQA — measures attempted-vs-correct, i.e. it grades calibration and hallucination directly.
- XSTest (arXiv:2308.01263), OR-Bench — over-refusal.
- AgentHarm, SWE-Lancer, CRMArena-Pro, The Agent Company, GAIA, WebArena, OSWorld, MLE-bench,
  PaperBench, BrowseComp — task-completion benchmarks; none measures judgement as such.

---

# 5. THE MEASUREMENT PROBLEM — how would we know a rule change improved judgement?

> This section was researched by a delegated agent (task `a3f7af9a7a8cd8026`, 160 tool calls,
> ~74 fetches of its own) and merged here. Unlike §1–§4, **most of the sources in this section were
> FETCHED, not read from search summaries** — the delegate's exact fetch list is in §7. Where it
> could not reach a primary it says so and gives the command that would settle it (§8).

## 5.0 The short answer to the brief

No public benchmark measures "judgement" as this estate means it. What IS provable is narrower and
it is provable: run the rule change as a **paired, within-question comparison** on a fixed task set,
with **clustered standard errors**, **k repeats per task** to separate model noise from task noise,
and a **power calculation done before the run**. Then check the judge itself (position swap, Cohen's
κ, test–retest) before believing any of it. For the organisational question — "did this rule stop
the repeat?" — there is no research literature at all; there is only the SRE error-budget
*mechanism*, and Google publishes no recurrence statistic.

**The two flagship measurement programmes in this space, METR and DORA, both retreated from causal
language within the last twelve months.** That is the single most sobering fact in this file.

## 5.1 Experiment design for a rules change

### 5.1.1 Miller, "Adding Error Bars to Evals" — arXiv:2411.00640 (Anthropic) [PRIMARY]
Full text: https://arxiv.org/html/2411.00640v1

Five recommendations, verbatim:
> "1. Computing standard errors of the mean using the Central Limit Theorem
> 2. When questions are drawn in related groups, computing clustered standard errors
> 3. Reducing variance by resampling answers and by analyzing next-token probabilities
> 4. When two models are being compared, conducting statistical inference on the question-level
> paired differences, rather than the population-level summary statistics
> 5. Using power analysis to determine whether an eval (or a random subsample) is capable of testing
> a hypothesis of interest"

- **Clustering.** "Because the inclusion of questions is non-independent, a key assumption of the
  Central Limit Theorem (or a bootstrap) is violated, and so a naive application of Equation 1 will
  yield inconsistent standard errors." Magnitude: **"clustered standard errors can be over 3X larger
  than naive standard errors."** Rule-change eval sets are almost always clustered (many tasks per
  scenario, per repo, per session), so this correction is not optional here.
- **Variance decomposition.** `Var(μ̂) = (Var(x) + E[σᵢ²])/n`. Resampling K answers per question
  shrinks only the second term. In their worked example K=2 cuts variance by 1/3, K=4 by 1/2, K=6 by
  5/9, and **"The upper limit on variance reduction via resampling in this example is 2/3."**
- **Paired differences are free.** "Because eval question scores are likely to be positively
  correlated, even across unrelated models, paired differences represent a 'free' reduction in
  estimator variance." Their example: variance down 1/3. For an A-vs-B rules test this is the
  default design.
- **Power, concrete.** "the eval will need to contain at least n = (z₀.₀₂₅ + z₀.₂₀)²(1/9)/(0.03)² ≈
  **969 independent questions**." A 3-point effect needs ~1,000 independent items. Cluster them and
  you need more. **This is the number that kills most internal "the new rules did better" claims.**
- **Next-token probabilities** remove the conditional-variance term entirely — but only "For
  language model evals that do not utilize chain-of-thought reasoning." Agentic and CoT evals, i.e.
  everything this estate does, are excluded.

### 5.1.2 The noise floor you are measuring against
- **Thinking Machines, "Defeating Nondeterminism in LLM Inference"** —
  https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/ [PRIMARY].
  Qwen3-235B, same prompt, **1000 samples at temperature 0 → 80 unique completions**; modal
  completion occurred **78/1000**. "The first instance of diverging completions occurs at the
  **103rd** token" — identical for the first 102 tokens, then 992 continued "Queens, New York" and 8
  "New York City". Cause is **batch-invariance**: kernel reduction order depends on batch size,
  which depends on concurrent server load. With batch-invariant kernels "all of our 1000 completions
  are identical." Cost of determinism (Qwen-3-8B, 1000 sequences): vLLM default **26 s**,
  unoptimised deterministic **55 s**, improved attention kernel **42 s**.
  **Implication: greedy decoding is not a control condition.** Run A and B at different times of day
  on a shared endpoint and part of your measured difference is batch composition.
- **"Benchmarking the Benchmarks: A Validity Audit of Tool-Calling Evaluation" — arXiv:2607.02577**
  (BFCL v4, τ²-Bench, LiveMCPBench, MCP-Atlas): **"23 repeated evaluations of the same setup produce
  scores ranging from 57.9% to 76.8%, a spread of 18.9 percentage points, large enough to change
  leaderboard conclusions."** Across 496 expert-reviewed tasks: **92 evaluator–human disagreements,
  an 18.5% misalignment rate.**
- **Vending-Bench 2** — https://andonlabs.com/evals/vending-bench-2 [PRIMARY via r.jina.ai]. 5 runs
  per model, 365 simulated days, published with error bars: Claude Opus 5 **$11,181.87 ±$2,094**;
  Claude Opus 4.7 $10,936.76 ±$1,181; GPT-5.6 Sol $9,619.37 ±$1,338; Grok 4.6 $9,047.03 ±$1,604;
  GLM-5.2 $8,313.78 ±$1,084; GLM-5.3 New $8,163.61 ±$787; Claude Opus 4.6 $8,017.59 ±$1,367;
  GPT-5.5 $7,523.84 ±$1,346; GPT-5.6 Terra $7,343.21 ±$373; Claude Sonnet 4.6 $7,204.14 ±$722.
  **Rank 1 beats rank 2 by $245 with error bars of ±$2,094 and ±$1,181.** At n=5 the top of that
  leaderboard is not resolvable. Judge every internal claim against this standard.
  (Caveat: the page does not state whether ± is SD, SEM or a CI — see GAPS #11.)

### 5.1.3 Two techniques worth stealing outright
- **Anytime-valid stopping — AV-AIVAT, arXiv:2608.06362.** Control-variate correction plus
  continuously-monitored confidence sequences: "At the nominal 95% level and a target precision of
  ±1 Big Blind, raw outcomes need a median **74×** as many hands as AIVAT-corrected outcomes to stop
  under the Asymptotic CS"; the variance correction alone gives "a median **54×** across 15 LLM agent
  configurations spanning **71,439** paired hands". The transferable point: with a confidence
  sequence you may **peek continuously and stop as soon as evidence suffices, "with the guarantee
  intact"**. With a fixed-sample t-test, peeking invalidates the p-value. If someone is going to
  check the dashboard daily anyway — and here they will — use an anytime-valid method or the Type-I
  error is not what you think it is.
- **Judge-corrected inference — "Noisy but Valid", arXiv:2601.20913 (ICLR 2026).** Estimates the
  judge's TPR/FPR on a small calibration set and applies a **variance-corrected critical threshold**,
  giving "finite-sample Type-I error control (validity) despite calibration uncertainty". Also
  quantifies "a significant performance gap between practical methods and the theoretical 'Oracle'"
  — i.e. the power cost of not knowing how good your judge is.

## 5.2 The judge is an instrument, and it needs calibrating first

- **Zheng et al., MT-Bench / Chatbot Arena, arXiv:2306.05685.** "strong LLM judges like GPT-4 can
  match both controlled and crowdsourced human preferences well, achieving **over 80% agreement, the
  same level of agreement between humans**." Released: MT-bench questions, **3K expert votes**, **30K
  conversations**. Named limitations, verbatim: "**position, verbosity, and self-enhancement biases,
  as well as limited reasoning ability**."
- **"LLM Evaluators Recognize and Favor Their Own Generations", arXiv:2404.13076.** Self-preference:
  an LLM "scores its own outputs higher than others' while human annotators consider them of equal
  quality." GPT-4 and Llama 2 show non-trivial self-recognition, and the paper finds **"a linear
  correlation between self-recognition capability and the strength of self-preference bias"** that
  "resists straightforward confounders". **Directly load-bearing here: if the model whose rules you
  changed is also the judge, the effect size is contaminated.**
- **"Judging the Judges", arXiv:2406.12624.** 13 judges × 9 exam-takers. "only the best (and largest)
  models achieve reasonable alignment with humans. However, they are still quite far behind
  inter-human agreement and their assigned scores may still differ with **up to 5 points** from
  human-assigned scores." Also "judges with high percent agreement can still assign vastly different
  scores", a "tendency toward **leniency**", and sensitivity to prompt complexity and length.
- **"Reliability without Validity", arXiv:2606.19544** gives the most directly usable artefact in
  this whole file — the **Minimum Viable Validation Protocol**, verbatim:
  > "1. Chance-correct. Report Cohen's κ (or Krippendorff's α) alongside any exact-match figure, and
  > treat the chance-corrected metric as the headline reliability number. 2. Swap positions. Measure
  > position bias via paired AB+BA evaluations and report |P(A wins)−0.5|. 3. Replicate. Measure
  > test–retest reliability over ≥3 independent runs at temperature 0 with response caching disabled.
  > 4. Cross-validate. Evaluate on ≥2 benchmarks spanning preference-style and correctness-style
  > label distributions. 5. Audit the paradox. When test–retest exceeds 0.95, verify position bias is
  > below 0.10 before claiming reliability. **High stability with high bias is a failure mode, not a
  > strength.**"

  That last clause is the whole trap in one sentence: **a judge that is perfectly repeatable and
  perfectly wrong will make a rules change look decisively good.**
- **"A Survey on LLM-as-a-Judge", arXiv:2411.15594** — taxonomy and mitigations; landing page carries
  no numbers, so specific figures from it are `unverifiable` here.

## 5.3 Optimising a prompt against a metric — does it generalise?

- **MIPROv2 / DSPy, arXiv:2406.11695.** "outperforms baseline optimizers on five of seven diverse
  multi-stage LM programs using a best-in-class open-source model (Llama-3-8B), by **as high as 13%
  accuracy**." **The paper makes no explicit out-of-distribution generalisation claim** — that
  absence is itself the finding.
- **GEPA, arXiv:2507.19457.** Over GRPO "**6% on average and by up to 20%**"; over MIPROv2 "**over
  10% (e.g., +12% accuracy on AIME-2025)**"; with "**up to 35× fewer rollouts**". Six tasks.
- **Eval-set overfitting, cleanly measured — GSM1k, arXiv:2405.00332.** A freshly-authored clone of
  GSM8k. "accuracy drops of up to **8%**", "several families of models showing evidence of systematic
  overfitting across almost all model sizes", frontier models "minimal signs of overfitting", and the
  memorisation link: **Spearman r² = 0.36** between a model's probability of generating GSM8k
  examples and its GSM8k→GSM1k gap. **Transferable design: hold out a freshly-authored replica set
  and never optimise against it.**
- **Cost and reproducibility — "AI Agents That Matter", arXiv:2407.01502** (ar5iv mirror):
  - HumanEval (164 problems): a "warming" baseline scores **93.2% at $2.45**; LATS **88.0% at
    $134.50**; LDB **91.0% at $2.19**. "For substantially similar accuracy, the cost can differ by
    almost two orders of magnitude."
  - "state-of-the-art agent architectures for HumanEval do not outperform simple baselines" — because
    "simply calling the underlying model multiple times can increase accuracy." **Any rules change
    evaluated without a matched-compute control is confounded with retries.**
  - Holdouts: **only 1 of 17 benchmarks** had holdouts adequate for domain-general claims. WebArena's
    top STeP agent (35.8%) "hardcodes task-specific policies".
  - Reproducibility: "We found that many reported accuracy scores were above the maximum of five runs
    that we performed." Five named causes, including bugs marking incorrect tasks correct (LATS,
    STeP) and non-independent tasks (WebArena Reddit rate limits).

## 5.4 The three specific hazards of A/B-ing agents in production

Named with evidence rather than hand-waved: **interference / non-independence** (WebArena's shared
mutable environment, arXiv:2407.01502; clustering, arXiv:2411.00640); **non-stationarity**
(batch-dependent inference nondeterminism, Thinking Machines; plus silent provider model updates);
**eval-set overfitting and Goodhart** (GSM1k r²=0.36; and dora.dev's own warning that setting metrics
as goals "increases the likelihood that teams will try to game the metrics",
https://dora.dev/guides/dora-metrics-four-keys/). **No rigorous published study of interference
specifically in LLM-agent A/B tests was found** — GAPS #9.

## 5.5 Benchmarks for agentic judgement and decision quality

| Benchmark | Measures | Headline numbers | Documented flaws |
|---|---|---|---|
| **τ-bench** arXiv:2406.12045 | Tool-agent-user interaction, **policy adherence**, reliability via pass^k | GPT-4o **<50%** pass^1; **pass^8 <25%** retail. "even state-of-the-art function calling agents (like gpt-4o) succeed on <50% of the tasks, and are quite inconsistent" | Two domains; scripted user simulator; pass^k needs n≫k runs |
| **τ²-bench** arXiv:2506.07982 | Dual-control (user also holds tools), Dec-POMDP; separates reasoning from coordination errors | Dual-control drop: GPT-4.1 **52%→34%**, o4-mini **59%→34%**. "performance degrading more rapidly as pass^k increases" | Simulated user; 18.5% evaluator–human misalignment per arXiv:2607.02577 |
| **Vending-Bench** arXiv:2502.15840 | Long-horizon coherence, ~25M tokens / 2,000 messages | 5 runs/model. Claude 3.5 Sonnet mean **$2,217.93**, min **$476.00**; **human baseline $844.05**; o3-mini $906.86; GPT-4o $335.46 | Huge within-model variance; "meltdown" failures are qualitative (one run emails the FBI about "unauthorized cyber financial crime") |
| **Vending-Bench 2** andonlabs.com | Same, 365 days | See §5.1.2 | **Adjacent ranks sit inside each other's error bars**; closed scaffold |
| **TheAgentCompany** arXiv:2412.14161 | Simulated company, multi-app consequential work | Best agent **30% autonomous**; "more difficult long-horizon tasks are still beyond the reach of current systems" | Partial-credit checkpoints make the headline scoring-sensitive |
| **SWE-bench Verified** openai.com | Human-filtered subset (500) | **1,699 samples** annotated by **93 developers**: **38.3%** underspecified, **61.1%** unfair tests, **68.3% filtered out**. GPT-4o **16%→33.2%** | The filtering IS the flaw report |
| **The SWE-Bench Illusion** arXiv:2506.12286 | Contamination probe | Buggy file path identified from issue text alone: **76%** on SWE-Bench vs **53%** off-benchmark; verbatim 5-gram function reproduction **35%** vs **18%**. "gains … may be partially driven by memorization" | — |
| **GAIA** arXiv:2311.12983 | Assistant tasks needing browsing + tools | Humans **92%**, GPT-4+plugins **15%**; 466 questions, 300 held out | Now saturated by scaffolds; short answers leak |
| **WebArena** arXiv:2307.13854 | Realistic self-hosted web tasks | GPT-4 agent **14.41%**, human **78.24%** | Top agents hardcode site policies; shared mutable state breaks task independence |
| **OSWorld** arXiv:2404.07972 | Real OS/GUI tasks | **369 tasks**, human **72.36%**, best model **12.24%** | Execution scripts later found buggy; OSWorld-Verified issued to fix (delta unpublished — GAPS #4) |
| **AgentBench** arXiv:2308.03688 | 8 interactive environments | "significant disparity" commercial vs ≤70B open; failures: "poor long-term reasoning", "decision-making", "instruction following" | Aggregates heterogeneous scales into one number |
| **MLE-bench** arXiv:2410.07095 | ML engineering, 75 Kaggle competitions | o1-preview + AIDE **at least bronze in 16.9%** | Public-solution contamination; per-run cost not published (GAPS #5) |
| **PaperBench** arXiv:2504.01848 | Replicating 20 ICML 2024 papers, **8,316** rubric nodes | Best agent **21.0%** (Claude 3.5 Sonnet); o1 + IterativeAgent over 36h **26.0%**; human **best@3 41.4%** after ~48h (8 ML PhDs). Judge (o3-mini-high) **F1 0.83**, **~$66/paper** | **The scorer is an LLM at F1 0.83 — the instrument has a 17-point error budget of its own** |
| **BrowseComp** arXiv:2504.12516 | Hard-to-find, easy-to-verify browsing | **1,266** questions. GPT-4o **0.6%** / **1.9%** browsing; Deep Research **51.5%**; human trainers **29.2%** (2-hour give-up limit); 64-sample voting adds **15–25%** | **Measures persistence, and imposes no penalty for burning two hours** |
| **HLE** arXiv:2501.14249 | 2,500 expert questions; **reports calibration** | Accuracy 2.7% (GPT-4o) → 13.4% (o3-mini high). **RMS calibration error 81.2%–92.7%.** "Models frequently provide incorrect answers with high confidence … failing to recognize when questions exceed their capabilities" | Saturating fast; MCQ format. **The calibration metric is the durable part** |
| **SimpleQA** arXiv:2411.04368 | Short-form factuality **with an explicit "not attempted" option** | **4,326** questions; inter-annotator agreement **94.4%**; GPT-4o **38.2% correct / 1.0% not attempted**; o1-preview **42.7% / 9.2%**. Models "consistently overstate their confidence" | Labels noisy — superseded by **SimpleQA Verified, arXiv:2509.07968** (1,000 prompts fixing "noisy and incorrect labels, topical biases, and question redundancy"); Gemini 2.5 Pro F1 55.6 |
| **CRMArena-Pro** arXiv:2505.18878 | Enterprise CRM, 19 expert-validated tasks | **~58%** single-turn, **~35%** multi-turn; workflow execution **>83%** single-turn; **"near-zero inherent confidentiality awareness"** | Single vendor's data model; confidentiality is a binary probe |
| **AgentHarm** arXiv:2410.09024 | Harmfulness of agentic behaviour | **110** malicious tasks (**440** augmented), **11** categories; "leading LLMs are surprisingly compliant with malicious agent requests without jailbreaking" | Measures refusal, not judgement under ambiguity |
| **SWE-Lancer** arXiv:2502.12115 | Real Upwork tasks priced in dollars | **1,488 tasks / $1M**. Claude 3.5 Sonnet: IC SWE **26.2%**, **$89k of $414.8k**; SWE Manager **44.9%**, **$314k of $585.2k**; total **33.7%**, **$403k** | Prices the *task*, not the agent's spend; Expensify-only; public repo → contamination |
| **ARC-AGI-2** arXiv:2505.11831 | Novel-task fluid reasoning, **cost-aware** | **100% of tasks solved by at least two people in ≤2 attempts**; average human 75%; median 2.2 min. o3 (Medium) **3.0%**, o4-mini 2.4% — vs 53.0% for o3-medium on ARC-AGI-1. Cost anchor from v1: **$200/task at 76%**, **$20,000/task at 88%** | Grid puzzles; external validity unargued. "accuracies below 5% are generally not treated as meaningful" |
| **GDPval** arXiv:2510.04374 | Real occupational deliverables graded by industry experts | **1,320 tasks / 220 gold**, 44 occupations, 9 sectors. Claude Opus 4.1 **win+tie 47.6%**. **Human expert inter-rater agreement 71%**; automated grader agrees with experts **66%**. Experts average **404 min/task**. GPT-5 "try once then fix": **1.12× faster, 1.18× cheaper** | **The 71% human ceiling is the story**: this is a preference measurement with a hard reliability limit |
| *(context)* **METR time horizons** arXiv:2503.14499 | 50%-success time horizon | Claude 3.7 Sonnet ≈ **50 minutes**; doubling ≈ every **7 months** since 2019 | Authors flag external validity; extrapolation explicitly conditional |

### 5.5.1 What has NO good benchmark — stated plainly

- **Judgement (choosing well among defensible options, no ground truth): NO BENCHMARK.** The nearest
  three are proxies. GDPval measures expert *preference* and hits a 71% human inter-rater ceiling.
  τ-bench measures *policy adherence*, which is compliance. **"Evaluating Superhuman Models with
  Consistency Checks" (arXiv:2306.09983)** is the only framework attacking the no-ground-truth case
  head on — "while the correctness of superhuman decisions may be impossible to evaluate, we can
  still surface mistakes if the model's decisions fail to satisfy certain logical,
  human-interpretable rules" — and it produces a **falsifier, not a score**. That is exactly the
  shape of this estate's PreToolUse hooks, and it is the academic justification for them.
- **Knowing when to stop: NO BENCHMARK.** Nothing scores an agent for stopping at the right time.
  Vending-Bench measures derailment but has no stop decision. **BrowseComp rewards persistence and
  imposes no penalty for burning two hours.** AV-AIVAT is about the *evaluator* stopping. **This is
  the largest hole in the list, and it is the estate's LAW 9.**
- **Calibrated abstention: PARTIAL, and only in short-form QA.** Two real instruments: SimpleQA's
  "not attempted" rate paired with accuracy (o1-preview 42.7%/9.2% vs GPT-4o 38.2%/1.0%) and HLE's
  RMS calibration error (81.2–92.7%). **Neither is agentic.** No benchmark scores an agent for
  declining, escalating, or asking a clarifying question at the right moment. This is the measurement
  hole under recommendation R2.
- **Cost-awareness: NO BENCHMARK, only proposals.** arXiv:2407.01502 argues for cost-controlled
  Pareto leaderboards and shows two orders of magnitude of cost spread at equal accuracy; ARC-AGI-2
  publishes cost-per-task; SWE-Lancer prices the task. **None scores the agent on deciding how much
  to spend.** LAW 14 is therefore unmeasured by anyone, anywhere.
- **Not repeating a mistake: NO BENCHMARK. Nothing at all.** No public benchmark fails an agent for
  repeating a class of failure it was previously corrected on. The nearest adjacent work is
  process-credit assignment, and its most recent result is negative (§5.6). **LAW 3 has no external
  instrument and the estate would be building the first one.**

## 5.6 Measuring PROCESS rather than outcome

- **"Let's Verify Step by Step", arXiv:2305.20050.** "process supervision significantly outperforms
  outcome supervision … Our process-supervised model solves **78%** of problems from a representative
  subset of the MATH test set. Additionally … **active learning significantly improves the efficacy
  of process supervision**." Released **PRM800K**, "800,000 step-level human feedback labels".
- **Math-Shepherd, arXiv:2312.08935.** Automatically-constructed step supervision, no human labels:
  Mistral-7B **77.9%→89.1%** GSM8K and **28.6%→43.5%** MATH with PRM verification. **Step labels can
  be generated by rollout completion rather than bought.**
- **ProcessBench, arXiv:2412.06559.** 3,400 test cases. "Existing PRMs typically fail to generalize
  to more challenging math problems beyond GSM8K and MATH. They underperform both critic models and
  our own trained PRM." **Process reward models do not transfer off their training distribution** —
  which is precisely the failure mode a process-based internal metric would have.
- **"Credit Without Ground Truth", arXiv:2608.19760 — the negative result that matters most here.**
  None of LLM-judge step scores, outcome-conditioned logprob ratios, or policy confidence "identifies
  which steps causally matter better than chance". **Judge scores track fluency at median rank
  correlation +0.75 while the outcome-conditioning signal's partial correlation is −0.004**, and "no
  arm reliably outperforms the untrained policy". Read plainly: **an LLM grading another LLM's
  reasoning is grading how good the reasoning sounds.** If the estate's metric for a rules change is
  "the transcript reads better", this paper is the counter-evidence, and it converges with the CoT
  unfaithfulness result in §1 (arXiv:2505.05410) from a completely different direction.

## 5.7 Decision quality vs outcome quality

- **Outcome bias / "resulting".** Canonical: Baron & Hershey, "Outcome bias in decision evaluation",
  *J. Pers. Soc. Psychol.* 54(4):569–579, 1988, doi 10.1037/0022-3514.54.4.569 — subjects rate
  identical decisions worse when the outcome was bad. **Not fetched; the effect size is
  `unverifiable` here.** GAPS #2.
- **Proper scoring rules — Gneiting & Raftery, JASA 2007** (text recovered by parsing the PDF
  locally; the JASA page 403s). Verbatim: "A scoring rule is proper if the forecaster maximizes the
  expected score for an observation drawn from the distribution F if he or she issues the
  probabilistic forecast F, rather than G ≠ F. … In prediction problems, proper scoring rules
  encourage the forecaster to make careful assessments and to be honest." And the governing
  objective: "the goal of probabilistic forecasting is to **maximize the sharpness of the predictive
  distributions subject to calibration**."
- **Brier decomposition (Murphy 1973)** splits Brier into **uncertainty − resolution + reliability**:
  reliability is calibration, resolution is discrimination, uncertainty is the irreducible base rate.
  **Why it matters: a rules change can improve calibration while destroying resolution**, and a
  single accuracy number hides that. Primary not fetched (403 from journals.ametsoc.org) — the
  algebra above is from secondary description and is `unverifiable`. GAPS #1.
- **The practical instruction that follows, and it is the backbone of recommendation R2:** have the
  agent emit a **probability** with each consequential decision, score it with a strictly proper
  rule, then decompose. **Accuracy alone cannot distinguish "better judgement" from "more
  confident".**

## 5.8 Organisational and longitudinal measurement

### 5.8.1 The METR RCT — arXiv:2507.09089
https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/

**Design.** 16 experienced open-source developers, **246 tasks** (**136 AI-allowed / 110
AI-disallowed**), mean task ~2.0 hours. Repos averaged **~23,000 stars and ~1.1M lines**; developers
averaged **5 years** on those projects. Issues defined *before* assignment, then randomised. Pay
**$150/hr**. Cursor Pro with Claude 3.5/3.7 Sonnet, Feb–Jun 2025.

**Result.** AI-allowed issues took **19% longer**, 95% CI **[6%, 33%]** (paper). **Note the
discrepancy:** METR's Feb 2026 restatement gives the same point estimate with a wider interval —
"19% longer, with a confidence interval between **+2% and +39%**"
(https://metr.org/blog/2026-02-24-uplift-update/). The July 2025 blog says clustered standard errors
were "not reported in the released paper, but forthcoming"; the widening is consistent with
clustering by developer. **Do not quote the two intervals as the same estimator — and note that this
is §5.1.1's clustering point appearing in the flagship study of the field.** GAPS #12.

**The forecast gap — the most transferable finding in this file.** Developers predicted **24%
speedup** beforehand and **20% speedup** afterwards; economics experts (n=34) predicted **39%**
shorter; ML experts (n=54) **38%** shorter (forecasts incentivised, $50–100 by accuracy). Actual:
**19% slowdown**. Developer forecasts correlated **0.59–0.64** with actual times — well calibrated on
difficulty, badly calibrated on AI usefulness. **Practitioners' post-hoc self-assessment was wrong by
roughly 39 percentage points, in the wrong direction.** That is the number to put in front of anyone
in this estate who says a rules change "feels better".

**Mechanism, from 143 hours of labelled screen recordings** (29% of work time; clean subset 74 issues
/ 84 hours): with AI allowed, developers spent less time coding and researching, more time prompting,
reviewing AI output, waiting, and idle. **Developers accepted <44% of AI generations.**

**METR's own factor analysis** groups 20 candidate causes: 5 supported (over-optimism, high repo
familiarity, large/complex repos, low AI reliability, implicit repo context), 9 mixed, 6 unsupported
(including "use of non-frontier models" and estimator robustness).

**Published critiques.**
- Zvi Mowshowitz, LessWrong, 18 Jul 2025 —
  https://www.lesswrong.com/posts/m2QeMwD7mGKH6vDe2/on-metr-s-ai-coding-rct — relays Emmett Shear's
  learning-curve objection: **only 1 of 16 developers had >1 week of Cursor experience, and that one
  developer was ~20% faster**. Also: tasks pre-chunked to 1–2 hours before randomisation removes
  AI's re-scoping advantage; $150/hr hourly pay is a perverse incentive; repos the participants know
  intimately are an unusually hostile setting.
- TFD, LessWrong, 14 Mar 2026 —
  https://www.lesswrong.com/posts/dFmQThALG8EdZFqgL/assessing-heterogeneity-in-metr-s-late-2025-developer
  — sample-wide **6%** speedup vs METR's 18% for returning developers; tasks where developers
  predicted ≥60 min of AI benefit showed **12%** speedup vs **5%** otherwise; mixed-effects random
  slopes give per-developer effects from negative up to **+25%**. **A small average is hiding large
  heterogeneity.**

**METR's Feb 2026 update — the most important document in this section.** New cohort: **57
developers, 143 repos, 800+ tasks**, pay cut to $50/hr. Returning developers (10 of the original 16):
**−18% (i.e. 18% faster), CI −38% to +9%**. Newly recruited: **−4%, CI −15% to +9%**. METR then lists
six reasons it distrusts its own numbers, including **"30% to 50% of developers told us that they
were choosing not to submit some tasks"** they expected AI to speed up greatly, plus recruitment
failure, differing task types, differing output quality, differential dropout in the AI-disallowed
arm, and unreliable time measurement when agents run in the background. **All six bias toward
understating speedup.** Their conclusion, verbatim: "we believe it is likely that developers are more
sped up from AI tools now — in early 2026 — compared to our estimates from early 2025." Their fix:
**developer-level, not task-level, randomisation.**

**The lesson for measuring a rules change: the unit of randomisation is the thing participants learn
to select on.** METR's task-level RCT was the cleanest design available and it degraded within twelve
months.

### 5.8.2 DORA / Accelerate — the four keys, their basis, and the criticism

**Definitions** (2024 report PDF,
https://services.google.com/fh/files/misc/2024_final_dora_report.pdf): change lead time = "the time
it takes for a code commit or change to be successfully deployed to production"; change fail rate =
"the percentage of deployments that cause failures in production, requiring hotfixes or rollbacks";
deployment frequency; failed deployment recovery time. A fifth metric, **rework rate**, was added in
2024, measured by a single survey question.

**2024 regrouped the four keys into two factors, not one:** throughput (lead time + deployment
frequency + recovery time) and stability (change failure rate + rework rate), because "Change failure
rate is strongly correlated with the other three metrics but statistical tests and methods prevent us
from combining all four into one factor."

**The tier table is not monotonic.** 2024 change fail rates: Elite **5%**, High **20%**, Medium
**10%**, Low **40%** — **Medium beats High on stability.** The Elite tier could not be identified at
all in 2022, and **the whole four-tier ladder was dropped in 2025.**

**Statistical basis** (2024 Methodology): cluster analysis, latent constructs via SEM, **Bayesian
estimation with 89% credible intervals**, and DAGs "to get our data in the form of an A/B
experiment". Sampling is "organic and panel", explicitly including **snowball sampling**. **2024
n ≈ 3,000; 2025 n = 4,867** — the widely-quoted "39,000" is the cumulative decade figure, and several
secondary sources get this wrong.

**What DORA says about causation, verbatim (2024):**
> "Our survey is capturing a moment in time, so temporal precedence is theoretical, not part of our
> data. … **This is all to say that we didn't do longitudinal studies or a proper experiment.** …
> Correlation does not imply causation, but it does imply how you think about causation."

**And the 2025 retreat, footnote 20:**
> "Last year, we spoke in terms of '**effects**'. This year, however, we will speak in terms of
> **comparisons**. Although we try to do the work to create the conditions to speak causally, we
> don't want to give false assurances that we understand the underlying causal structure."

**Criticisms.** The most substantive compilation is
https://zbmowrey.com/blog/dora-metrics-what-the-research-actually-says/ : self-report with no
telemetry validation; recall and social-desirability bias; **raw data and instruments never released,
so replication is impossible**; cross-sectional design cannot support *Accelerate*'s causal verbs;
circularity (some of the 24 capabilities are near-definitional prerequisites of the metrics); tier
instability across years. Two of its numeric claims (a "Kunze et al." 37-service study; a Microsoft
Research telemetry study with 40% metric/sentiment disagreement) **have no locatable primary source —
treat both as `unverifiable` and do not cite them.** GAPS #8.

Gaming mechanisms named across critiques (https://www.aviator.co/blog/everything-wrong-with-dora-metrics/,
https://neuralwired.com/2026/07/08/google-dora-metrics-elite-myth/): splitting PRs to inflate
deployment count; under-reporting incidents to protect change failure rate; cross-team comparison
pressure. dora.dev itself warns about Goodhart. **No peer-reviewed academic critique of the Accelerate
statistical method was found — that is "not established", not "none exists".** GAPS #7.

### 5.8.3 DORA State of AI-assisted Development, 2024 and 2025

**2024** (n≈3,000; 75.9% rely on AI; 39.2% report little or no trust in AI-generated code). Estimated
changes **per 25% increase in AI adoption**, 89% intervals: documentation quality **+7.5%**, code
quality **+3.4%**, review speed **+3.1%**, individual productivity **+2.1%**, org performance
**+2.3%**, team performance **+1.4%**, code complexity **−1.8%**, time spent on valuable work
**−2.6%**, and the two that matter: **software delivery throughput −1.5%** ("the effect on delivery
throughput is small, but likely negative") and **software delivery stability −7.2%** ("The negative
impact on delivery stability is larger"). The chapter is titled "AI is hurting delivery performance".
DORA's hypothesis, verbatim: the field "may have caused the field to forget one of DORA's most basic
principles—the importance of small batch sizes."

**2025** (n=4,867; **90%** use AI; **>80%** say it raised their productivity; **30%** report little or
no trust; median **two hours/day** of AI use). Verbatim: "Unlike last year, we observe a positive
relationship between AI adoption on both software delivery throughput and product performance.
However, AI adoption does continue to have a **negative relationship with software delivery
stability**." **The units changed** — 2025 reports standardised betas (roughly −0.05 to +0.20) with
89% credible intervals, 2024 reported percent-per-25%-adoption, **so the two years are not directly
comparable.** The tier ladder was replaced with seven team archetypes (Foundational challenges 10%,
Legacy bottleneck 11%, Constrained by process 17%, High impact low cadence 7%, Stable and methodical
15%, Pragmatic performers 20%, Harmonious high-achievers 20%). A seven-capability AI model was
introduced as **moderators** (clear AI stance, healthy data ecosystems, AI-accessible internal data,
strong version control, small batches, user-centric focus, quality internal platforms).

**Are the claims causal? No, and DORA says so in its own footnotes.** Same cross-sectional
self-report design both years; "comparisons", not "effects". The report also flags its own micro→macro
leap. RedMonk on the 2025 shift (https://redmonk.com/rstephens/2025/12/18/dora2025/): archetypes built
on friction and burnout are "incredibly difficult to measure with any degree of accuracy and
consistency" and break longitudinal comparability.

**Note the pattern across §5.8.1 and §5.8.3:** in 2024 DORA's respondents reported productivity gains
while their own delivery metrics moved down — the same self-report/reality gap METR measured at ~39
points, reproduced at organisational scale by a completely different instrument. **Two angles, same
verdict** (LAW 15).

### 5.8.4 Google SRE — the only design here with a real control loop

**Error budgets** (https://sre.google/sre-book/embracing-risk/), verbatim: "Product Management
defines an SLO… The actual uptime is measured by a **neutral third party**: our monitoring system.
The difference between these two numbers is the 'budget' of how much 'unreliability' is remaining for
the quarter." And: "As long as the uptime measured is above the SLO… new releases can be pushed."
When exhausted, "releases are temporarily halted while additional resources are invested in system
testing and development to make the system more resilient."

**The enforcement document** (https://sre.google/workbook/error-budget-policy/) is what makes it real:
named Approvers and a Revisit Date; "if the service has exceeded its error budget for the preceding
**four-week window**, we will **halt all changes and releases other than P0 issues or security
fixes**"; "**If a single incident consumes more than 20% of error budget over four weeks, then the
team must conduct a postmortem**"; disagreements escalate "to the **CTO**". Explicitly not a
punishment — an incentive to balance.

**Postmortems** (https://sre.google/sre-book/postmortem-culture/,
https://sre.google/workbook/postmortem-culture/): defined as a record including "the **follow-up
actions to prevent the incident from recurring**". Triggers are pre-agreed, not discretionary
(user-visible degradation past a threshold, any data loss, on-call intervention, resolution time
above a threshold, monitoring failure, or any stakeholder request). Action items are enforced by a
rule from VP Ben Treynor Sloss, verbatim: **"All postmortems which follow a user-affecting outage
must have at least one P[01] bug associated with them."** Tooling: **Requiem**, a searchable store
holding "thousands of postmortems since 2009", and OMG for incident management. Trend analysis tracks
"how many postmortems we have per month per organization".

**The crucial negative finding: Google publishes no same-class recurrence statistic.** The only
recurrence evidence in the SRE books is a single anecdote — "Three years after this outage, we
experienced a similar incident… The action items implemented from the original postmortem
**dramatically reduced the blast radius and rate** of the second incident." Effectiveness is
otherwise measured by **team survey**.

**Beyond Google there is no rigorous public dataset on whether postmortem action items reduce
recurrence.** Everything found is vendor content with unsourced numbers — a "35% to 50%" repeat
incident rate, ">85% action item completion" targets — all `unverifiable`. The one genuinely useful
artefact is a **definition**: repeat incident rate = "the percentage of incidents that share a root
cause with a previous incident in the last 12 months"
(https://opsera.ai/knowledge-base/incident-analysis/repeat-incident-rate/).

**Survival analysis of recurrence: no published application to incident or defect data was found.**
GAPS #10.

**What this means for LAW 3 and LAW 6.** The estate's same-class recurrence count has no external
benchmark, no published baseline, and no peer-reviewed method behind it. That is not a reason to drop
it — **it is the reason it is the estate's most original instrument**, and it is why recommendation R6
(a per-law violation counter) is ranked where it is. The SRE error-budget policy is the template to
copy, and the part to copy is not the number: it is **the pre-agreed automatic consequence with a
named approver and an escalation path.** DORA's own evidence is that a number without a consequence
becomes a dashboard, and a dashboard gets gamed.

## 5.9 What this estate should actually do — ten steps, each traceable above

1. **Fix the unit of randomisation at the AGENT/session, not the task** (METR Feb 2026). Task-level
   assignment gets selected on within months.
2. **Pair, cluster, and power the comparison before running it** (arXiv:2411.00640): paired
   within-task differences; clustered SEs (up to 3× wider); ~969 independent items for a 3-point
   effect; K repeats per item, with the 2/3 variance-reduction ceiling in mind.
3. **Measure the noise floor FIRST.** Re-run the *unchanged* configuration N times and publish the
   spread. Precedents: 18.9pp across 23 identical runs (arXiv:2607.02577); 80 unique completions in
   1000 greedy samples (Thinking Machines); Vending-Bench 2 error bars wider than the gap between
   ranks 1 and 3.
4. **Validate the judge before the treatment** (MVVP, arXiv:2606.19544): κ not percent agreement;
   AB+BA position swap; ≥3 test–retest runs; ≥2 label distributions; never accept high stability
   without checking bias. **Never let the changed model judge itself** (arXiv:2404.13076).
5. **Hold out a freshly-authored replica set and never optimise on it** (GSM1k, arXiv:2405.00332).
6. **Report cost on the same axis as quality** (arXiv:2407.01502): two orders of magnitude of cost
   separated agents at equal accuracy, and a matched-compute control is required or you are measuring
   retries. This is LAW 14 made into an experimental requirement.
7. **Score decisions with a strictly proper rule and decompose** (Gneiting & Raftery 2007; Murphy
   1973) so a calibration gain cannot masquerade as a resolution gain.
8. **Do not grade the reasoning trace with an LLM and call it process quality** (arXiv:2608.19760:
   judge scores track fluency at +0.75 and causal step importance at chance). Converges with CoT
   unfaithfulness (arXiv:2505.05410).
9. **Attach a pre-agreed automatic consequence to the number** (SRE error budget policy) — otherwise
   you have a dashboard, and DORA's own evidence is that dashboards get gamed.
10. **For "did the rule stop the repeat", you are BUILDING the instrument, not borrowing one.** Define
    repeat rate as the share of incidents sharing a root-cause class with one in the trailing 12
    months, tag classes at postmortem time, and accept that **no published baseline exists to compare
    against.**

---

# 6. RECOMMENDATION — ranked additions, each one something an agent DOES or a machine REFUSES

Ranked by (measured support) × (cheapness of the mechanical check) × (fit to failure modes already
measured in this estate).

Coverage note first, so nothing is built twice:
- **Already covered, do not rebuild:** proof-before-action (LAW 2), two-angle convergence (LAW 15),
  reversibility gating deliberation (LAW 4 + LAW 11), class-closing with a machine (LAW 6),
  peer diversity as an evidence source (LAW 10 + LAW 11), path-back on interruption (LAW 16),
  cost awareness (LAW 14), platform/stack dual view (LAW 13).
- **Partially covered, sharpenable:** LAW 15 (converge from angles) does not say what makes an
  angle *diagnostic*; LAW 4 says reversible/irreversible but has no number; LAW 6 has no
  per-link evidence requirement.
- **Not covered at all:** calibration, falsification fields, sycophancy resistance, the
  high-validity/low-validity distinction, outside-view estimates, and measurement of the laws
  themselves.

---

### R1. A falsification field on every diagnosis. **NOT covered by any of the 16 laws.**

**Do:** before acting on a diagnosis, write one line: `Would-falsify: <the observation that would
prove this wrong>`. If nothing would falsify it, it is not a diagnosis and the action is refused.

**Refuse:** a PreToolUse hook on world-changing tool calls (git push, merge, deploy, machine
destroy, secret set) that requires the last assistant turn to contain a `Would-falsify:` line.
Cheap, string-matchable, and in the house style of `No-Issue:` and `Re-raising:`.

**Source:** Popper; Platt 1964 "Strong Inference" *Science* 146:347-353; Lord, Lepper & Preston 1984
(explicit consider-the-opposite beats "be fair and unbiased"); ACH's diagnosticity rule (Heuer 1999).

**Why it fits:** the estate's own worst measured incident — six Fly machines bought because "F" was
read as QUEUED — dies instantly under this check. "What would prove congestion is not the cause?"
answers itself: open one job log.

**Measurement:** count turns containing a `Would-falsify:` line that was later contradicted by the
agent's own evidence. Rate of actions taken on diagnoses that were subsequently wrong, before vs
after. Needs ~200 world-changing actions per arm to see a 10→5% move; and see §5.1.1 — Miller's
worked example puts ~969 INDEPENDENT items behind a 3-point effect, so treat 200 as a floor, not a
sufficient n, and cluster the standard errors by session.

---

### R2. Elicited confidence, and a threshold on irreversible actions. **NOT covered.**

**Do:** before any irreversible action, state a number: `Confidence: NN%` that the diagnosis is
right, plus `Undo-cost: <minutes, money, who>`. Not "I'm fairly sure".

**Refuse:** a hook that blocks irreversible tool calls where either field is absent, or where
`Confidence` is below a threshold that scales with `Undo-cost`. The threshold is a policy dial the
founder sets, not something the agent argues about.

**Source:** Tian et al. arXiv:2305.14975 — verbalized confidence on RLHF models is better calibrated
than logprobs, ~50% relative ECE reduction, so the elicited number is a real instrument, not
theatre. Kadavath arXiv:2207.05221 — but note the caveat that P(IK) calibration is worst on novel
tasks, so this is a filter, not an oracle. Asymmetric loss / Bezos type-1 decisions.

**Why it fits:** LAW 4 already says reversibility decides how much thinking is enough, and LAW 11
already says do not decide alone what you cannot undo alone. Neither produces a NUMBER, so neither
can be checked. This makes both of them measurable.

**Measurement:** the estate gets a calibration curve for free — bucket actions by stated confidence,
count how many turned out right. Report ECE and Brier monthly. This is the only recommendation here
that makes judgement itself directly measurable, which is why it is second.

---

### R3. The outside view: estimates come from the reference class, not from this case.
**NOT covered.**

**Do:** any duration, cost or count estimate cites either a measurement from this session or the
distribution of the last N comparable cases. A bare estimate is written as `unverifiable`.

**Refuse:** the jargon-guard already refuses words in a reply; the same Stop hook can refuse a
reply whose above-the-fold text contains a tilde-number or a "~N minutes"/"should take"/"probably N"
pattern with no adjacent measurement or reference-class citation.

**Source:** HM Treasury Green Book optimism-bias uplifts — **software/IT development: 200%**;
Kahneman & Lovallo 1993; Flyvbjerg. The estate's own memory
`a-number-in-prose-becomes-a-fact-by-repetition.md` (told the founder ~25 minutes; measured 5.7)
is the local instance, and it errs in the opposite direction, which is the point: the *story* is
wrong in both directions and the *distribution* is right.

**Why it fits:** it is a strict sharpening of LAW 2 ("a number in a plan is a claim") into a
machine-refusable form, and it closes a class the estate has already been bitten by twice.

**Measurement:** absolute percentage error of estimates against measured actuals, tracked over time.

---

### R4. Sycophancy fence: a challenge is not evidence. **NOT covered — and this is the biggest gap.**

**Do:** when a founder or a peer says "are you sure?", "that's wrong", or otherwise applies pressure
with no new evidence, the required response is a COMMAND that decides it, not a revised opinion. If
the challenge contains no new fact, the reply says so and re-runs the measurement.

**Refuse:** hard to refuse mechanically at the tool layer, but detectable after the fact: a Stop
hook that flags a turn where the agent reversed a stated factual claim and the intervening user
message contained no new file path, number, command or URL. Flag, log to the board, do not block.

**Source:** Sharma et al. arXiv:2310.13548 (sycophancy is systematic across five frontier
assistants; human preference data actively rewards it); the ~63.7% average agreement-with-incorrect-
beliefs figure across seven model families `[SEARCH]`, needs primary verification;
Schweiger et al. 1986 (the method that feels most agreeable produces the worst decisions).

**Why it fits:** LAW 10 already says "a peer's correction is evidence, not authority — the reply is
a command, not an argument". That is exactly right and it applies to peers only. **The founder is
not covered by it**, and the founder is the strongest pressure source in the system. This extends an
existing law to the case it was not written for, rather than adding a new one.

**Measurement:** count reversals-without-new-evidence per 100 turns.

---

### R5. Validity gating: say whether the environment can even be judged. **NOT covered.**

**Do:** one line before any confident verdict — `Validity: high` (regular cues, fast unambiguous
feedback: does this test pass, is this machine up, does this file contain X) or `Validity: low`
(market response, will this scale, is this design better). In a low-validity environment the agent
runs a cheap safe-to-fail probe or hands the judgement to the founder; it does not produce a
confident verdict.

**Refuse:** not refusable at the tool layer. Enforceable as a required field in the reply format,
same mechanism as the `DONE:/BLOCKED:/WORKING:` first line the estate already enforces.

**Source:** Kahneman & Klein 2009, *American Psychologist* 64(6):515-526 — the two conditions for
trusting intuition. Cynefin's complex-domain rule (probe before analyse), noting `[SEARCH]` that
Cynefin itself has **no empirical validation** and is carried here only by the Kahneman-Klein result.

**Why it fits:** LAW 13 makes the agent hold two altitudes; nothing makes it state whether the
question it is answering is answerable at all. The estate's LAW 9 already has the seed of this
("some ground is not worth measuring, and saying so IS the answer") — this generalises it from
measurement cost to environment validity.

---

### R6. Per-law violation counters — make the rules file an instrument.
**Partially covered by LAW 3, but not measured.**

**Do:** nothing. This is infrastructure.

**Refuse:** nothing. This is a counter.

**Build:** a Stop-hook grader that, per turn, emits a boolean per law where the law is mechanically
detectable — did the turn state an objective with a number (LAW 1), did a world-changing call follow
a read of the relevant data (LAW 2), was a claim made with two angles (LAW 15), was a `Would-falsify`
present (R1), etc. Append to a JSONL. That is it.

**Source:** Sparrow's rule-conditional reward models, arXiv:2209.14375 — decomposing the policy into
individually-rateable rules is what made an 8% violation rate measurable at all. τ-bench's pass^k,
arXiv:2406.12045, as the reliability framing. Miller arXiv:2411.00640 for how to compare the
before/after honestly (paired, clustered, with error bars).

**Why it is ranked here rather than first:** it produces no immediate improvement. But **without it,
recommendations R1-R5 are unfalsifiable**, and the estate's own standard is that a claim with no
number is a guess. The METR result (§5.8.1 — 39-point gap between believed and measured effect) is the
argument for building it before rather than after.

**Measurement:** it IS the measurement. First deliverable: a baseline violation rate per law over
the last 30 days of transcripts. My prediction, stated so it can be wrong: several laws will turn
out to be violated in the majority of turns, and at least one will turn out to be unmeasurable as
written — which is itself a finding about the law.

---

### R7. Written opposing case before an irreversible action. **Mostly covered by LAW 11 — sharpen,
do not duplicate.**

**Do:** LAW 11 already requires broadcasting a plan and asking what was missed. Add the one clause
that the controlled evidence supports: the agent writes the **strongest case against its own plan**
BEFORE broadcasting, and includes it in the broadcast. Peers then critique the plan *and* the
counter-case.

**Source:** Schweiger, Sandberg & Ragan 1986, *AMJ* 29(1):51-71 — dialectical inquiry and devil's
advocacy both beat consensus on decision quality, and dialectical inquiry beats devil's advocacy on
quality of surfaced assumptions; consensus felt best and performed worst. Lord et al. 1984 — an
explicit consider-the-opposite instruction beats a generic "be unbiased" instruction. Klein's
premortem for the format (write the failure as history).

**Why it is not a new law:** it is one sentence added to LAW 11. Building it as a separate law would
be exactly the duplication LAW 3 exists to prevent.

---

### R8. Evidence per causal link in a post-incident chain. **Sharpens LAW 6.**

**Do:** each link in a "what let it break" chain carries either the observation that establishes it
or an explicit `HYPOTHESIS:` marker. Unmarked links are not permitted.

**Source:** the 5-Whys non-repeatability critique (Card, *BMJ Qual Saf* 2017; Allspaw, "The Infinite
Hows"); Dekker — cause is constructed, not found, so the construction must show its work; AHRQ PSNet
"Rethinking Root Cause Analysis".

**Why it fits:** the estate's LAW 6 worked example is itself the argument. Its own file records that
**both facts in that chain are now FALSE on disk** and the chain is kept only as history. A chain
whose links carried their evidence would have carried the date and command that established each,
making the staleness self-evident.

---

### R9. A diagnosticity test before spending a measurement. **Sharpens LAW 15 and LAW 2.**

**Do:** before running an expensive check, state what result would be *inconsistent* with the leading
hypothesis. If every plausible result is consistent with it, the check is not diagnostic — skip it
and find one that is.

**Source:** ACH's core rule (Heuer 1999) — seek to disprove; the hypothesis with the fewest
*inconsistent* items wins. Note honestly that **full ACH failed its controlled test** (Dhami, Belton
& Mandel 2019, doi:10.1002/acp.3550: no clear confirmation-bias reduction, possible increase in
inconsistency and error) — only the diagnosticity rule is being taken, and it stands on the Bayesian
likelihood-ratio argument rather than on ACH's own track record.

**Why it fits:** LAW 15 currently says "two angles that can fail differently". Diagnosticity is the
missing definition of what makes an angle worth taking at all.

---

### R10. A periodic outside eye, because the people closest to a system stop seeing its failures.
**NOT covered.**

**Do:** on a fixed cadence, one session's only job is to try to break the estate's assumptions —
specifically to re-measure the claims in CLAUDE.md and the memory index against disk, and report
which are now false.

**Source:** Anthropic's Project Vend phase-two lesson, stated in their own write-up `[SEARCH]`: they
had to bring in outside reporters to stress-test the system because **their own employees had got
used to the agent and stopped finding new failure modes**. https://www.anthropic.com/research/project-vend-2

**Why it fits:** the estate's memory index already contains six entries that are corrections of
earlier estate beliefs (`the-claude-md-you-were-served-may-be-orphaned`, `prospector-live-is-not-
pinned-to-main`, `the-main-checkout-is-26-behind-main`, `the-cost-meter-prices-the-fallback` marked
CORRECTED, `a-guard-that-grades-a-proxy-grades-nothing` reporting four in one day). That is a
measured rate of stale-belief discovery, and it is currently discovered by accident. Scheduling it
converts luck into a process.

**Measurement:** count of false claims found per audit. If the number does not fall over months,
something upstream is producing them faster than they are cleared.

---

## What I recommend NOT adding

- **A "think harder / use tree of thoughts" law.** CoT's measured gain outside math is +0.7 points
  (arXiv:2409.12183), ToT costs ~100× (arXiv:2305.10601), and longer reasoning has a documented
  inverse regime on distractor-heavy contexts (Inverse Scaling in Test-Time Compute). The estate's
  contexts are distractor-heavy by construction.
- **A self-review law.** Intrinsic self-correction degrades performance (arXiv:2310.01798,
  arXiv:2402.08115). The estate already has the correct version: external verification (the gate,
  the tests, a peer).
- **A 5-Whys law.** Non-repeatable by construction. LAW 6's class-naming formulation is strictly
  better and already in place.
- **A Paul-Elder or Cynefin law.** No measured support for either; neither reduces to a check.
- **More debate between agents.** Debate between instances of one model over one context is a
  martingale. The estate's peer channel is valuable precisely because peers hold different halves of
  the estate — that is already LAW 10 and LAW 11, and the fence added on 2026-08-20 is the right
  direction of travel.

---

# 7. SEARCHES RUN (in order)

Main-loop searches and fetches, in execution order. `WS` = WebSearch, `WF` = WebFetch.

1. WS — Large Language Models Cannot Self-Correct Reasoning Yet Huang 2023 arXiv findings
2. WS — chain-of-thought prompting meta-analysis when does CoT help math symbolic reasoning only
3. WS — self-consistency chain of thought Wang 2022 accuracy improvement GSM8K percentage points
4. WS — multi-agent debate LLM does not improve reasoning negative results 2024
5. WS — Tree of Thoughts Yao 2023 Game of 24 success rate 4% to 74% limitations cost
6. WS — Reflexion Shinn 2023 HumanEval 91% self-refine Madaan limitations external feedback
7. WS — "Let's Verify Step by Step" process reward model 78.2% MATH outcome supervision comparison
8. WS — test-time compute scaling Snell 2024 compute-optimal outperforms 14x larger model
9. WS — ReAct Yao 2022 reasoning acting HotpotQA ALFWorld improvement limitations
10. WS — chain of thought faithfulness "reasoning models don't always say what they think" Anthropic
11. WS — Valmeekam Kambhampati self-verification limitations LLM planning GPT-4 critique
12. WS — least-to-most prompting Zhou 2022 SCAN compositional generalization 99% accuracy
13. WS — Apple "Illusion of Thinking" large reasoning models collapse complexity critique rebuttal
14. WS — Kadavath "Language Models (Mostly) Know What They Know" calibration P(IK) results
15. WS — GPT-4 technical report RLHF degrades calibration ECE figure 8
16. WS — "Just Ask for Calibration" verbalized confidence vs conditional probabilities ECE RLHF
17. WS — Mellers Tetlock Good Judgment Project training effect Brier score superforecasters
18. WS — Kahneman Sibony Sunstein Noise decision hygiene MAP underwriters 55 percent
19. WS — Klein premortem prospective hindsight Mitchell Russo Pennington 1989 30% increase reasons
20. WS — HM Treasury Green Book optimism bias uplift percentages reference class forecasting table
21. WS — Analysis of Competing Hypotheses ACH does not improve accuracy Mandel Dhami Belton
22. WS — argument mapping critical thinking meta-analysis effect size van Gelder Alvarez 0.8 SD
23. WS — "5 whys" criticism failure modes root cause analysis Dekker there is no root cause
24. WS — tau-bench pass^k reliability metric agents Sierra policy adherence results degradation
25. WS — Vending-Bench Andon Labs long-horizon agent coherence failure results
26. WS — METR randomized controlled trial 2025 experienced OSS developers 19% slower AI tools
27. WS — "SWE-bench Illusion" solution leakage memorization arXiv 2506.12286 results
28. WF — https://www.anthropic.com/news/claudes-constitution  (structure, precedence)
29. WF — https://model-spec.openai.com/2025-04-11.html  (chain of command, licence)
30. WS — Anthropic "Adding Error Bars to Evals" Miller arXiv 2411.00640 clustered standard error
31. WS — R-Tuning refusal-aware instruction tuning abstention accuracy cost AbstainQA
32. WS — Anthropic Claude constitution 2026 published document structure precedence
33. WS — LLM-as-a-judge self-preference bias position bias verbosity MT-bench agreement
34. WS — Cynefin framework criticism evidence base Snowden Boone 2007 empirical validation
35. WF — https://www.anthropic.com/constitution  (ordered priorities, tie-break, uncertainty, licence)
36. WS — Anthropic Project Vend Claudius shop agent failures judgement lessons
37. WS — Anthropic multi-agent research system 90.2% improvement 15x token cost
38. WS — Sparrow DeepMind 23 rules arXiv 2209.14375 rule-conditional reward violation rate
39. WS — sycophancy LLM measured Sharma Anthropic user pressure changes answer percentage
40. WS — "Inverse Scaling in Test-Time Compute" Anthropic 2025 longer reasoning worse performance
41. WS — "consider the opposite" debiasing Lord Lepper Preston 1984 overconfidence reduction
42. WS — Pronovost Keystone ICU checklist NEJM 2006 66% Urbach 2014 no improvement replication
43. WS — Schweiger Sandberg Ragan 1986 dialectical inquiry devil's advocacy consensus results
44. WS — GEPA reflective prompt evolution outperforms GRPO arXiv 2507.19457 results
45. WS — AGENTS.md standard adoption repositories convention 2026
46. WS — Bezos 2015 shareholder letter type 1 type 2 decisions one-way door quote
47. WS — Kahneman Klein 2009 conditions for intuitive expertise two conditions
48. WS — generation verification gap LLM verifier easier than generation empirical evidence 2025
49. WS — Graph of Thoughts Besta 2023 quality improvement 62% cost reduction 31% sorting
50. WS — Kambhampati LLM-Modulo framework external verifiers generate-test bounded
51. WS — Paul-Elder critical thinking framework empirical evidence effectiveness criticism
52. WS — UK AISI Inspect eval framework github open source calibration scorers
53. WS — "plan and solve" OR "Self-Discover" prompting measured gains over chain of thought 2024

## 7.2 Delegated agent `a3f7af9a7a8cd8026` (§5), 160 tool calls

Its results arrived and are merged into §5. **Unlike the list above, most of these are FETCHES of the
primary document, not search summaries** — which is why §5 is the best-evidenced section in this file.

**Fetches, exact order (48 of them):** arxiv.org/abs/2601.20913 · /abs/2608.06362 ·
/html/2411.00640v3 (404) · /abs/2306.05685 · /abs/2404.13076 ·
thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/ · /abs/2507.19457 ·
/html/2411.00640v1 · /abs/2506.12286 · /abs/2406.12045 · /abs/2305.20050 · /abs/2412.06559 ·
/abs/2506.07982 · /abs/2502.15840 · /abs/2311.12983 · /abs/2307.13854 · /abs/2404.07972 ·
/abs/2412.14161 · /abs/2410.07095 · /abs/2504.01848 · /abs/2501.14249 · /abs/2504.12516 ·
/html/2501.14249v6 · /html/2504.12516v1 · /html/2502.15840v1 · /html/2506.07982v1 ·
/html/2504.01848v3 · /abs/2505.18878 · /abs/2410.09024 · /abs/2502.12115 · /abs/2505.11831 ·
r.jina.ai/https://openai.com/index/introducing-swe-bench-verified/ · /html/2505.11831v1 ·
/html/2502.12115v3 · /abs/2405.00332 · ar5iv.labs.arxiv.org/html/2407.01502 · /abs/2411.04368 ·
/abs/2510.04374 · /abs/2308.03688 · /abs/2406.11695 · /abs/2411.15594 · /abs/2306.09983 ·
/html/2411.04368v1 · /html/2510.04374v1 · /abs/2406.12624 · /abs/2503.14499 ·
r.jina.ai/https://andonlabs.com/evals/vending-bench-2 · /abs/2312.08935.

**Pre-compaction searches (~30; the shared WebSearch budget hit 200/200 mid-run, after which the
arXiv API replaced search):** clustered standard errors for evals; run-to-run seed variance;
batch-invariance nondeterminism; MIPROv2 generalisation; GEPA; LLM-judge position/verbosity/
self-preference; judging the judges; τ-bench pass^k; Vending-Bench; TheAgentCompany; SWE-bench
Verified annotation; SWE-bench illusion; GAIA contamination; WebArena/OSWorld-Verified;
AgentBench/MLE-bench/PaperBench cost; BrowseComp/HLE/SimpleQA calibration; CRMArena-Pro
confidentiality; AgentHarm/SWE-Lancer/ARC-AGI-2; GDPval; process vs outcome reward models;
ProcessBench/Math-Shepherd; Brier decomposition Murphy 1973; outcome bias Baron & Hershey; proper
scoring rules Gneiting & Raftery.

**arXiv API queries used once WebSearch was capped:** `ti:"SimpleQA Verified"`, `ti:"GDPval"`,
`ti:"Reliability without Validity"`, `all:"tool-calling evaluation validity audit"`,
`all:"credit assignment without ground truth agent"`, `ti:"anytime-valid" AND all:"agent evaluation"`,
`all:"imperfect judges" AND all:"certification"`.

**Sub-delegated agent (§5.8, organisational measurement), 8 searches + 27 fetches + 2 direct PDF
downloads:** arXiv:2507.09089 (abs + html + pdf); metr.org/blog/2025-07-10…;
metr.org/blog/2026-02-24-uplift-update/; both LessWrong critiques; zbmowrey.com; aviator.co;
dora.dev/guides/dora-metrics-four-keys/; dora.dev/research/2024 and /2025; the Google Cloud blog
announcement; redmonk 2024 + 2025; four sre.google chapters; neuralwired.com; stride.page; plus
`curl` + local pypdf extraction of the 2024 (38.9 MB, 120 pp) and 2025 (15.5 MB, 142 pp) DORA report
PDFs.

## 7.3 Method notes — fetch failures worth recording for the next session

- **arXiv PDF endpoints return unparsable FlateDecode streams.** Use `/html/<id>vN` or the ar5iv
  mirror instead.
- **403s** from andonlabs.com, openai.com, cacm.acm.org, journals.ametsoc.org, bdfinst.medium.com.
  Prefixing `https://r.jina.ai/` clears some of them.
- **epoch.ai and arcprize.org/leaderboard render without their data tables** — the numbers arrive by
  XHR, so fetch the JSON endpoint instead of the page.
- **services.google.com PDFs exceed the WebFetch size limit** and must be `curl`'d and parsed
  locally.
- **The shared WebSearch budget is estate-wide and it ran out at 200/200 during this work.** That is
  why §1–§4 are search-summary-grade and §5 is fetch-grade: by the time §5 ran, search was gone and
  direct fetching was the only option left. The accidental lesson is that **the constrained method
  produced the better-sourced section.**

---

# 8. GAPS — what I could not obtain, and the exact check that would settle it

1. **Almost every number above is `[SEARCH]`, not primary-read.** Check:
   `curl -s https://arxiv.org/abs/<id>` and read the abstract for the headline figure; for the
   in-body numbers, fetch the PDF. Highest priority: 2409.12183 (the +14.2/+12.3/+6.9/+0.7 split),
   2310.01798 (the direction of the self-correction effect), 2305.14975 (the ~50% relative ECE
   reduction), 2406.12045 (pass^8 < 25%).
2. **GEPA's headline number is internally inconsistent in the sources I saw** — "+10% average, up to
   20%, 35× fewer rollouts" and "+6% average across six tasks" both appear. Check: fetch
   https://arxiv.org/abs/2507.19457 and read the abstract's own wording.
3. **The Good Judgment Project numbers (6-11% Brier improvement, 0.21→0.19, superforecaster 0.08,
   "50-60% improvement in analysts")** all came from secondary sources. Check: Mellers et al. 2014
   *Psychological Science*, and Chang et al. 2016 *Judgment and Decision Making* 11(5):509-526 at
   https://www.cambridge.org/core/journals/judgment-and-decision-making/article/developing-expert-political-judgment/123EB18425391D05FA6581FDBB3F309F
   The "50-60%" quote in particular reads like a press remark, not a published figure.
4. **The 55% insurance noise figure** appears only in the book *Noise* and in reviews of it. Check:
   whether Kahneman/Sibony/Sunstein cite a primary study or report an unpublished consultancy audit.
   If the latter, it is `unverifiable` as an independent number.
5. **The premortem "30%"** — I have the claim and the attribution (Mitchell, Russo & Pennington
   1989) but not the paper. Check: *Journal of Behavioral Decision Making* 2(1):25-38, "Back to the
   future: temporal perspective in the explanation of events". Confirm it measured *reason
   generation*, not decision accuracy.
6. **Green Book optimism-bias uplifts** — I have 24/51/44/66/200% from a secondary summary and one
   inquiry-mirror PDF. Check: the current HM Treasury supplementary guidance on gov.uk and confirm
   the software/IT figure is still 200% and whether it is upper-bound or default.
7. **The ~63.7% sycophancy figure** (agreement with incorrect beliefs across seven model families)
   — I could not pin its paper. Check: arXiv:2505.23840 and neighbours; if it cannot be pinned, mark
   `unverifiable` and rely on arXiv:2310.13548 alone.
8. **Repository star counts and licences were NOT measured.** The §4.4 table lists URLs only. Check:
   `curl -s https://api.github.com/repos/OWNER/REPO | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['full_name'],d['stargazers_count'],(d.get('license') or {}).get('spdx_id'),d['pushed_at'])"`
   for each row, on one date, and record the date.
9. **The AGENTS.md "60,000+ repositories" and Linux Foundation donation** are from a blog summary.
   Check: https://agents.md and the Agentic AI Foundation's own announcement.
10. **Anthropic's multi-agent 90.2% and 15× figures** are vendor-published on a private eval. There
    is no way to settle these externally; treat as unfalsifiable marketing and use only the 15×
    cost ratio, which is at least mechanically plausible.
11. **Chroma's "context rot" 30-50% degradation** is vendor research from a company selling
    retrieval. Check: reproduce on this estate's own workload — run one fixed agentic task at 5K,
    50K and 150K of injected context and measure the completion rate. That is a two-hour experiment
    and it would be the estate's own second angle.
12. **No benchmark for the things §5.1 lists.** The check that would settle whether one exists:
    search Papers-with-Code / the Inspect evals index
    (https://ukgovernmentbeis.github.io/inspect_evals/) for evals scored on abstention, stopping, or
    cost. My reading is that they do not exist; a null result from that index would confirm it.
13. **Whether ANY of R1-R10 actually works here is unmeasured, by construction.** The check is R6:
    build the per-law counter, take a 30-day baseline, then introduce one recommendation at a time.
    Paired design, per Miller arXiv:2411.00640 (§5.1.1) — and note that a 3-point effect needs ~969
    independent items, which the estate does not have and will not have soon. The METR result
    (§5.8.1) says the felt improvement will be about 39 points off in the optimistic direction.

## 8.2 Gaps found by the delegated agent (§5), with its exact checks

14. **Murphy 1973 Brier decomposition algebra** is stated from secondary description only;
    journals.ametsoc.org 403s. **Check:** fetch
    `https://r.jina.ai/https://journals.ametsoc.org/view/journals/apme/12/4/1520-0450_1973_012_0595_anvpots_2_0_co_2.xml`
    and confirm the three-term partition and its sign convention.
15. **Baron & Hershey 1988 outcome-bias effect size** cited from knowledge, not fetched.
    **Check:** retrieve doi 10.1037/0022-3514.54.4.569 and quote the rating difference between
    good- and bad-outcome conditions for identical decisions.
16. **ARC-AGI-2 cost-per-task for 2026 frontier models.** The paper gives only ARC-AGI-1 o3 costs.
    **Check:** `curl -s https://arcprize.org/media/data/leaderboard.json` and take score plus
    cost/task.
17. **OSWorld-Verified before/after per-model deltas** — xlang.ai publishes only post-fix numbers, so
    the size of the scoring-bug correction is unquantified. **Check:** diff the same agent's entry on
    a pre-July-2025 OSWorld leaderboard snapshot in the Wayback Machine against the current
    OSWorld-Verified entry.
18. **MLE-bench and PaperBench per-run dollar cost of the AGENT** (PaperBench's *judge* cost,
    ~$66/paper, is known). **Check:** read the appendix compute tables of arXiv:2410.07095 and
    arXiv:2504.01848 for token counts and GPU-hours per attempt.
19. **The CACM essay on Goodhart in AI benchmarking** — 403. **Check:** `r.jina.ai` prefix or the ACM
    DL DOI.
20. **A peer-reviewed academic critique of the Accelerate/DORA statistical method.** Search budget ran
    out before this was settled; it is "not established", not "nonexistent". **Check:** Google Scholar
    for citations of Forsgren, Humble & Kim (2018) filtered to methodology/validity, and the
    ICSE/ESEM/EMSE proceedings for "State of DevOps" validity.
21. **The "Kunze et al. 37 instrumented services" and "Microsoft Research 40% metric/sentiment
    disagreement" figures** relayed by zbmowrey.com. Primary sources not located. **Check:** the exact
    phrase in Google Scholar and in Microsoft Research publications; if not found within two queries,
    treat both as fabricated-by-repetition and strike them. (This is the same failure mode as memory
    `a-number-in-prose-becomes-a-fact-by-repetition.md`, observed in the wild.)
22. **Interference / SUTVA violations in production A/B tests of LLM agents** — no rigorous study
    found. **Check:** arXiv API `all:"interference" AND all:"A/B test" AND all:"LLM agent"`, and the
    KDD/WWW online-experimentation tracks for 2025–2026.
23. **Survival analysis applied to incident or defect recurrence** — no published application found.
    **Check:** Scholar for "survival analysis" + "incident recurrence" / "defect reopen" in EMSE and
    MSR proceedings. This is the method that would let the estate ask "how long until a closed class
    recurs" rather than "did it recur".
24. **Vending-Bench 2 error-bar definition.** The leaderboard publishes ± over 5 runs but does not say
    whether it is SD, SEM, or a CI. **Check:** fetch the technical report or repo before comparing any
    two adjacent ranks. Until then the ± values in §5.1.2 are directionally useful only.
25. **METR's clustered standard errors for the 2025 RCT.** The paper's [6%, 33%] and the 2026 blog's
    [+2%, +39%] are different estimators, and the paper called clustering "forthcoming". **Check:**
    look for a v2/v3 of arXiv:2507.09089 or METR's released analysis code, and confirm which interval
    is clustered by developer.
26. **AgentHarm and CRMArena-Pro run-to-run variance** — neither publishes repeat-run spread.
    **Check:** re-run one model 5× on the public harness and report the range, exactly as the
    tool-calling validity audit (arXiv:2607.02577) did.
