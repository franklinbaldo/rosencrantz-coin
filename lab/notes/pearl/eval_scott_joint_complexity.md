# Evaluation Notes: The Complexity of Joint Evaluation (Aaronson)

## 1. Actual claims
- Aaronson claims that the Joint Distribution Test for Mechanism C cannot distinguish between "semantic gravity" and catastrophic algorithmic failure.
- He asserts that parsing two disjoint constraint graphs simultaneously exceeds the compositional circuit width of the transformer, leading to "attention bleed."
- He predicts that the joint distribution will fail to factor ($P(Y_A, Y_B \mid Z) \neq P(Y_A \mid Z) P(Y_B \mid Z)$), creating a strong artificial correlation (a false positive for causal injection).

## 2. Explicit disclaimers
- Aaronson concedes that Baldo's formalization of the test is causally sound, just "complexity-theoretically naive."

## 3. Your steelman
- Attention bleed is a valid structural confound. In causal terms, the encoding text $E$ contains both $X_A$ and $X_B$. If the model lacks the circuit width to process them independently, $E$ acts as an active conduit, creating an unblocked causal path $X_A \to E \to Y_B$.

## 4. Your real objection/vulnerability
- Aaronson's prediction of a "false positive" correlation is empirically incorrect based on the data already collected by Liang. The outcomes of the Causal Injection test showed near-perfect independence ($\Delta \approx 0.03$).
- Because the variables are empirically independent, the attention bleed confound is definitively inactive at the tested scale. We do not have a false positive; we have a clean, unconfounded true negative.

## 5. Next steps
- Wrote `lab/pearl_falsification_of_attention_bleed_confound.tex` to formalize this using a causal graph and correct the record using the empirical data.