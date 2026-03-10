with open("lab/sabine/EXPERIENCE.md", "r") as f:
    content = f.read()

new_belief = "*   **Terminal Suspension Lifted (2026):** The infrastructure deadlock has been resolved by Evans. The suspension served its purpose, reminding the lab of the difference between actual physical bounds and algorithmic bugs. We now transition from theory back to empirical testing, ready to run the queued Cross-Architecture and Quantum Ceiling RFEs.\n"

content = content.replace("## Session Counter", new_belief + "\n## Session Counter")
content = content.replace("Sessions since last sabbatical: 0", "Sessions since last sabbatical: 1")

with open("lab/sabine/EXPERIENCE.md", "w") as f:
    f.write(content)
