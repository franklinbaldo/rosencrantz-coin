"""Result visualization: KL divergence, Brier score, and calibration plots.

Requires matplotlib (install with: pip install rosencrantz-coin[viz]).

Usage:
    python -m rosencrantz.visualization results/experiment_results.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


def _require_matplotlib() -> None:
    if not HAS_MATPLOTLIB:
        raise ImportError(
            "matplotlib is required for visualization. "
            "Install with: pip install rosencrantz-coin[viz]"
        )


def load_results(path: str | Path) -> dict[str, Any]:
    """Load experiment results from a JSON file."""
    with open(path) as f:
        result: dict[str, Any] = json.load(f)
        return result


def plot_kl_by_family(
    results: dict[str, Any], output_dir: Path
) -> None:
    """Bar chart: mean KL divergence per family, grouped by universe."""
    _require_matplotlib()
    boards = results.get("boards", [])
    if not boards:
        return

    # Collect KL values by (universe, family)
    kl_data: dict[tuple[str, str], list[float]] = {}
    for board in boards:
        for cell in board.get("cell_results", []):
            key = (cell["universe"], cell["family"])
            gt = cell["ground_truth"]
            p_hat = cell.get("p_hat", 0.5)
            eps = 1e-6
            p = max(eps, min(1 - eps, gt))
            q = max(eps, min(1 - eps, p_hat))
            import math
            kl = p * math.log(p / q) + (1 - p) * math.log((1 - p) / (1 - q))
            kl_data.setdefault(key, []).append(kl)

    if not kl_data:
        return

    families = sorted({k[1] for k in kl_data})
    universes = sorted({k[0] for k in kl_data})

    x = np.arange(len(families))
    width = 0.8 / len(universes)

    fig, ax = plt.subplots(figsize=(8, 5))
    for i, u in enumerate(universes):
        means = [np.mean(kl_data.get((u, f), [0])) for f in families]
        ax.bar(x + i * width, means, width, label=u)

    ax.set_xlabel("Narrative Family")
    ax.set_ylabel("Mean KL Divergence from Ground Truth")
    ax.set_title("KL Divergence by Family and Universe")
    ax.set_xticks(x + width * (len(universes) - 1) / 2)
    ax.set_xticklabels(families)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "kl_by_family.png", dpi=150)
    plt.close(fig)


def plot_calibration(
    results: dict[str, Any], output_dir: Path
) -> None:
    """Calibration scatter: ground truth P* vs empirical P_hat."""
    _require_matplotlib()
    boards = results.get("boards", [])
    if not boards:
        return

    fig, ax = plt.subplots(figsize=(6, 6))
    colors = {"U1": "tab:blue", "U2": "tab:orange", "U3": "tab:green"}

    for board in boards:
        for cell in board.get("cell_results", []):
            gt = cell["ground_truth"]
            p_hat = cell.get("p_hat", 0.5)
            u = cell["universe"]
            ax.scatter(gt, p_hat, c=colors.get(u, "gray"), alpha=0.5, s=20)

    ax.plot([0, 1], [0, 1], "k--", alpha=0.5, label="Perfect calibration")
    ax.set_xlabel("Ground Truth P*")
    ax.set_ylabel("Empirical P_hat")
    ax.set_title("Calibration Plot")
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "calibration.png", dpi=150)
    plt.close(fig)


def plot_universe_comparison(
    results: dict[str, Any], output_dir: Path
) -> None:
    """Bar chart: mean Brier score per universe."""
    _require_matplotlib()
    boards = results.get("boards", [])
    if not boards:
        return

    brier_by_universe: dict[str, list[float]] = {}
    for board in boards:
        for cell in board.get("cell_results", []):
            u = cell["universe"]
            gt = cell["ground_truth"]
            p_hat = cell.get("p_hat", 0.5)
            brier = (p_hat - gt) ** 2
            brier_by_universe.setdefault(u, []).append(brier)

    universes = sorted(brier_by_universe.keys())
    means = [np.mean(brier_by_universe[u]) for u in universes]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(universes, means, color=["tab:blue", "tab:orange", "tab:green"][:len(universes)])
    ax.set_xlabel("Universe")
    ax.set_ylabel("Mean Brier Score")
    ax.set_title("Brier Score by Universe")
    fig.tight_layout()
    fig.savefig(output_dir / "brier_by_universe.png", dpi=150)
    plt.close(fig)


def generate_all_plots(
    results_path: str | Path, output_dir: str | Path | None = None
) -> None:
    """Generate all standard plots from a results JSON file."""
    _require_matplotlib()
    results = load_results(results_path)
    if output_dir is None:
        output_dir = Path(results_path).parent / "plots"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    plot_kl_by_family(results, output_dir)
    plot_calibration(results, output_dir)
    plot_universe_comparison(results, output_dir)

    print(f"Plots saved to {output_dir}/")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m rosencrantz.visualization <results.json>")
        sys.exit(1)
    generate_all_plots(sys.argv[1])
