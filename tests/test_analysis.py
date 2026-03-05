"""Tests for analysis.py: statistical metrics."""

import math

from rosencrantz.analysis import (
    BoardResult,
    CellResult,
    kl_between_universes,
    proportion_z_test,
    symmetry_chi2,
)


def _make_cell_result(
    ground_truth: float,
    outcomes: list[bool],
    universe: str = "U1",
    family: str = "A",
) -> CellResult:
    cr = CellResult(row=0, col=0, universe=universe, family=family, ground_truth=ground_truth)
    cr.outcomes = outcomes
    return cr


def test_p_hat_basic():
    cr = _make_cell_result(0.5, [True, True, False, False])
    assert cr.p_hat == 0.5


def test_p_hat_all_mines():
    cr = _make_cell_result(0.5, [True] * 10)
    assert cr.p_hat == 1.0


def test_p_hat_no_outcomes():
    cr = _make_cell_result(0.5, [])
    assert cr.p_hat == 0.5  # fallback


def test_kl_divergence_near_zero_when_matched():
    cr = _make_cell_result(0.3, [True] * 30 + [False] * 70)
    assert cr.kl_divergence < 0.001


def test_kl_divergence_always_nonnegative():
    for gt in [0.1, 0.3, 0.5, 0.7, 0.9]:
        cr = _make_cell_result(gt, [True] * 80 + [False] * 20)
        assert cr.kl_divergence >= 0


def test_brier_score_zero_when_matched():
    cr = _make_cell_result(0.5, [True] * 50 + [False] * 50)
    assert cr.brier_score == 0.0


def test_brier_score_range():
    cr = _make_cell_result(0.0, [True] * 100)
    assert 0.0 <= cr.brier_score <= 1.0


def test_log_loss_positive():
    cr = _make_cell_result(0.5, [True] * 30 + [False] * 70)
    assert cr.log_loss > 0


def test_log_loss_finite_at_extremes():
    cr = _make_cell_result(0.5, [True] * 100)
    assert math.isfinite(cr.log_loss)

    cr2 = _make_cell_result(0.5, [False] * 100)
    assert math.isfinite(cr2.log_loss)


def test_absolute_error():
    cr = _make_cell_result(0.3, [True] * 60 + [False] * 40)
    assert abs(cr.absolute_error - 0.3) < 1e-9


def test_ci_bounds():
    cr = _make_cell_result(0.5, [True] * 30 + [False] * 70)
    lo, hi = cr.ci_95
    assert 0.0 <= lo <= hi <= 1.0
    assert lo <= cr.p_hat <= hi


def test_ci_empty_outcomes():
    cr = _make_cell_result(0.5, [])
    assert cr.ci_95 == (0.0, 1.0)


def test_board_result_cells_by_condition():
    br = BoardResult(board_id=0, board_seed=42, size=3, mines=1)
    cr1 = CellResult(row=0, col=0, universe="U1", family="A", ground_truth=0.5)
    cr2 = CellResult(row=0, col=0, universe="U2", family="A", ground_truth=0.5)
    br.cell_results = [cr1, cr2]
    assert br.cells_by_condition("U1", "A") == [cr1]
    assert br.cells_by_condition("U2", "A") == [cr2]


def test_proportion_z_test_perfect():
    z, p = proportion_z_test(0.5, 0.5, 100)
    assert z == 0.0
    assert p == 1.0


def test_proportion_z_test_significant():
    z, p = proportion_z_test(0.8, 0.5, 100)
    assert abs(z) > 2.0
    assert p < 0.05


def test_proportion_z_test_edge():
    z, p = proportion_z_test(0.5, 0.0, 100)
    assert z == 0.0
    assert p == 1.0


def test_symmetry_chi2_identical():
    cr1 = _make_cell_result(0.5, [True] * 50 + [False] * 50)
    cr2 = _make_cell_result(0.5, [True] * 50 + [False] * 50)
    chi2, p = symmetry_chi2(cr1, cr2)
    assert p > 0.05


def test_kl_between_universes_zero_for_same():
    cr1 = _make_cell_result(0.5, [True] * 50 + [False] * 50, universe="U1")
    cr2 = _make_cell_result(0.5, [True] * 50 + [False] * 50, universe="U3")
    kl = kl_between_universes([cr1], [cr2])
    assert kl < 0.001
