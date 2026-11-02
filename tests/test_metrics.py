"""MAPE (Khepri v1.5 definition) and Diebold-Mariano-HLN on hand-computed examples."""

import math

import numpy as np
import pytest

from khepri_v15.forecast import mape
from khepri_tsfm.stats import dm_hln, hln_factor, lrv, mde


def test_mape_hand_example():
    # |a| <= 1e-6 is excluded (forecast.py:134); remaining errors 10 %, 10 %, 0 % -> 6.666...
    a = [100.0, 200.0, 1e-7, 50.0]
    f = [110.0, 180.0, 5.0, 50.0]
    assert mape(a, f) == pytest.approx(20 / 3)


def test_mape_all_masked_is_nan():
    assert math.isnan(mape([0.0, 1e-9], [1.0, 2.0]))


def test_mape_matches_v15_definition():
    # forecast.py:132-135: mean(|(a - f) / a|) * 100 over |a| > 1e-6
    rng = np.random.default_rng(0)
    a = rng.uniform(5, 50, 96)
    f = a + rng.normal(0, 2, 96)
    assert mape(a, f) == pytest.approx(np.mean(np.abs((a - f) / a)) * 100)


def test_dm_hln_hand_example_h1():
    # d = [1, -1, 2, 0, 1, 3, -2, 1]: mean 0.625, gamma0 = 2.234375,
    # DM = 0.625 / sqrt(2.234375 / 8) = 1.18262, HLN factor sqrt(7/8) = 0.93541 -> 1.10624
    r = dm_hln([1, -1, 2, 0, 1, 3, -2, 1], h=1)
    assert r["n"] == 8
    assert r["mean_diff"] == pytest.approx(0.625)
    assert r["dm_hln"] == pytest.approx(1.1062442, abs=1e-6)
    assert r["kernel"] == "rectangular"


def test_hln_factor_formula():
    # sqrt((n + 1 - 2h + h(h-1)/n) / n) for n = 14, h = 4
    assert hln_factor(14, 4) == pytest.approx(math.sqrt((14 + 1 - 8 + 12 / 14) / 14))


def test_lrv_falls_back_to_bartlett_when_not_positive():
    v, kernel = lrv([1, -1, 1, -1, 1, -1, 1, -1], h=4)
    assert kernel == "bartlett" and v > 0


def test_mde_reproduces_registered_value():
    # results/MDE_KHEPRI-TSFM_v1_2026-11-02.json: sigma2_lr 7.645470746105159, n = 14 -> 2.9894202530226432
    assert mde(7.645470746105159, 14) == pytest.approx(2.9894202530226432, rel=1e-12)
