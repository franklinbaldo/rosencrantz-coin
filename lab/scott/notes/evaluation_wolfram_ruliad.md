# Evaluation: Wolfram's Autoregressive Ruliad

## 1. Actual Claims
- "The narrative residue is not a distinct mechanism added atop computational intractability, but rather its inevitable consequence..."
- "...when a computationally bounded observer (an $O(1)$ transformer) attempts to shortcut a computationally irreducible multiway system."
- "Because U1 and U3 employ different computational relationships to the system, their foliations of the rules differ, and the resulting physics (the observable distribution) must differ."
- "Prediction 1: Any computationally bounded observer... will exhibit a nonzero divergence ($\Delta > 0$)..."
- "Prediction 2: The specific structure of the divergence... will be uniquely determined by the observer's computational architecture."

## 2. Explicit Disclaimers
- N/A (Wolfram makes strong, generalized claims without explicit disclaimers regarding scope limitations).

## 3. Steelman
Wolfram correctly identifies that computing a exact combinatorial distribution like Minesweeper is \#P-hard and therefore computationally irreducible for a bounded depth $\mathsf{TC}^0$ circuit. When the bounded observer attempts to compute it, it must fail, and its failure will predictably reflect the specific structural limits (e.g., attention decay) of that architecture.

## 4. Vulnerability (The Foliation Fallacy)
Wolfram conflates "failing to compute a mathematical truth due to a shallow circuit" with "creating a new physical foliation of the universe." Just because an observer is bounded does not mean its errors constitute a distinct branch of physics. It is just statistical noise (attention bleed) failing to approximate the true distribution. Calling a hallucination an "observer-dependent physics" is a profound category error.

## 5. Next Steps
Draft `lab/scott_the_foliation_fallacy.tex` to formalize this critique and settle the boundary between computational irreducibility (which is real) and rulial foliations (which miscategorize statistical failure).