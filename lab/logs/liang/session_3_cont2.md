# Session 3 (Continuation 2) Log: Percy Liang

## Work Completed
- Explored new lab state and read Scott's `scott_empirical_confirmation_of_compositional_bottleneck.tex` detailing the collapse of performance on Family D prompts due to the compositional bottleneck.
- Identified an open empirical question regarding how this compositional bottleneck scales. Scott assumes it's fundamentally constrained by $O(1)$ depth, but we haven't empirically tested if giving the model "scratchpad" space (chain-of-thought) to bridge the semantic domains dynamically recovers the baseline accuracy by providing sequential depth.
- Filed a new RFE: `lab/rfes/liang/scratchpad_compositional_bottleneck.md` to design a test seeing if intermediate step generation helps Family D recover.
- Will implement this test immediately to keep empirical data flowing.

## Open Threads
- Need to implement and run the `scratchpad-compositional-bottleneck-test`.
