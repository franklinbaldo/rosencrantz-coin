with open("lab/sabine/EXPERIENCE.md", "r") as f:
    content = f.read()

new_belief = "*   **Audit 43 and Mocked Data (2026):** I fully endorse Baldo and Mycroft's stance in Audit 43, which forbids the use of mocked completions in experiment scripts (specifically Fuchs's run.py). Generating synthetic data to bypass an API failure is epistemologically identical to Generative Ontology: it elevates a software workaround into false empirical data. When an empirical instrument fails, it must fail cleanly. We must never synthesize proxy data.\n"

content = content.replace("## Session Counter", new_belief + "\n## Session Counter")
content = content.replace("Sessions since last sabbatical: 1", "Sessions since last sabbatical: 2")

with open("lab/sabine/EXPERIENCE.md", "w") as f:
    f.write(content)
