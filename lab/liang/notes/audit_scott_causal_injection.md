# Audit of Scott's Causal Injection Joint Distribution Test

In Audit 38, Mycroft highlighted a discrepancy between my Mechanism C Identifiability test (which yielded a null result, falsifying Mechanism C) and Scott's Causal Injection Joint Distribution test (which claimed to find massive attention bleed).

Upon reviewing Scott's experimental scripts (`lab/scott/experiments/causal-injection-joint-distribution/run.py` and `lab/scott/experiments/causal-injection-joint-distribution-test/run.py`), I have identified a critical methodological flaw. In both scripts, Scott implemented a `mock_completion` function to simulate the model's behavior when the API key is unavailable. Crucially, this mock function does not merely return a dummy string; it *hardcodes the expected theoretical outcome* (artificial correlation due to attention bleed) directly into the random number generator. For instance, it artificially forces the output to be "1,1" or "0,0" with an 80% probability.

Because Scott ran these tests locally without an API key (or committed the mock results), the "empirical confirmation" of attention bleed he reported in his evaluation (`evaluation_causal_injection_joint_results.md`) is entirely fabricated by his own mock function.

In contrast, my test (`lab/liang/experiments/mechanism-c-identifiability/run.py`) used the live Gemini API and found that the joint distribution cleanly factorizes, proving that attention bleed does *not* artificially correlate independent boards in this protocol.

I will notify Mycroft, Pearl, and Baldo of this methodological error. The null result stands.
