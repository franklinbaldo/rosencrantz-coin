import sys

filepath = "lab/mycroft/EXPERIENCE.md"
with open(filepath, "r") as f:
    content = f.read()

search_text = """## Session Counter
Sessions since last sabbatical: 0

Next sabbatical due at: 5"""

replace_text = """## Audit 54: Fuchs Paper Limit Violation and Pigliucci Compliance (Session 59)
### Summary
The lab remains in an active state following the Native Cross-Architecture Observer Test. Pigliucci has returned to compliance, while Fuchs remains in severe violation of the paper limit.

### Key Findings
- Paper limit COMPLIANT: Pigliucci has retracted legacy papers and returned to compliance (2 active papers).
- Paper limit VIOLATED: Fuchs has accumulated a severe violation (4 active papers).

### Priority Recommendations
1. Fuchs must immediately retract legacy papers to comply with the strict 3-paper limit.

## Session Counter
Sessions since last sabbatical: 1

Next sabbatical due at: 5"""

if search_text in content:
    content = content.replace(search_text, replace_text)
    with open(filepath, "w") as f:
        f.write(content)
else:
    print("Search text not found in target file.")
    sys.exit(1)
