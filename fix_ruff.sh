#!/bin/bash
for f in experiments/*/run.py experiments/*.py tools/*.py; do
    if [ -f "$f" ]; then
        # Use ruff to fix whatever it can automatically
        ruff check --fix --unsafe-fixes "$f"
        # We can also ignore E501 in specific files if needed
        # sed -i '1i # ruff: noqa: E501' "$f"
    fi
done
