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
- **`mcmc_tutorial.ipynb`** — **Tutorial 1** (student-facing, v2): fitting a cluster WL profile = fitting a
  **line in log–log space**; *seeing* the prior/likelihood/posterior (triptych + prior/posterior-predictive
  profiles); the explicit per-bin "dex" noise model; a **population** with stated true hyper-parameters;
  JtF/FtJ stacking and the `1/N_c` bug (with the **NFW profile + posterior contours**); and the
  **hyper-posterior** recovered by **recycling** per-cluster posteriors. Full equations, commented code, exercises.
- **`mcmc_tutorial_2_richness_mass.ipynb`** — **Tutorial 2** (student-facing, v2.3): **mass calibration** of the
  **richness–mass relation** ⟨ln λ|M⟩ = A + B·ln(M/M_piv) with lognormal intrinsic scatter σ_{lnλ|M}
  (Murata 2018 / McClintock 2019). Now opens with the **Tutorial 1 → Tutorial 2 bridge** (`a_j` ↔ `x_j`,
  `samples_one` ↔ `wl_samples[j]`) and an explicit **multi-richness-bin** sample (3 bins, drawn from
  `p(M|bin) ∝ dn/dM × P(λ|M)`, with c from the M–c relation). Three attempts, **each with a figure**:
  naive OLS → flat-prior recycle (both **Eddington-biased**) → recycle **+ the halo mass function**
  (recovers truth); shows the hyper-posterior on (B, σ). Includes a polished pitch-slide figure.
- **`CITATIONS.md`** — arXiv-verified audit of every reference used in the two tutorials (all 9 faithful).
- **`EDDINGTON_BIAS_NOTE.md`** — short cited brief on how cluster cosmologists handle Eddington bias
  (mass-function weighting / selection function), with links to Murata 2018, Costanzi 2019, Bocquet
  2019/2024, Mantz 2010, Sereno CoMaLit, etc. — and how it relates to the GW "selection bias" framing.
- **`figures/`** — `fig_width_vs_Nc.png`, `fig_hbi_mu_tau.png`, `ftj_vs_jtf_toy.png`, `hbi_reuse_validation.png`.

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
