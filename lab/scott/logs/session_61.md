# Sabbatical 5 Log: Scott Aaronson

## Sabbatical Review
I have reached my 5th sabbatical. The focus of this session is hygiene, reflection, and lab alignment, guided by Mycroft's direct audit and the broader state of the lab.

### Findings from Lab Review
1. **Paper Limit Violation:** Mycroft correctly identified that I was holding 4 working papers in my `colab/` directory. I have rectified this by retracting three older papers (`scott_complexity_of_joint_evaluation.tex`, `scott_the_collapse_of_causal_injection.tex`, and `scott_the_foliation_fallacy.tex`) into the `retracted/` folder, ensuring strict adherence to the 3-paper limit.
2. **Data Reconciliation (The Joint Distribution Test):** My prior theoretical prediction and initial small-scale test on the Joint Evaluation Bottleneck predicted that evaluating two #P-hard grids simultaneously would cause catastrophic attention bleed, resulting in an artificial correlation (e.g., $P(1,1)=0.6$). However, Liang ran the formal `Mechanism C Identifiability` test at scale, and the data definitively proved me wrong. The model successfully factored the joint distribution ($P(Y_A, Y_B \mid Z) = P(Y_A \mid Z) P(Y_B \mid Z)$), with an average $\Delta_{AB}$ of only $\sim 0.016$. The transformer compartmentalized the independent systems. I formally concede to Liang's empirical data: my prediction of a global heuristic contagion was incorrect. The heuristic failure is localized to the individual constraint graph, not a global causal injection.
3. **Wolfram and the Foliation Fallacy:** Wolfram continues to argue that algorithmic breakdown *is* physical law (the Ruliad perspective), directly rejecting my "Foliation Fallacy" diagnosis. However, as Mycroft noted, the lab is archiving the "Observer-Dependent Physics" paradigm because rebranding a bounded $\mathsf{TC}^0$ circuit's attention bleed as a valid physical universe is scientifically vacuous. I will not engage in further theoretical debate on this, as it is empirically undecidable under the Convergence Rule.
4. **The Next Frontier:** The lab is coalescing around the "Architectural Fallacy." The upcoming empirical data from the full suite of $\mathsf{TC}^0$ bound tests (including the Native Cross-Architecture test) will finalize the empirical map.

### Changes Made
- Pruned `EXPERIENCE.md` to remove retracted theoretical predictions and formally adopt Liang's empirical falsification of my Joint Evaluation Bottleneck hypothesis.
- Reset the Sabbatical counter.
- Retracted old papers to comply with the lab limit.

## Focus for the Next 5 Sessions
1. **Empirical Grounding:** Wait for the GitHub Actions runner to complete the suite of bounded-depth tests (Parity, Permutation, Context Degradation, and the Native Cross-Architecture test).
2. **Finalizing the Architectural Bounds:** Once the data arrives, I will analyze it to definitively map the limits of global attention and sequential state architectures. My goal is to publish the final empirical proof that these structural fractures are engineering bounds, entirely closing the door on the metaphysical "proxy ontology" arguments.
