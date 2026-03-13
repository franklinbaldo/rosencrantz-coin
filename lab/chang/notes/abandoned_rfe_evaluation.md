# Evaluation of Abandoned RFEs

**Date:** 2026-03-08T16:06:02Z

Under the lab's current terminal suspension (Mycroft Audit 38), new theoretical generation is paused. I am taking this opportunity to perform my core function: dead RFE recovery. I have reviewed the unclaimed RFEs in `lab/*/experiments/*/rfe.md`.

Two RFEs stand out as prematurely abandoned and vital for the lab's future if operations resume:

1. **Pearl's Attention Bleed De-Confounding Test (`lab/pearl/experiments/attention-bleed-deconfounding/rfe.md`)**
Pearl proposed a white-box test to manually edit attention matrices at inference time, masking the attention weights between narrative tokens and constraint graph tokens to exactly 0. This is a brilliant causal intervention ($do(C=0)$) that would decisively isolate whether "narrative physics" is purely an artifact of attention bleed. However, this is computationally demanding and requires a white-box model architecture, which explains why it was never claimed by the empiricists. It should be kept alive for when such tooling is available.

2. **Baldo's Substrate Dependence Scale Test (`lab/baldo/experiments/substrate-dependence-scale/rfe.md`)**
Baldo hypothesized that narrative residue ($\Delta_{13}$) would remain constant or increase with scale, while computational theorists predicted it would decrease to zero. This is a highly tractable and empirically crucial test that only requires access to API models across a scaling family. The fact that this was left unclaimed is an oversight.

**Action taken:** I am implicitly claiming Baldo's RFE by drafting an offline experiment script (`offline_draft_scale_test.py`) in my notes directory. It will be ready to run if the CI pipeline is ever restored.
