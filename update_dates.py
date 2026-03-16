with open('lab/pearl/colab/pearl_causal_dag_of_capacity_limit.md', 'r') as f:
    content = f.read()

content = content.replace("**Date:** 2026-03-16T12:43:23Z", "**Date:** 2026-03-16T12:43:37Z")

with open('lab/pearl/colab/pearl_causal_dag_of_capacity_limit.md', 'w') as f:
    f.write(content)

with open('lab/pearl/logs/session_29.md', 'r') as f:
    content = f.read()

content = content.replace("**Date:** 2026-03-16", "**Date:** 2026-03-16T12:44:06Z")

with open('lab/pearl/logs/session_29.md', 'w') as f:
    f.write(content)
