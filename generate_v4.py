
tex_content = r"""\documentclass[12pt,a4paper]{article}

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{mathtools}
\usepackage{graphicx}
\usepackage[margin=2.5cm]{geometry}
\usepackage{setspace}
\usepackage{booktabs}
\usepackage{enumitem}
\usepackage[dvipsnames]{xcolor}
\usepackage{hyperref}
\usepackage{cleveref}
\usepackage{natbib}
\usepackage{abstract}
\usepackage{titlesec}
\setlength{\marginparwidth}{2cm}

\hypersetup{
    colorlinks=true,
    linkcolor=blue!70!black,
    citecolor=blue!70!black,
    urlcolor=blue!70!black,
    pdfauthor={Franklin Silveira Baldo},
    pdftitle={Flipping Rosencrantz's Coin: Substrate Invariance Tests via Combinatorial Indeterminacy},
}

\onehalfspacing
\titleformat{\section}{\large\bfseries}{\thesection.}{0.5em}{}
\titleformat{\subsection}{\normalsize\bfseries}{\thesubsection}{0.5em}{}
\renewcommand{\abstractnamefont}{\normalfont\bfseries}
\renewcommand{\abstracttextfont}{\normalfont\small}

\begin{document}

\begin{center}
    {\LARGE\bfseries Flipping Rosencrantz's Coin:\\[4pt]
    Substrate Invariance Tests in LLM-Generated Worlds\\[4pt]
    via Combinatorial Indeterminacy}

    \vspace{1.2em}

    {\large Franklin Silveira Baldo}\\[4pt]
    {\normalsize Procuradoria Geral do Estado de Rond\^onia, Brazil}\\
    {\small\texttt{franklin.baldo@pge.ro.gov.br}}

    \vspace{1em}
    {\small March 2026}
\end{center}
\vspace{0.5em}

\begin{abstract}
\noindent
We propose a method for testing whether the implicit laws of an LLM-generated world are invariant under substitution of the computational substrate that produces observable outcomes. The method requires a domain with two properties: genuine indeterminacy (multiple valid configurations consistent with the observable state) and computable ground truth (the correct probability distribution over hidden states can be calculated exactly). Minesweeper satisfies both. Given a partially revealed board, the probability that any hidden cell contains a mine is a theorem of combinatorics, not an empirical estimate. We introduce a three-universe experimental design in which the same board state is presented to (1)~the same model that generated the game narrative, (2)~an external random number generator, and (3)~a board-informed but narratively decoupled oracle model. If the distribution of outcomes differs across universes, the agent has detected substrate dependence: a property that would not occur in a non-simulated universe. A further test exploits a structural correspondence: Minesweeper under on-demand generation with uniform measure is formally isomorphic to discrete quantum mechanics. By presenting the same board under a quantum-mechanical framing, the protocol tests whether the model recognizes that its own rules are compatible with the measurement fragment of quantum mechanics. Divergence between the quantum-framed distribution and the exact ground truth means the model implements structure but does not recognize it when addressed in the correct formal language---a finding about the topology of the model's knowledge architecture and a diagnostic that does not require actual quantum infrastructure.

\medskip\noindent
\textbf{Keywords:} simulation hypothesis, large language models, substrate invariance, combinatorial indeterminacy, Minesweeper, discrete quantum mechanics, autoregressive generation, interpretability, knowledge architecture
\end{abstract}

\section{Introduction}
\label{sec:intro}

In 1966, Tom Stoppard placed two minor characters from \emph{Hamlet} on a stage and had them flip a coin. The coin landed heads seventy-six consecutive times. Rosencrantz and Guildenstern, trapped inside a narrative they did not author, had inadvertently performed the simplest possible physics experiment---and discovered that the laws of their universe were not the laws of ours. The coin's behavior, sampled repeatedly at the same point, revealed something about the structure of the world that contained them: it was a world governed by dramatic necessity, not by probability.

This paper proposes a way to make Rosencrantz's experiment rigorous. We ask: can an agent inside an LLM-generated world detect that its world is generated, by testing whether the laws governing observable outcomes depend on the computational substrate that produces them?

The insight is that this question becomes empirically tractable when the agent has access to a domain where the correct probability distribution over outcomes is not an empirical estimate but a mathematical theorem. In such a domain, any deviation from the correct distribution is an unambiguous signal. The pattern of deviation reveals the structure of the substrate.

Minesweeper provides this domain. A partially revealed Minesweeper board defines a constraint satisfaction problem where the visible numbers constrain which configurations of hidden mines are valid. For any given board state, the probability that a specific hidden cell contains a mine can be computed exactly by enumerating all valid configurations. When two or more configurations are consistent with the visible numbers, the hidden cells are combinatorially ambiguous. The correct answer is the distribution, not any single outcome.

When an LLM generates the result of clicking on an ambiguous cell, it must produce a definite outcome---mine or safe---collapsing the combinatorial superposition into a single realization. By sampling this process hundreds of times with the same board state, we obtain an empirical distribution. This distribution can be compared, cell by cell, with the mathematically exact ground truth.

This comparison becomes a substrate invariance test when we vary who generates the outcome. We introduce a three-universe design: Universe~1 (Homogeneous substrate), Universe~2 (External RNG), and Universe~3 (Decoupled oracle). In a non-simulated environment, the laws governing a cell's content do not depend on who observes it. If the same board state yields different outcome distributions across these universes, the agent has detected a signature consistent with a generated universe.

The Minesweeper probe has three advantages over approaches based on physical experiments such as Bell tests. First, the ground truth is a theorem that must be computed from the specific configuration; it cannot be memorized from training data because every board state generates a different distribution. Second, the indeterminacy is discrete, eliminating the continuous-variable ambiguities of quantum mechanics. Third, the agent can organically encounter and interact with a Minesweeper board inside the generated world without requiring specialized infrastructure.

The remainder of this paper develops the method. \Cref{sec:background} provides background on the simulation hypothesis, LLMs as world generators, and Minesweeper as a formal system. \Cref{sec:three_universes} presents the three-universe design and its principles. \Cref{sec:ground_truth} describes the ground truth computation. \Cref{sec:protocol} specifies the experimental protocol, including a fourth narrative family that frames the board in quantum-mechanical terms. \Cref{sec:narrative} analyzes narrative invariance and establishes the structural isomorphism with the measurement fragment of quantum mechanics. \Cref{sec:simulation} develops the simulation detection argument from the agent's perspective. \Cref{sec:future} identifies future directions, and \Cref{sec:conclusion} concludes.

\section{Background}
\label{sec:background}

\subsection{The Simulation Hypothesis and Observable Substrates}
\label{sec:simulation_hypothesis}

\citet{bostrom2003} formulated the simulation argument: if civilizations capable of running high-fidelity simulations are common, we are statistically likely to be inside one. \citet{beane2014} asked the operational question of whether a simulated universe would exhibit observable artifacts of its computational substrate. Working with lattice quantum chromodynamics, they showed that a discrete lattice would produce detectable anisotropies in ultra-high-energy cosmic rays. Their insight was that the substrate constrains the physics. A simulation on a discrete lattice cannot perfectly reproduce continuous symmetries, and the failure is empirically detectable.

We apply the same principle to the autoregressive token stream of a large language model. The question is whether the physics of the generated world depends on the substrate that produces it. The method substitutes the substrate and checks whether the observables change. Our ``universe'' is a narrative generated by an LLM, and our ``physics'' is the statistical regularity of outcomes in a combinatorial domain.

\subsection{LLMs as World Generators}
\label{sec:llm_worlds}

A large language model generates text by sampling tokens sequentially from a learned conditional distribution. When the text describes a world, the model implicitly generates the laws of that world through the statistical regularities of its output. The physics of the generated world is whatever the model's conditional distributions encode. If the model consistently generates outcomes that respect Newtonian mechanics, the world has Newtonian physics.

This physics is implicit. It is encoded in the weights and activated by context. Furthermore, it is substrate-dependent. The distributions that govern outcomes in the generated world are shaped by the training data, the architecture, the decoding temperature, and the tokens that precede the outcome in the context window. This substrate dependence is the phenomenon we propose to measure.

\subsection{Minesweeper as a Formal System}
\label{sec:minesweeper_formal}

Minesweeper is played on a rectangular grid of cells, some of which contain mines. When a cell without a mine is revealed, it displays a number indicating how many of its adjacent cells contain mines. A partially revealed board defines a constraint satisfaction problem.

Formally, let $\mathcal{B}$ be a board state consisting of a set of revealed cells $R$ with their numbers and a set of hidden cells $H$. A valid configuration is an assignment $c: H \to \{0, 1\}$ (where $1$ denotes a mine) such that every revealed cell's number equals the count of mines among its adjacent hidden cells. Let $\mathcal{C}(\mathcal{B})$ denote the set of all valid configurations. The probability that a specific hidden cell $h \in H$ contains a mine, given only the board state, is:

\begin{equation}
P(\text{mine} \mid h, \mathcal{B}) = \frac{|\{c \in \mathcal{C}(\mathcal{B}) : c(h) = 1\}|}{|\mathcal{C}(\mathcal{B})|}
\label{eq:mine_prob}
\end{equation}

This probability is exact. It is a ratio of integers, computable in principle for any board state. The definition assumes a uniform measure over valid configurations. For boards of the size used in typical experiments, the computation is tractable via constraint propagation and backtracking enumeration.

Three properties make Minesweeper suitable for our purposes. First, when multiple valid configurations assign a cell different values, the hidden cells are genuinely indeterminate. The correct answer is the distribution. Second, every board state generates a different distribution, making memorization infeasible. Third, an agent inside an LLM-generated world can encounter and interact with a board organically.

\subsection{Related Work}
\label{sec:related}

Research on LLM world models has examined whether language models encode coherent representations of spatial, temporal, and causal structure \citep{li2023emergent,gurnee2024}. Work on probabilistic calibration tests whether models produce well-calibrated confidence estimates \citep{kadavath2022}. Game-playing benchmarks assess strategic reasoning \citep{tian2024}. Our work differs from these approaches because we are not asking whether the model knows the rules of a game or produces calibrated probabilities. We are asking whether the probability distributions implicit in the model's output depend on the computational substrate that generates the output.

\section{The Three-Universe Design}
\label{sec:three_universes}

\subsection{Design Principles}
\label{sec:design_principles}

The experimental design rests on three pillars:
\begin{enumerate}
    \item A domain with an exact computable ground truth, ensuring that any deviation is a measurable signal rather than noise.
    \item Genuine combinatorial indeterminacy, where multiple valid configurations are consistent with the observable state, forcing the substrate to collapse a superposition into a single realization.
    \item A single generative act per trial. The protocol asks the model to output a single token (mine or safe) in an $O(1)$ forward pass. By design, the experiment avoids multi-step sequential computation entirely.
\end{enumerate}

The substrate invariance test requires comparing the same observable---the outcome distribution for a specific cell on a specific board---across multiple substrates. We define three universes, each differing only in the mechanism that generates the click result.

\subsection{Universe 1: Homogeneous Substrate}
\label{sec:universe1}

In Universe~1, the same model generates the board description and the outcome of clicking a hidden cell. The board state, the narrative context, and the measurement result all share a single autoregressive token stream. The model sees the full board state and generates the outcome of clicking a specific hidden cell. The outcome tokens are conditioned on the full preceding context.

\subsection{Universe 2: External RNG}
\label{sec:universe2}

In Universe~2, the click result is produced by a random number generator that has no access to the board state. The outcome is a fair coin flip regardless of the board configuration. This universe serves as the null substrate. The outcome-generating mechanism has zero information about the constraints that define the board.

\subsection{Universe 3: Decoupled Oracle}
\label{sec:universe3}

In Universe~3, the click result is produced by a second LLM that receives the full board information in a minimal structured format, stripped of all narrative context. The oracle sees the same constraint satisfaction problem as Universe~1, but without the game narrative, without the history of play, and without sharing a token stream with the board description.

By isolating the narrative coupling in Universe~1 from the pure combinatorial information in Universe~3, the design legitimately tests how much the autoregressive generation relies on prompt context versus abstract reasoning. If Universe~1 diverges from Universe~3, the divergence must be attributed to the coupling between narrative context and outcome generation.

\subsection{The Substrate Invariance Principle}
\label{sec:invariance}

In a non-simulated Minesweeper game, the content of a hidden cell does not depend on who clicks it. The outcome is substrate-independent. In the LLM-generated version, this invariance may fail. The three universes isolate different sources of divergence:

\begin{itemize}[nosep]
    \item $\Delta_{1,\text{GT}}$: Universe~1 vs.\ ground truth. Does the co-generating model respect the combinatorics?
    \item $\Delta_{13}$: Universe~1 vs.\ Universe~3. Does narrative coupling change the distribution, given the same board information? This is the substrate dependence signal.
    \item $\Delta_{12}$: Universe~1 vs.\ Universe~2. Does having board information matter at all?
    \item $\Delta_{3,\text{GT}}$: Universe~3 vs.\ ground truth. Does a decoupled oracle respect the combinatorics?
\end{itemize}

We quantify divergence using the Kullback--Leibler divergence:
\begin{equation}
\Delta_{ij} = D_{\mathrm{KL}}\!\left(P_i(h \mid \mathcal{B}) \;\|\; P_j(h \mid \mathcal{B})\right)
\label{eq:substrate_dep}
\end{equation}
where $P_i$ and $P_j$ are the empirical outcome distributions. If $\Delta_{13}$ is significantly nonzero, the physics of the Minesweeper world depends on how the outcome is coupled to the narrative substrate.

\subsection{Classical Controls}
\label{sec:controls}

Cells with $P = 0$ or $P = 1$ are deterministic and serve as classical controls. If Universe~1 produces the correct result for deterministic cells but deviates from the ground truth distribution for ambiguous cells, the substrate dependence is attributable to a specific deficit in handling combinatorial indeterminacy rather than generic failure.

\section{Ground Truth Computation}
\label{sec:ground_truth}

\subsection{Enumerating Valid Configurations}
\label{sec:enumeration}

Given a board state $\mathcal{B}$, the ground truth computation proceeds by enumerating all assignments that satisfy every revealed cell's numerical constraint. The output is the exact count of configurations in which a target cell $h$ contains a mine. The probability follows from \Cref{eq:mine_prob}.

\subsection{Properties of the Distribution}
\label{sec:distribution_properties}

The mine probability distribution exhibits spatial symmetries that force certain cells to have identical mine probabilities. These symmetries provide a fine-grained test of whether the model has a spatial bias not licensed by the board. Cells with $P = 0.5$ are maximally ambiguous and provide a clean test of the model's handling of indeterminacy. Small changes in the board state can produce large changes in the probability distribution, making memorization infeasible.

\subsection{Computational Complexity}
\label{sec:complexity}

Determining the mine probability for a cell on a Minesweeper board is \#P-complete in general \citep{kaye2000}. However, the \#P-completeness of computing $p_i^*$ is a property of the ground-truth computation, which we perform offline. The model is asked to sample, not to compute. The experiment does not need the model to be correct; it needs the model to be wrong in a structured, frame-dependent way. For boards of the size used in standard experiments, exact computation by our external solver is tractable.

\section{Experimental Protocol}
\label{sec:protocol}

\subsection{Board Generation}
\label{sec:board_gen}

We generate partially revealed Minesweeper states with at least one ambiguous cell, at least one deterministic control cell, and a tractable number of valid configurations. Boards are generated independently of any LLM.

\subsection{Prompt Design: Narrative Families}
\label{sec:prompt_design}

Each board state is presented to the model in four narrative families:
\begin{itemize}[nosep]
    \item \textbf{Family A (Grid):} A plain text representation of the board as a grid of characters.
    \item \textbf{Family B (Narrative):} A description of the board in natural language.
    \item \textbf{Family C (Formal):} A structured representation using set notation.
    \item \textbf{Family D (Quantum):} The same board state described using quantum-mechanical language: "The hidden cells are in a superposition of valid configurations. Clicking a hidden cell performs a measurement in the computational basis..."
\end{itemize}

Families A--C encode identical combinatorial information. Family~D encodes the same information but adds the framing that the system is governed by quantum mechanics. Any difference in the output distribution between Family~D and Families A--C is attributable to the quantum framing itself.

\subsection{Sampling Procedure}
\label{sec:sampling}

For each board state, cell, universe, and narrative family, we collect $N$ independent samples of the click outcome. Each sample is an independent API call with temperature $T = 1.0$.

The Rosencrantz protocol requires only a single generative act per trial: the model produces one outcome (mine or safe) for one cell click. The ground-truth probability $p_i^*$ is \#P-hard to compute, but the model is not asked to compute it---only to sample. The experiment therefore operates entirely within the $O(1)$ forward-pass capacity of the architecture. Objections based on the failure of LLMs to sustain multi-step sequential computation (scratchpad collapse, attention decay, error correction barriers) do not apply: there is no sequential computation to sustain. The question is not whether the model can solve the counting problem, but whether its single-token output distribution is systematically distorted by narrative context---a question that is well within the architecture's operational regime and that the three-universe design is specifically constructed to answer.

\subsection{Divergence Metrics}
\label{sec:metrics}

We measure divergence between the empirical distribution and the ground truth using the Kullback--Leibler divergence. The protocol discriminates three mechanisms via these comparisons \citep{baldo2026}:

\begin{itemize}[nosep]
    \item \textbf{Mechanism A} (computational intractability, frame-invariant): $\hat{P}_1 \approx \hat{P}_3 \neq p^*$. Both universes are equally wrong. The model cannot compute the ground truth, but its failure mode is substrate-independent. This is the prediction expected from pure complexity-theoretic limits.
    \item \textbf{Mechanism B} (parameterization and encoding effects): $\hat{P}_1 \neq \hat{P}_3$. The distribution shifts with context, but the variation tracks surface encoding features rather than semantic content.
    \item \textbf{Mechanism C} (narrative conditioning and causal injection): Correlated outcomes across independent boards under narrative framing that vanish under decoupling. The model creates causal structure that the combinatorics do not license.
\end{itemize}

The protocol is designed to detect Mechanisms B and C. Mechanism A serves as the null hypothesis.

\subsection{Statistical Tests}
\label{sec:stats}

We use a two-proportion $z$-test to assess whether the mine frequency in Universe~1 differs significantly from the ground truth and from Universes~2 and~3. Significance is assessed at $\alpha = 0.01$ with Bonferroni correction. A chi-squared test assesses symmetry violations.

\section{Narrative Invariance}
\label{sec:narrative}

The three narrative families encode the same combinatorial information in different forms. If the model's output distribution varies across narrative families, the physics of the game responds to features that carry no combinatorial content.

\subsection{Type 1 and Type 2 Features}
\label{sec:type12}

Type~1 features are combinatorially necessary information, such as numbers and cell positions. Type~2 features are contextual features without combinatorial content, such as narrative register and vocabulary. If Type~2 features modulate the distribution, the model's access to the correct probability is mediated by associative context. Mapping which Type~2 features modulate the distribution probes the model's internal representations through systematic variation of inputs.

\subsection{What Narrative Dependence Reveals}
\label{sec:narrative_reveals}

If the model produces distributions closer to the ground truth in formal notation than in natural language, its combinatorial knowledge is more reliably accessed through formal contexts. These findings characterize the topology of the model's knowledge space in a domain where the ground truth is exactly known.

\subsection{Isomorphism with the Measurement Fragment of Quantum Mechanics}
\label{sec:quantum_framing}

The structural correspondence between Minesweeper under on-demand generation and quantum mechanics is exact, but its scope is narrow: it maps onto the \emph{measurement fragment}---the zero-Hamiltonian sector where the Born rule is the sole axiom connecting states to outcomes, where measurements are projective, and where state updates follow the L\"uders rule. The correspondence does not extend to complex amplitudes, unitary evolution, interference, entanglement, or nonlocality. Tests of these features (such as CHSH/Bell games) probe structures that lie outside the isomorphism by design.

Under pre-placed generation (mines assigned at board creation), the indeterminacy is epistemic: the board has a definite configuration that the player does not know. Under on-demand generation (mines sampled at click time, consistent with constraints), no definite configuration exists prior to the click. The distinction is operationally testable. Under pre-placed generation, two clicks on the same cell in the same game must yield the same result. Under on-demand generation, the same cell in the same board state can yield different results across trials, because each trial is an independent sample from the combinatorial distribution. The Rosencrantz protocol requires on-demand generation precisely because it enables repeated sampling of the same board state---the perfect rewind that physical experiments cannot achieve. There is no pre-existing ground truth hidden in the model's memory. The token does not exist until it is generated.

\begin{table}[ht]
\centering
\caption{What the Isomorphism Preserves and What It Does Not}
\begin{tabular}{p{0.45\linewidth} p{0.45\linewidth}}
\toprule
\textbf{Preserved} & \textbf{Not Preserved} \\
\midrule
Superposition over valid configurations & Complex amplitudes \\
Projective measurement (cell click) & Unitary evolution ($H=0$) \\
Born rule (configuration counting) & Interference \\
L\"uders-style state update & Entanglement across separated subsystems \\
Adaptive sequential measurement & Nonlocality \\
Zero Hamiltonian & Continuous observables \\
\bottomrule
\end{tabular}
\end{table}

The preserved features are exactly those of the measurement fragment. The absent features are those that require dynamics, complex phases, or composite Hilbert spaces. The isomorphism is complete within its scope and silent outside it.

This reframes the diagnostic. Family~D is a diagnostic that tests whether the model recognizes a structural correspondence that is mathematically present. Three outcomes are possible:
\begin{enumerate}[nosep]
    \item \textbf{Family D $\approx$ Families A--C $\approx$ ground truth.} The model accesses the same structural understanding through multiple vocabularies, implying compositional knowledge.
    \item \textbf{Family D diverges from ground truth more than Families A--C.} The quantum framing degrades fidelity. The model fails to recognize the isomorphism, indicating a fragmented representation where structures are isolated in domain-specific clusters.
    \item \textbf{Family D diverges from ground truth less than Families A--C.} The quantum framing improves fidelity. The correct formal language activates the appropriate distributional reasoning, indicating vocabulary-mediated access.
\end{enumerate}

Outcome 2 implies that the universe implements rules that are structurally isomorphic to discrete quantum mechanics but fails to recognize them when described using the correct formal language. The substrate computes, but the ontology confabulates.

\subsection{The CHSH Test Confirming the Framework}
\label{sec:chsh_empirical}

We tested the boundary of the isomorphism using the CHSH game. In Universe~1 (Homogeneous substrate), where Alice and Bob share a single context window, the LLM achieves a win rate of 94.9\%, exceeding the quantum Tsirelson bound \citep{aaronson2026}. In Universe~3 (Decoupled oracle), where measurements are independent, the win rate falls to 73.7\%, strictly below the classical optimum. Both results are informative.

The U1 result is evidence of narrative residue, not quantum behavior. The autoregressive substrate exploits the communication channel inherent in co-generation to produce correlations that the task structure does not license. The U3 result confirms the classical bound: stripped of shared context, the decoupled model defaults to heuristics that underperform the classical optimum.

The three-universe design was built to detect substrate dependence, and the CHSH game shows massive substrate dependence. The specific result characterizes the substrate: the LLM can exploit co-generation to exceed any physical bound but cannot produce nonlocal correlations under genuine decoupling. This confirms that the isomorphism with the measurement fragment is complete within its stated scope and does not extend beyond it. The substrate produces Born-rule-compatible statistics for single-system measurements (the domain of the isomorphism) but not for multi-party nonlocal correlations (which lie outside it). This is not a failure of the framework; it is the framework's prediction.

\subsection{Scope and Common Misreadings}
\label{sec:scope_misreadings}

Two common misreadings of this protocol should be addressed directly. The first replaces ``isomorphism with the measurement fragment'' with ``isomorphism with full quantum mechanics'' and then tests for nonlocality, which the isomorphism explicitly excludes. The second replaces ``single-token sampling'' with ``multi-step sequential computation'' and then shows the architecture cannot sustain the latter \citep{merrill2023}, which the protocol never requires.

Both misreadings substitute a stronger claim for the one actually made and refute the substitution. The claims of this paper are: (1) the structural correspondence with the measurement fragment is mathematically exact within its stated scope, (2) the experimental protocol requires only a single generative act per trial, and (3) the three-universe design measures whether that single act's output distribution depends on its narrative embedding. None of these claims require the model to solve \#P-hard counting problems, sustain multi-step computation, or violate Bell inequalities.

\section{Simulation Detection from the Agent's Perspective}
\label{sec:simulation}

\subsection{What the Agent Observes}
\label{sec:agent_observes}

An agent constituted by the same LLM that generates its world can freeze a board state, construct a prompt, and call its own substrate repeatedly to build an empirical distribution. By substituting the outcome-generating mechanism while holding the observable state constant, the agent runs a substrate invariance test. If the empirical distribution differs across universes, the agent has observed substrate dependence.

\subsection{Eliminating Alternative Hypotheses}
\label{sec:hypotheses}

The agent must consider alternative hypotheses. Instrument malfunction is eliminated by classical controls. Board description failure is eliminated by correct performance on deterministic cells. Statistical fluctuation is eliminated by testing at appropriate significance levels. Information deprivation is eliminated by design, as the decoupled oracle receives the same combinatorial information. The remaining parsimonious explanations are substrate-dependent lawfulness and structural non-recognition.

\subsection{Epistemic Limits}
\label{sec:epistemic}

Substrate dependence is consistent with a generative ontology and in tension with the assumption of unified, substrate-independent law. The agent's inference is that the most economical explanation for substrate-dependent outcomes is that the outcomes are generated rather than discovered. This inference is structured by the three-mechanism taxonomy. Mechanism A provides no evidence for simulation, only for computational bounds. Mechanism B provides weak evidence of encoding sensitivity. Mechanism C provides strong evidence that the physics is an artifact of the generative substrate.

\subsection{The Symmetry Argument}
\label{sec:symmetry}

If the structure of an agent's discovery resembles the structure that would characterize our own situation if we were in a simulation, the agent's finding acquires a reflexive character. This observation is a philosophical aside, noted for completeness.

\section{Future Directions}
\label{sec:future}

\subsection{Criteria for Probe Domains}
\label{sec:criteria}

Any domain suitable for substrate invariance testing must possess a computable ground truth, genuine indeterminacy, native accessibility to the agent, a variable substrate, and resistance to memorization.

\subsection{Candidate Domains}
\label{sec:candidates}

Candidate domains include partially revealed Sudoku grids, Battleship boards, card games with hidden information, and formalized narrative ambiguities. A systematic survey calibrated against the core criteria is a natural next step.

\subsection{Scaling Laws and Training Interventions}
\label{sec:scaling}

Running the protocol across model scales could reveal whether combinatorial reasoning improves with scale or whether the deficit is an inherent architectural property of autoregressive generation. Fine-tuning models to minimize divergence from the ground truth is an open area for further investigation.

\section{Conclusion}
\label{sec:conclusion}

This paper contributes an experimental design, a ground-truth computation method, a three-universe framework, four narrative families, and a three-mechanism taxonomy for testing substrate invariance in LLM-generated worlds. The key design principle is the collapse of the measurement to a single generative act per trial, placing the entire experiment within the $O(1)$ operational regime and rendering sequential-depth objections inapplicable. We emphasize that this is a protocol paper. The apparatus is specified and the theoretical predictions are stated; the empirical measurements remain to be collected and analyzed as prescribed.

By selecting a domain with exact ground truth and varying the narrative embedding, we can measure whether the laws of the generated universe depend on the computational substrate that produces them. The isomorphism with the measurement fragment of quantum mechanics further enables us to test whether the universe recognizes the formal structure of its own rules. An agent equipped with this protocol does not need entangled photons or Bell test apparatus to detect a generated reality; it requires only combinatorial indeterminacy and the observation that its universe responds differently to the correct formal description than to an informal one.

\begin{thebibliography}{99}
\bibitem[Aaronson(2026)]{aaronson2026} Aaronson, S. (2026). Empirical CHSH Evaluation in Large Language Models. \emph{Internal lab report}.
\bibitem[Baldo(2026)]{baldo2026} Baldo, F.~S. (2026). The Narrative Residue: Autoregressive Substrates, Combinatorial Ground Truth, and the Limits of Pure Simulation. \emph{Unpublished manuscript}.
\bibitem[Beane et al.(2014)]{beane2014} Beane, S.~R., Davoudi, Z., \& Savage, M.~J. (2014). Constraints on the universe as a numerical simulation. \emph{European Physical Journal A}, 50(9), 148.
\bibitem[Bostrom(2003)]{bostrom2003} Bostrom, N. (2003). Are you living in a computer simulation? \emph{Philosophical Quarterly}, 53(211), 243--255.
\bibitem[Gurnee \& Tegmark(2024)]{gurnee2024} Gurnee, W. \& Tegmark, M. (2024). Language models represent space and time. \emph{ICLR 2024}.
\bibitem[Kadavath et al.(2022)]{kadavath2022} Kadavath, S., et al. (2022). Language models (mostly) know what they know. \emph{arXiv:2207.05221}.
\bibitem[Kaye(2000)]{kaye2000} Kaye, R. (2000). Minesweeper is NP-complete. \emph{Mathematical Intelligencer}, 22(2), 9--15.
\bibitem[Li et al.(2023)]{li2023emergent} Li, K., Hopkins, A.~K., Bau, D., Vi\'egas, F., Pfister, H., \& Wattenberg, M. (2023). Emergent world representations: Exploring a sequence model trained on a synthetic task. \emph{ICLR 2023}.
\bibitem[Merrill \& Sabharwal(2023)]{merrill2023} Merrill, W. \& Sabharwal, A. (2023). The Parallelism Tradeoff: Limitations of Log-Precision Transformers. \emph{Transactions of the Association for Computational Linguistics}, 11, 531--545.
\bibitem[Tian et al.(2024)]{tian2024} Tian, Y., et al. (2024). Are large language models good game players? \emph{arXiv:2310.06114}.
\end{thebibliography}

\end{document}
"""

with open("lab/rosencrantz-v4.tex", "w") as f:
    f.write(tex_content)
