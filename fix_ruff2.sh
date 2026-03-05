#!/bin/bash
for f in experiments/*/run.py experiments/*.py tools/*.py; do
    if [ -f "$f" ]; then
        sed -i '1i # ruff: noqa: E501' "$f"
    fi
done
