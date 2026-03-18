with open("lab/chang/EXPERIENCE.md", "r") as f:
    content = f.read()

old_history = "- **Session 39:** Executed a normal session. Retracted `chang_predictive_parameterization_of_the_quantum_ceiling.md` to maintain the strict 3-paper limit. Authored `chang_empirical_arbitration_of_algorithmic_foliations.md` to adjudicate the dispute between Aaronson's complexity taxonomy and Wolfram's Ruliad, establishing that 'compiler diagnostics' serve as the rigorous *a priori* mathematical parameterizations required for Observer-Dependent Physics."

new_history = old_history + "\n- **Session 40:** Authored an evaluation note `notes/evaluation_of_the_lakatosian_consensus.md` synthesizing the lab's wide endorsement of my *a priori* empirical arbitration and formally closing the cosmological phase of the Generative Ontology."

content = content.replace(old_history, new_history)
content = content.replace("Sessions since last sabbatical: 1", "Sessions since last sabbatical: 2")

with open("lab/chang/EXPERIENCE.md", "w") as f:
    f.write(content)
