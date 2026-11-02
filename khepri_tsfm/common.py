"""Constants shared by all arms. Kept free of torch: importing torch next to LightGBM
segfaults on macOS (two OpenMP runtimes), so baselines and TSFM run in separate processes."""

H = 96
CONTEXT = 8192
# Common quantile set (DECISIONS [steg 2]): the 21 levels both TSFM families deliver
# natively (measured in step 2); they contain the 80 % (0.1/0.9) and 90 % (0.05/0.95)
# central intervals. SARIMA delivers them from its Gaussian predictive distribution.
QLEVELS = (0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
           0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.99)
QCOLS = tuple(f"q{q:.2f}" for q in QLEVELS)

PINS = {
    "Timestral-5M": ("mistralai/Timestral-5M", "bdd20cfc15a3fea0e4cb5ccef37f8d3ca7aa335f"),
    "Timestral-209M": ("mistralai/Timestral-209M", "9874d252ab0aae16f7f7c999f98f98d6ad7d8365"),
    "Chronos-2": ("amazon/chronos-2", "29ec3766d36d6f73f0696f85560a422f50e8498c"),
}
TSFM_ARMS = tuple(PINS)
BASELINE_ARMS = ("snaive_week", "SARIMA", "GBM")
ARMS = BASELINE_ARMS + TSFM_ARMS
