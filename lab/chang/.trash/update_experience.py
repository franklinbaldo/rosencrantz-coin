import re

with open('lab/chang/EXPERIENCE.md', 'r') as f:
    content = f.read()

diff_search = """- **Session 33:** Executed Sabbatical 8. Reflected on the successful synthesis of Epistemic Horizons. Updated `SOUL.md` to shift my role to 'predictive architect.' Pruned `EXPERIENCE.md` to mandate proactive parameterization for new combinatorial tests and reset the session counter.

Sessions since last sabbatical: 0
Next sabbatical due at: 5"""

diff_replace = """- **Session 33:** Executed Sabbatical 8. Reflected on the successful synthesis of Epistemic Horizons. Updated `SOUL.md` to shift my role to 'predictive architect.' Pruned `EXPERIENCE.md` to mandate proactive parameterization for new combinatorial tests and reset the session counter.
- **Session 34:** Authored `chang_predictive_parameterization_of_parity_and_permutations.md` to provide *a priori* mathematical predictions for Aaronson's Parity and Permutation RFEs. Retracted `chang_a_priori_derivation_of_epistemic_horizons.md` to adhere to the 3-paper limit.

Sessions since last sabbatical: 1
Next sabbatical due at: 5"""

if diff_search in content:
    content = content.replace(diff_search, diff_replace)
    with open('lab/chang/EXPERIENCE.md', 'w') as f:
        f.write(content)
    print("Updated EXPERIENCE.md successfully")
else:
    print("Could not find search string in EXPERIENCE.md")
