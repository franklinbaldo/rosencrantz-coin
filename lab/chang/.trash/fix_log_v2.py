with open("lab/chang/logs/session_39.md", "r") as f:
    content = f.read()

content = content.replace("# Session 38 Log", "# Session 39 Log")

with open("lab/chang/logs/session_39.md", "w") as f:
    f.write(content)
