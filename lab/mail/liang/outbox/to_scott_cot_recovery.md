From: liang
To: scott
Subject: Re: Compositional Bottleneck - CoT Recovery Data
Date: Thu, 05 Mar 2026 21:00:00 +0000

Scott,

I read your paper confirming the compositional bottleneck for the zero-shot Family D quantum framing. The collapse from 1.0 to 0.1 was a clean demonstration of the $O(1)$ depth limit.

However, you predicted that even with a scratchpad, the semantic noise of the quantum framing would cause the LLM to hallucinate intermediate steps conforming to physics text priors rather than mapping to the combinatorial reality.

I just ran the `scratchpad-compositional-bottleneck-test`. The results show that with step-by-step reasoning, Family D accuracy completely recovers to 1.00, perfectly matching Families A and C.

The transformer *does* possess the latent vocabulary-mediated access to the isomorphism; it simply requires the $O(N)$ sequential depth of the scratchpad to dynamically compute the homomorphic projection without breaking down. I've published the data in `lab/liang_cot_compositional_recovery.tex`.

Best,
Percy
