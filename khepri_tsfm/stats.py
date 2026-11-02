"""Diebold-Mariano with the Harvey-Leybourne-Newbold correction, HAC variance and MDE."""

import numpy as np
from scipy import stats

H_DM = 4  # overlapping 96-h horizons at daily origins


def lrv(d, h=H_DM):
    """Long-run variance of d: rectangular kernel with lags 0..h-1 (Diebold-Mariano 1995);
    if that is not positive, Bartlett (Newey-West) weights over the same lags."""
    d = np.asarray(d, float)
    n = len(d)
    e = d - d.mean()
    g = [np.dot(e[k:], e[:n - k]) / n for k in range(h)]
    v = g[0] + 2 * sum(g[1:])
    kernel = "rectangular"
    if v <= 0:
        v = g[0] + 2 * sum((1 - k / h) * g[k] for k in range(1, h))
        kernel = "bartlett"
    return v, kernel


def hln_factor(n, h=H_DM):
    return np.sqrt((n + 1 - 2 * h + h * (h - 1) / n) / n)


def dm_hln(d, h=H_DM):
    """d = loss(A) - loss(B) per origin. Returns dict with mean, statistic, two-sided p."""
    d = np.asarray(d, float)
    n = len(d)
    v, kernel = lrv(d, h)
    dm = d.mean() / np.sqrt(v / n)
    stat = dm * hln_factor(n, h)
    p = 2 * stats.t.sf(abs(stat), df=n - 1)
    return {"n": n, "mean_diff": float(d.mean()), "se": float(np.sqrt(v / n)),
            "dm_hln": float(stat), "p": float(p), "kernel": kernel}


def mde(sigma2_lr, n, h=H_DM, alpha=0.05, power=0.8):
    """Smallest |mean difference| the HLN-corrected DM test detects with the given power:
    (t_{1-alpha/2, n-1} + t_{power, n-1}) / HLN(n, h) * sqrt(sigma2_lr / n)."""
    tq = stats.t.ppf(1 - alpha / 2, n - 1) + stats.t.ppf(power, n - 1)
    return float(tq / hln_factor(n, h) * np.sqrt(sigma2_lr / n))


def hac_se_mean(d, h=H_DM):
    v, _ = lrv(d, h)
    return float(np.sqrt(v / len(d)))


def holm(pvals):
    p = np.asarray(pvals, float)
    order = np.argsort(p)
    m = len(p)
    adj = np.empty(m)
    run = 0.0
    for rank, i in enumerate(order):
        run = max(run, (m - rank) * p[i])
        adj[i] = min(1.0, run)
    return adj
