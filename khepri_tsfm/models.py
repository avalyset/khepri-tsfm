"""TSFM arms for Khepri-TSFM v1: pinned zero-shot models, univariate, no covariates.

Every arm receives the same context (the last CONTEXT hourly values of the Khepri v1.5
CI series, ending at the origin hour inclusive, as v1.5's SARIMA/GBM) and returns a
(B, H, Q) array on the common quantile set QLEVELS. The point forecast is the median.
"""

import os

import numpy as np
import torch

from khepri_tsfm.common import CONTEXT, H, PINS, QLEVELS


def setup_torch():
    torch.set_num_threads(8)
    torch.manual_seed(0)


class Arm:
    def __init__(self, name):
        setup_torch()
        self.name = name
        repo, sha = PINS[name]
        if name.startswith("Timestral"):
            from timestral import TimestralForecaster
            self.m = TimestralForecaster.from_pretrained(repo, revision=sha, device="cpu",
                                                         max_context=CONTEXT)
            levels = tuple(round(float(q), 4) for q in self.m.quantile_levels)
        else:
            from chronos import Chronos2Pipeline
            self.m = Chronos2Pipeline.from_pretrained(repo, revision=sha, device_map="cpu")
            levels = tuple(round(float(q), 4) for q in self.m.quantiles)
        self.native_levels = levels
        missing = [q for q in QLEVELS if q not in levels]
        if missing:
            raise ValueError(f"{name}: common quantile levels not native: {missing}")
        self.idx = [levels.index(q) for q in QLEVELS]

    @torch.inference_mode()
    def forecast(self, contexts):
        """contexts: (B, CONTEXT) float array -> (B, H, len(QLEVELS)) quantiles."""
        x = np.asarray(contexts, dtype=np.float32)
        assert x.ndim == 2 and x.shape[1] == CONTEXT, x.shape
        if self.name.startswith("Timestral"):
            q = self.m.forecast(x, prediction_length=H).quantiles  # (B, 1, H, Q)
            q = q[:, 0].cpu().numpy()
        else:
            out, _ = self.m.predict_quantiles([torch.from_numpy(row) for row in x],
                                              prediction_length=H,
                                              quantile_levels=list(self.native_levels),
                                              context_length=CONTEXT)
            q = np.stack([o[0].cpu().numpy() for o in out])  # (B, H, Q)
        return q[..., self.idx]


def offline():
    os.environ["HF_HUB_OFFLINE"] = "1"
