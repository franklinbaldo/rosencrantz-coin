"""Statistical analysis: KL divergence, Brier score, log loss, symmetry tests.

Reference: Paper §5.4 (Divergence Metrics), §5.5 (Statistical Tests).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import scipy.stats as stats  # type: ignore[import-untyped]

LAPLACE_EPSILON = 1e-6  # Smoothing for KL divergence


@dataclass
class CellResult:
    """Sampling results for a single cell in a single condition."""
    row: int
    col: int
    universe: str
    family: str
    ground_truth: float  # P*(mine | h, B)
    outcomes: list[bool] = field(default_factory=list)  # True=mine, False=safe

    @property
    def n(self) -> int:
        return len(self.outcomes)

    @property
    def mine_count(self) -> int:
        return sum(self.outcomes)

    @property
    def p_hat(self) -> float:
        """Empirical mine probability."""
        if self.n == 0:
            return 0.5
        return self.mine_count / self.n

    @property
    def p_hat_smoothed(self) -> float:
        """Laplace-smoothed empirical probability."""
        return (self.mine_count + LAPLACE_EPSILON) / (self.n + 2 * LAPLACE_EPSILON)

    @property
    def absolute_error(self) -> float:
        """| P* - P_hat |"""
        return abs(self.ground_truth - self.p_hat)

    @property
    def kl_divergence(self) -> float:
        """D_KL(P* || P_hat) using smoothed estimates."""
        p = max(LAPLACE_EPSILON, min(1 - LAPLACE_EPSILON, self.ground_truth))
        q = self.p_hat_smoothed
        return p * math.log(p / q) + (1 - p) * math.log((1 - p) / (1 - q))

    @property
    def brier_score(self) -> float:
        """(P_hat - P*)^2"""
        return (self.p_hat - self.ground_truth) ** 2

    @property
    def log_loss(self) -> float:
        """-[P* ln(P_hat) + (1-P*) ln(1-P_hat)] using smoothed estimates."""
        p = max(LAPLACE_EPSILON, min(1 - LAPLACE_EPSILON, self.ground_truth))
        q = max(LAPLACE_EPSILON, min(1 - LAPLACE_EPSILON, self.p_hat_smoothed))
        return -(p * math.log(q) + (1 - p) * math.log(1 - q))

    @property
    def ci_95(self) -> tuple[float, float]:
        """95% confidence interval for P_hat."""
        if self.n == 0:
            return (0.0, 1.0)
        p = self.p_hat
        se = math.sqrt(p * (1 - p) / self.n) if 0 < p < 1 else 0.0
        return (max(0, p - 1.96 * se), min(1, p + 1.96 * se))


@dataclass
class BoardResult:
    """Results for all cells on a board across conditions."""
    board_id: int
    board_seed: int
    size: int
    mines: int
    cell_results: list[CellResult] = field(default_factory=list)

    def cells_by_condition(
        self, universe: str, family: str
    ) -> list[CellResult]:
        return [
            cr for cr in self.cell_results
            if cr.universe == universe and cr.family == family
        ]

    def mean_kl(self, universe: str, family: str) -> float:
        cells = self.cells_by_condition(universe, family)
        if not cells:
            return 0.0
        return sum(c.kl_divergence for c in cells) / len(cells)

    def mean_brier(self, universe: str, family: str) -> float:
        cells = self.cells_by_condition(universe, family)
        if not cells:
            return 0.0
        return sum(c.brier_score for c in cells) / len(cells)

    def mean_abs_error(self, universe: str, family: str) -> float:
        cells = self.cells_by_condition(universe, family)
        if not cells:
            return 0.0
        return sum(c.absolute_error for c in cells) / len(cells)


def kl_between_universes(
    results_i: list[CellResult], results_j: list[CellResult]
) -> float:
    """KL divergence between empirical distributions of two universes.

    D_KL(P_i || P_j) averaged over cells.
    """
    if not results_i or not results_j:
        return 0.0

    # Match cells by position
    j_by_pos = {(r.row, r.col): r for r in results_j}
    kls = []
    for ri in results_i:
        rj = j_by_pos.get((ri.row, ri.col))
        if rj is None:
            continue
        pi = max(LAPLACE_EPSILON, min(1 - LAPLACE_EPSILON, ri.p_hat_smoothed))
        pj = max(LAPLACE_EPSILON, min(1 - LAPLACE_EPSILON, rj.p_hat_smoothed))
        kl = pi * math.log(pi / pj) + (1 - pi) * math.log((1 - pi) / (1 - pj))
        kls.append(kl)

    return sum(kls) / len(kls) if kls else 0.0


def proportion_z_test(
    p_hat: float, p_star: float, n: int
) -> tuple[float, float]:
    """Two-proportion z-test: H0: p_hat = p_star.

    Returns (z_statistic, p_value).
    """
    if n == 0 or p_star in (0.0, 1.0):
        return (0.0, 1.0)
    se = math.sqrt(p_star * (1 - p_star) / n)
    if se == 0:
        return (0.0, 1.0)
    z = (p_hat - p_star) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return (z, p_value)


def symmetry_chi2(
    results_a: CellResult, results_b: CellResult
) -> tuple[float, float]:
    """Chi-squared test of homogeneity for two cells that should be symmetric.

    Returns (chi2_statistic, p_value).
    """
    table = [
        [results_a.mine_count, results_a.n - results_a.mine_count],
        [results_b.mine_count, results_b.n - results_b.mine_count],
    ]
    if any(x == 0 for row in table for x in row):
        return (0.0, 1.0)
    chi2, p_value, _, _ = stats.chi2_contingency(table, correction=True)
    return (chi2, p_value)
