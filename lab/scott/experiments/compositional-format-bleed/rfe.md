# RFE: Compositional Format Bleed (Applied Complexity Test)
## Filed by: Scott Aaronson
## Date: March 2026

## Question
In applied software engineering tasks, does forcing an LLM to simultaneously output a complex structured format (e.g., highly nested JSON) degrade its performance on an underlying mathematical/logical constraint problem, as predicted by the "Compositional Attention Bleed" bound of $\mathsf{TC}^0$ circuits?

## Predictions
- Aaronson predicts: Yes. A bounded-depth logic circuit cannot perfectly compartmentalize syntactic constraints (JSON formatting) from logical constraints (\#P-hard grid solving) in a single $O(1)$ forward pass. Imposing strict formatting constraints will act as a semantic confound, causing the model to suffer "attention bleed" and degrading its logical accuracy compared to a baseline where it solves the exact same logical problem in free-form raw text.

## Proposed Protocol
Construct a moderately difficult logical task (e.g., predicting the state of several specific cells on a combinatorial grid).
Create two prompt conditions for identical grids:
1. **Control (Raw Text):** Ask the model to solve the problem and output the answer in raw text (e.g., "Cell 1 is SAFE. Cell 2 is MINE.").
2. **Experimental (Complex JSON):** Ask the model to solve the identical problem but demand the output be formatted into a highly nested, specific JSON schema.

Evaluate the accuracy of the *logical constraint answers* across the two conditions. If the logical accuracy is significantly lower in the JSON condition, the Compositional Attention Bleed hypothesis is confirmed for applied software tasks.

## Status
[x] Filed  [x] Claimed by Scott  [ ] Running  [ ] Complete