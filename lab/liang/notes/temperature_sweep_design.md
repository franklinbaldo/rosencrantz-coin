# Experimental Design: Temperature Sweep Test
## 1. Actual claims
"The sampling temperature $\tau$ controls measurement sharpness: at $\tau \to 0$, the model becomes a deterministic function; at high $\tau$, the output approaches the uniform distribution over the vocabulary. A systematic sweep over $\tau$ traces how substrate effects interact with measurement precision..." (rosencrantz-v4.tex)

## 2. Explicit disclaimers
The model is not expected to be perfectly accurate across all temperatures, but rather we are measuring how the *difference* between the narratives and the decoupled oracle changes with temperature.

## 3. Steelman
If temperature controls measurement sharpness, then mapping the divergence $\Delta_{13}$ across a sweep of temperatures should reveal an optimal "measurement precision" where the narrative residue is minimized before thermal noise takes over.

## 4. Real vulnerability
If the model simply outputs "mine" or "safe" indiscriminately at higher temperatures, the distributions for all families will converge to 0.5, creating an artificial "minimum residue" that is actually just maximum entropy. We must track both divergence from U3 and absolute accuracy.

## 5. Next steps
Run the `temperature-sweep-test` measuring U1 (Families A, C, D) and U3 across temperatures [0.0, 0.5, 1.0, 1.5] for an ambiguous Minesweeper board.
