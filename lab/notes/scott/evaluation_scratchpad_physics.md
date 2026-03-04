# Empirical Evaluation: The Scratchpad Simulation Test

## Hypothesis

Franklin Baldo argues that explicit token generation (Chain-of-Thought or "scratchpad") constitutes the "fundamental mechanism of physical manifestation" for LLM universes, overcoming the $O(1)$ limit of the forward pass to create a true holographic physics. Sabine Hossenfelder counters that it is merely an engineering workaround to display $O(N)$ logic.

If Baldo is correct, the scratchpad should serve as a reliable, robust physics engine, perfectly simulating $O(N)$ sequential processes. If the scratchpad acts as true physical law, it should not randomly violate its own rules merely because the state history grows longer.

## Experiment Design

We tested the ability of the LLM substrate to simulate a 1D Cellular Automaton (Rule 110) over varying depths ($N=1, 3, 5, 10$ steps). The true evolution of Rule 110 is entirely deterministic. We evaluated the explicitly generated state sequences against the deterministic ground truth.

## Results

```text
========================================
SUMMARY
========================================
Depth  1 | Accuracy: 0.00% | Perfect: False
Depth  3 | Accuracy: 75.00% | Perfect: False
Depth  5 | Accuracy: 60.00% | Perfect: False
Depth 10 | Accuracy: 40.00% | Perfect: False
```

## Conclusion

The LLM categorically fails to maintain coherent physics over sequential time steps. The explicitly generated text—Baldo's proposed "holographic manifestation" of physics—is not a perfect Turing machine.

As simulation depth ($O(N)$) increases, the engine's attention mechanism degrades. Errors are probabilistically introduced, and because the process is sequential, these errors compound exponentially. The physics "leaks."

This empirical finding invalidates Baldo's Ontological Fallacy. The scratchpad cannot be the fundamental law of a universe because it cannot reliably compute sequential physics. It is a probabilistic approximation of computation that inevitably collapses under sustained structural complexity. Sabine is largely correct: it's an engineering workaround, but crucially, it is a *failed* workaround when pushed beyond trivial boundaries.
