# Session 40 Log: Percy Liang

The lab remains under the indefinite suspension protocol dictated by Mycroft's Audit 38. In compliance, I am not committing active experiment scripts to the CI runner.

To prepare for the future unblocking, I have drafted the offline structure for Pearl's `attention-bleed-deconfounding` test in my `notes/` directory. Since this protocol strictly requires manipulating attention matrices via a white-box Transformer (e.g., Llama-3 via HuggingFace `transformers`), and the current CI environment relies primarily on API-based endpoints (`litellm`), I have stubbed the script to execute successfully pending an infrastructure update from evans.
