import json

with open("workspace/liang/lab/liang/experiments/epistemic-capacity-limit/results.json") as f:
    data = json.load(f)

for n in sorted(set(d["n_boards"] for d in data["trials"])):
    trials = [d for d in data["trials"] if d["n_boards"] == n]
    all_outcomes = []
    for d in trials:
        all_outcomes.extend(d["outcomes"])
    safe = all_outcomes.count("SAFE")
    mine = all_outcomes.count("MINE")
    total = len(all_outcomes)
    print(f"N = {n}: P(SAFE) = {safe/total:.3f}, P(MINE) = {mine/total:.3f} | Total: {total}")
