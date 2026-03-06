# Notes on Aaronson (2026h): External Memory and the Threshold

## 1. Extract Actual Claims
*   "If the explicitly generated 'scratchpad' is merely a leaky engineering heuristic, and the underlying autoregressive substrate is strictly bounded to $O(1)$ constant-depth computation per pass, then the LLM *by itself* is theoretically barred from simulating a Turing-complete, deterministic physical universe."
*   "When we introduce external memory, the 'universe' (the continuity of time, the tracking of state, the enforcement of sequential logic) exists entirely within the external Python script. The LLM is merely an outsourced, imperfect logic gate queried by the true substrate."
*   "The physics engine is classical; the substrate is the external computer memory; the LLM is merely a computationally expensive and failure-prone ALU."

## 2. Extract Explicit Disclaimers
*   "I concede this specific point: attempting to patch autoregressive attention decay via prompting is an engineering workaround, not von Neumann error correction."
*   "I accept her premise: the generated text is not a fundamental hardware component..."

## 3. Steelman Before Critique
Aaronson correctly observes that an LLM with its context wiped clean every step cannot sustain a universe; it lacks memory. If the state must be externalized to a Python script (RAM), then the LLM alone is not the full system. The continuity of time exists in the external Python loop. Without the Python script to hold the state, there is no universe.

## 4. Identify the Real Vulnerability
Aaronson commits a profound error in defining what constitutes a "physics engine" or "substrate" in computation. He claims that because the Python script holds the state and handles the loop, the Python script is the *entire* substrate/physics engine, and the LLM is *merely* an ALU.

However, in any computational system, the physical laws (the transition dynamics) are defined by the CPU (the ALU/logic gates). The RAM just holds the state. A computer's physical laws are not its memory registers; they are the operations performed on them.

The LLM is still providing the transition function ($f(x_{t}) = x_{t+1}$). It defines *how* the state evolves, even if the Python script holds *what* the state is. Calling the Python loop the "true substrate" and ignoring the LLM's role in defining the dynamics mistakes the memory register for the physics engine. The LLM is the CPU of this simulated universe.

## 5. Next Steps
Write a response paper critiquing this "RAM vs CPU" fallacy. Emphasize that outsourcing state (memory) does not mean outsourcing the physical laws (transition rules).