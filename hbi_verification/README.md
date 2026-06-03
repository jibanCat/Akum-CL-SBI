# hbi_verification/

Internal review + verification artifacts for the SBI cluster‑mass paper, and the seed of the
Hierarchical Bayesian Inference (HBI) follow‑up. **Local only — do not push without the authors' OK.**

## Contents
- **`VERIFICATION_REPORT.md`** — human‑readable writeup *with equations*: why FTJ and JTF differ
  (the `1/N_c` √N_c identity, the unit‑variance bug, naive‑stacking; note JTF and FTJ are two different
  *legitimate* targets), and the importance‑sampling posterior‑reuse fix validated against the **exact
  analytic hyper‑posterior**.
- **`BUG_REPORT.md`** — confirmed code issues with `file:line`, impact, and suggested fixes (flag‑only).
- **`toy_linear_verify.py`** — repo MCMC logic verbatim + toy linear forward model; analytic cross‑check
  (<2%); shows the FTJ/JTF math is pure likelihood combination (no cosmology/Colossus/SBI).
- **`nfw_verify.py`** — same comparison on the real Colossus NFW model (confirms the √N_c identity).
- **`hbi_reuse_demo.py`** — (C) exact analytic hyper‑posterior vs (B) importance‑sampling reuse vs
  (A) full joint hierarchical MCMC; reuse (B) matches the exact (C) cheaply, naive pooling over‑estimates τ.
- **`mcmc_tutorial.ipynb`** — executed, narrated tutorial: §1–6 the FtJ/JtF toy + real NFW, §7 the HBI
  reuse validation. Open it to read the results without running.
- **`figures/`** — `ftj_vs_jtf_toy.png`, `hbi_reuse_validation.png`.

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
- ✅ Posterior‑reuse HBI identity: validated against the exact analytic posterior (independently re‑verified).
- ⛔ Not yet: SBI refit (math‑irrelevant to the above), and matching the exact paper magnitudes.
