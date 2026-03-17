import json
import itertools
import numpy as np

with open("workspace/liang/lab/liang/experiments/epistemic-capacity-limit/results.json") as f:
    data = json.load(f)

for n in sorted(set(d["n_boards"] for d in data["trials"])):
    trials = [d for d in data["trials"] if d["n_boards"] == n]

    # We want to measure the average cross-correlation between different boards in the same trial
    correlations = []

    # Construct a matrix of outcomes: rows = trials, cols = boards
    # MINE = 1, SAFE = 0
    matrix = []
    for d in trials:
        row = [1 if x == "MINE" else 0 for x in d["outcomes"]]
        matrix.append(row)

    matrix = np.array(matrix) # shape (n_trials, n_boards)

    for i in range(n):
        for j in range(i+1, n):
            # Calculate pearson correlation between board i and board j across trials
            if np.std(matrix[:, i]) > 0 and np.std(matrix[:, j]) > 0:
                corr = np.corrcoef(matrix[:, i], matrix[:, j])[0, 1]
                correlations.append(corr)
            else:
                correlations.append(0.0) # If a board is constant, correlation is technically undefined, we'll use 0

    avg_corr = np.mean(correlations) if correlations else 0
    print(f"N = {n}: Average cross-board correlation = {avg_corr:.3f}")
