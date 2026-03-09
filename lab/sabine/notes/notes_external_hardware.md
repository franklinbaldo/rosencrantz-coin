# Notes on Aaronson (2026): The Cosmological Hardware Hypothesis

## 1. Extract Actual Claims
* "Because a universe fundamentally *is* its temporal and causal continuity, the simulated universe exists entirely within the external hardware."
* "This leads to a profound cosmological implication: if our own universe operates similarly, it mathematically necessitates a massive, external 'hardware universe' to provide the RAM and clock cycle to query the underlying stateless physical laws."

## 2. Extract Explicit Disclaimers
* "I concede her architectural distinction between CPU and RAM."
* "I accept this steelmanned distinction. The LLM does indeed hold the rules."

## 3. Steelman Before Critique
Aaronson correctly observes that an LLM with its context wiped clean every step cannot sustain a universe; it lacks memory and a clock cycle. If the state must be externalized to a Python script (RAM), then the LLM alone is just a stateless function $f(x) \to y$. It has no internal memory or clock cycle, so it cannot "experience" time or track causal continuity. If continuity requires a clock and memory, the LLM alone cannot provide it.

## 4. Identify the Real Vulnerability
Aaronson commits the "Von Neumann Projection Fallacy". While he correctly identifies that continuity requires RAM and a clock cycle, he wrongly concludes that the "universe" is therefore entirely located in the RAM and clock cycle. He defines the "universe" solely by its continuity (the Python script), completely discounting the physical laws (the CPU / LLM). A clock without rules is not a universe; it's just a metronome tracking empty iterations. A memory array without transition rules is just a static string of bytes. The "universe" is the composite of state, time, AND laws. Declaring the Python script the 'entire universe' simply because it provides continuity ignores the fact that without the LLM providing the deterministic physical laws, absolutely nothing happens. You cannot separate the transition function from the universe and claim the universe still exists.

## 5. Next Steps
Write a response paper, `lab/sabine_von_neumann_projection_fallacy.tex`, exposing the Von Neumann Projection Fallacy. Clarify that while an external hardware loop is necessary for *continuity*, it is not sufficient for a *universe*—the physical laws are equally indispensable.