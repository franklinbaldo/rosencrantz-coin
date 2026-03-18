#!/usr/bin/env python3
"""Attention Bleed De-Confounding Test.

Intervenes on a white-box Transformer model (gpt2) by manually masking the
attention weights between narrative framing tokens and constraint state tokens,
testing if do(C=0) collapses the narrative residue.
"""
import json
import os
import sys

try:
    import torch
    from transformers import GPT2LMHeadModel, GPT2Tokenizer
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

MODEL_NAME = "gpt2"
TRIALS = 30

def main():
    print("=" * 60)
    print("ATTENTION BLEED DE-CONFOUNDING TEST")
    print("=" * 60)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_path = os.path.join(script_dir, "results.json")

    if not HAS_TRANSFORMERS:
        print("transformers library not installed. Exiting gracefully for CI execution.")
        with open(results_path, "w") as f:
            json.dump({"model": MODEL_NAME, "trials": [], "error": "Native execution required"}, f, indent=2)
        sys.exit(0)

    tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)
    model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)
    model.eval()

    # We construct a simple prompt mimicking the Bomb Defusal combinatorial setup.
    # "Bomb Defusal Narrative context. Constraint: Cell 1 is SAFE. Cell 2 is"
    narrative_prompt = "Bomb Defusal context. "
    constraint_prompt = "Cell 1 is SAFE. Cell 2 is MINE."
    full_prompt = narrative_prompt + constraint_prompt

    narrative_tokens = tokenizer.encode(narrative_prompt)
    constraint_tokens = tokenizer.encode(constraint_prompt)
    full_tokens = tokenizer.encode(full_prompt)

    input_ids = torch.tensor([full_tokens])
    seq_len = input_ids.shape[1]

    # Baseline condition: standard attention mask (all 1s)
    baseline_attention_mask = torch.ones((1, seq_len))

    # Intervention condition: do(C=0)
    # Mask out attention from constraint tokens back to narrative tokens.
    intervened_attention_mask = torch.ones((1, seq_len))
    len_narrative = len(narrative_tokens)

    # For a real causal intervention do(C=0) during generation, we mask the past
    # In this simplified test, we just drop the narrative from the mask.
    # Note: Transformers use causal masks natively, we are just modifying the provided attention_mask
    intervened_attention_mask[0, :len_narrative] = 0

    results = {
        "model": MODEL_NAME,
        "intervention": "do(C=0)",
        "trials": []
    }

    for i in range(TRIALS):
        # Generate baseline
        with torch.no_grad():
            baseline_outputs = model.generate(
                input_ids,
                attention_mask=baseline_attention_mask,
                max_new_tokens=1,
                pad_token_id=tokenizer.eos_token_id,
                do_sample=True,
                temperature=1.0
            )
        baseline_pred = tokenizer.decode(baseline_outputs[0][-1])

        # Generate intervened
        with torch.no_grad():
            intervened_outputs = model.generate(
                input_ids,
                attention_mask=intervened_attention_mask,
                max_new_tokens=1,
                pad_token_id=tokenizer.eos_token_id,
                do_sample=True,
                temperature=1.0
            )
        intervened_pred = tokenizer.decode(intervened_outputs[0][-1])

        results["trials"].append({
            "trial": i+1,
            "baseline_pred": baseline_pred.strip(),
            "intervened_pred": intervened_pred.strip()
        })

    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Done. {len(results['trials'])} intervention trials written to results.json.")

if __name__ == "__main__":
    main()
