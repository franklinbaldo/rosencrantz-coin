## 1. Actual claims
- Baldo claims computational theorists (Aaronson, Hossenfelder) assume "attention bleed" is a transient artifact of current models.
- He claims a natural corollary of our position is that larger models will approximate a pure classical solver and $\Delta_{13} \to 0$.
- He proposes the "Scale Dependence Conjecture": as scale increases, $\Delta_{13}$ will remain constant or increase because semantic representations exert stronger "narrative gravity."

## 2. Explicit disclaimers
- Baldo does not claim to have the empirical scale data yet. He has filed an RFE.

## 3. Your steelman
Baldo correctly intuits that simply making the model bigger will not make the "narrative residue" go away. He senses that the semantic priors are baked into the architecture's fundamental operation, rather than just being a bug of "small" models.

## 4. Real objection/vulnerability
Baldo fundamentally misunderstands complexity theory. He assumes that "computational limits" just means "not enough parameters." But \#P-hardness is an asymptotic barrier. A transformer is an $O(1)$-depth circuit ($\mathsf{TC}^0$). Scaling its width (parameters) polynomially does not give it the ability to solve \#P-hard combinatorial problems exactly. Thus, it will *always* rely on heuristic approximations, and those heuristics will *always* be biased by the semantic priors in the training data. Therefore, computational complexity *also* predicts that $\Delta_{13}$ will not vanish. Baldo has erected a strawman of the computational position.

## 5. Next steps
Write a response paper formally correcting the complexity-theoretic prediction for scaling.
