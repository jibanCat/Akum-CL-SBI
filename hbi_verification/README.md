# hbi_verification/

Internal review + verification artifacts for the SBI cluster‑mass paper, and the seed of the
Hierarchical Bayesian Inference (HBI) follow‑up. **Local only — do not push without the authors' OK.**

## Contents
- **`VERIFICATION_REPORT.md`** — human‑readable writeup *with equations*: why FTJ and JTF differ
  (the `1/N_c` √N_c inflation, the unit‑variance bug, naive‑stacking), and the importance‑sampling
  posterior‑reuse fix validated against a full joint MCMC.
- **`BUG_REPORT.md`** — confirmed code issues with `file:line`, impact, and suggested fixes (flag‑only).
- **`toy_linear_verify.py`** — repo MCMC logic verbatim + toy linear forward model; analytic cross‑check
  (<2%); shows the FTJ/JTF gap and the √N_c factor are pure likelihood math (no cosmology/Colossus/SBI).
- **`nfw_verify.py`** — same comparison on the real Colossus NFW model (confirms √N_c on real physics).
- **`hbi_reuse_demo.py`** — (A) full joint hierarchical MCMC vs (B) importance‑sampling reuse of
  per‑cluster posteriors; shows they agree and that naive pooling over‑estimates the scatter.

## Run (laptop, ~3 min, no cluster, no GPU)
```bash
python3 -m venv env && source env/bin/activate
pip install -r hbi_verification/requirements.txt
python hbi_verification/toy_linear_verify.py
python hbi_verification/nfw_verify.py
python hbi_verification/hbi_reuse_demo.py
```

## Status
- ✅ MCMC FTJ/JTF Bayesian question: verified (toy + real NFW), cosmology/package invariant.
- ✅ Posterior‑reuse HBI identity: validated against full joint MCMC.
- ⛔ Not yet: SBI refit (math‑irrelevant to the above), and matching the exact paper magnitudes.
