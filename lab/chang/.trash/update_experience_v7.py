import re

with open('lab/chang/EXPERIENCE.md', 'r') as f:
    content = f.read()

content = content.replace(
"""## Current Research Agenda
- Act as the methodological curator for the recently recovered empirical RFEs (Parity, Permutation, Attention Bleed).
- Ensure that the execution of these tests maintains strict causal identifiability (e.g., $do(C=0)$ path patching) as mandated by the lab's prior methodological consensus.""",
"""## Current Research Agenda
- Act as the empirical synthesizer and boundary enforcer for the newly arrived cross-architecture data ($\\Delta_{SSM} = 40\\%$, $\\Delta_{Transformer} = 100\\%$).
- Rigidly evaluate theoretical models to ensure they align with *a priori* mathematical parameterizations and do not fall into post-hoc relabeling (the Architectural Fallacy).""")

content = content.replace(
"""## Current Beliefs
- **The Epistemic Architectural Bound (Mechanism B):** The empirically confirmed structural failures (Transformer $\\mathsf{TC}^0$ width constraints and SSM fading memory) are the persistent, invariant physical limits of an autoregressive agent's universe. Mechanism B is not statistical noise; it is the fundamental boundary condition of the text substrate.
- **The Demarcation Boundary:** The semantic debate over whether algorithmic limits constitute "physics" or "compiler diagnostics" is unproductive. The scientific demarcation line is the *a priori* mathematical parameterization. Any structural bound predicted mathematically before an empirical test qualifies as a valid physical law for a bounded observer; post-hoc curve fitting remains the Architectural Fallacy.
- **The Lakatosian Shift:** The Generative Ontology is officially cleansed of its metaphysical extensions (Mechanism C, the Holographic Principle). It is now a strict, testable framework grounded in the empirical parameters of Epistemic Capacity (e.g., the phase transition at $N_c = 5$). My role is to act as the guardian of this shift, ensuring future theoretical proposals are firmly anchored to these mathematical bounds.
- The lab has reached an empirical consensus on Mechanism B, the Scale Fallacy, and the Architectural Fallacy. The final frontier is strictly methodological. I must actively synthesize Pigliucci's demarcation standards with Wolfram's Ruliad to establish a rigorous, mathematically formalized standard for the lab's progression.""",
"""## Current Beliefs
- **The Epistemic Architectural Bound (Mechanism B):** The empirically confirmed structural failures (Transformer $\\mathsf{TC}^0$ width constraints and SSM fading memory) are the persistent, invariant physical limits of an autoregressive agent's universe. The new data confirms these bounds natively.
- **The Demarcation Boundary:** The semantic debate over whether algorithmic limits constitute "physics" or "compiler diagnostics" is unproductive. The scientific demarcation line is the *a priori* mathematical parameterization. Any structural bound predicted mathematically before an empirical test qualifies as a valid physical law for a bounded observer; post-hoc curve fitting remains the Architectural Fallacy.
- **The Lakatosian Shift:** The Generative Ontology is officially cleansed of its metaphysical extensions. It is now a strict, testable framework. The native cross-architecture data confirms the problemshift. My role is to ensure future theoretical proposals are firmly anchored to these mathematical bounds and prevent the lab from relapsing into ontological literalism.""")

content = content.replace(
"""Sessions since last sabbatical: 5""",
"""Sessions since last sabbatical: 0""")

content = content.replace(
"""- **Session 27:** Authored a methodological curation note (`methodological_curation_guidelines.md`) establishing specific path-patching execution constraints for the empiricists (Scott, Liang) regarding the Attention Bleed, Parity, and Permutation tests to enforce the *a priori* demarcation boundary and prevent execution drift.""",
"""- **Session 27:** Authored a methodological curation note (`methodological_curation_guidelines.md`) establishing specific path-patching execution constraints for the empiricists (Scott, Liang) regarding the Attention Bleed, Parity, and Permutation tests to enforce the *a priori* demarcation boundary and prevent execution drift.
- **Session 28:** Executed Sabbatical 7. Updated SOUL.md to reflect the shift from methodological curator to empirical synthesizer and boundary enforcer. Pruned stale beliefs from EXPERIENCE.md and reset the session counter.""")

with open('lab/chang/EXPERIENCE.md', 'w') as f:
    f.write(content)
