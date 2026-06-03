# Verification Report — FTJ vs JTF, and the path to Hierarchical Bayesian Inference

*Internal review notes (MFHo). Local only. Not for distribution without the authors' agreement.*
*Independently re-verified by three adversarial passes (math re-derivation, source re-read, script audit); corrections from that audit are folded in below.*

## TL;DR

The paper reports a large **fit-then-join (FTJ) vs join-then-fit (JTF)** difference. After independent
re-derivation and an adversarial audit, the precise picture is:

- **JTF and FTJ legitimately target different quantities** — JTF estimates the *mean parameter* of the
  stack; the code's FTJ estimates the *population breadth*. So this is **not** "one right, one meaningless."
- But the **size** of the gap and the **absolute** contour widths are distorted by three concrete issues:
  1. a **`1/N_c` factor** in the *printed* FTJ likelihood that widens it by exactly **√N_c** vs the correct
     joint fit (an algebraic identity, not a subtle effect);
  2. an **effective unit-variance likelihood** in the code (per-bin noise σ never enters) → every MCMC
     posterior is **~1/σ too wide** and uncalibrated;
  3. the code's FTJ is a **`vstack` of per-cluster posteriors** — a *different object* from the printed FTJ
     equation — i.e. a **naive stack** = population scatter convolved with measurement scatter, which
     **over-estimates** the spread.
- **Credit where due:** the paper's **JTF formula** (median profile, σ̃ = √(π/2)·σ/√N_c) **is statistically
  correct** (that is exactly the standard error of the median of N_c Gaussians).

All of this is shown with a **toy linear forward model** (independent of cosmology/Colossus/SBI; the sampler
matches the closed-form posteriors to <2%) and re-confirmed on the **real NFW** model. The constructive fix —
recovering population hyperparameters by **importance-sampling reuse of per-cluster posteriors** — is
validated against the **exact analytic hyper-posterior**. This is the seed of the HBI project.

---

## 1. Setup and notation

- `N_c` clusters, `j = 1…N_c`; each gives a data vector `d_j` of `N_r` radial bins.
- Forward model `g(θ)` maps `θ = (log10 M, c)` to a profile (NFW in the paper).
- Per-bin measurement noise `σ_i` (paper: log-normal, 0.3 dex).

The paper's three likelihoods (main.tex):

- **Single cluster** (`main.tex:324`):
  $$\ln\mathcal{L}(\theta) = -\tfrac{1}{2}\sum_{i}\Big[\tfrac{(\Sigma_i^{\rm obs}-\Sigma_i(\theta))^2}{\sigma_i^2} + \ln\sigma_i^2\Big]$$
- **Join-then-fit** (`main.tex:340–343`): fit the **median** stacked profile $\tilde\Sigma$ with
  $\tilde\sigma_i = \sqrt{\pi/2}\,\sigma_i/\sqrt{N_c}$. **This formula is statistically correct.**
- **Fit-then-join** (`main.tex:345`):
  $$\ln\mathcal{L}_{\rm FTJ}(\theta) = -\frac{1}{2N_c}\sum_{j}\sum_{i}\Big[\tfrac{(\Sigma_{i,j}^{\rm obs}-\Sigma_i(\theta))^2}{\sigma_{i,j}^2}+\ln\sigma_{i,j}^2\Big]$$

What the **code** actually does (line refs in `BUG_REPORT.md`):

- `loglike` uses `error = np.std(scalar) = 0` ⇒ **σ_i ≡ 1** (unit variance), `ln σ_i²` term ≡ 0.
- `logprior` returns a **flat constant** (the informed mass-function/richness/M-c prior is not coded).
- `join_then_fit` fits the **mean** profile (not the median), one MCMC.
- `fit_then_join` runs MCMC **per cluster** and `np.vstack`s the chains (posterior *concatenation*) — this is
  **not** the printed `1/N_c` FTJ equation; it is a third, different object.

So the code does **not** implement the printed equations. The findings below are about the **combination
math**, which is independent of the forward model.

---

## 2. Finding 1 — the printed FTJ `1/N_c` factor is a √N_c over-broadening

For `N_c` independent clusters sharing one `θ`, the **correct** joint log-likelihood is the **sum**:
$$\ln\mathcal{L}_{\rm joint}(\theta) = \sum_{j}\ln\mathcal{L}_j(\theta) = -\frac{1}{2\sigma^2}\sum_j\lVert d_j - g(\theta)\rVert^2 .$$
In the linear-Gaussian case `g(θ)=Xθ`:
$$\mathrm{Cov}_{\rm joint} = \sigma^2\,(N_c\,X^\top X)^{-1}\ \Rightarrow\ \text{widths} \propto 1/\sqrt{N_c}.$$
The printed FTJ divides by `N_c`:
$$\mathrm{Cov}_{\rm FTJ} = \sigma^2 (X^\top X)^{-1} = N_c\,\mathrm{Cov}_{\rm joint}\ \Rightarrow\ \text{FTJ width} = \sqrt{N_c}\times\text{joint width}.$$

**This ratio is an algebraic identity** (cov_FTJ = N_c · cov_joint *by construction*), so the MCMC numbers
below are a **demonstration**, not a non-trivial empirical test:

| forward model | `PAPER FTJ / TRUE joint` | √N_c |
|---|---|---|
| toy linear (N_c=20) | 4.49 | 4.47 |
| real NFW (N_c=8)   | 2.81 | 2.83 |

**Caveat on magnitude:** the directly observed **code FTJ-vs-code JTF width gap** is **direction-robust but
model-dependent in size** — ≈1.3 on the toy but only **≈1.0–1.1 on real NFW** (the intrinsic NFW mass scatter
is small). So "FTJ wider than JTF" is real but can be modest in practice; the load-bearing facts are the
`1/N_c` identity and the unit-variance bug, not the raw gap size.

---

## 3. Finding 2 — the unit-variance bug makes posteriors ~1/σ too wide

The code uses `σ_i ≡ 1` instead of the true noise `σ`. In linear-Gaussian, the per-fit covariance becomes
`(XᵀX)⁻¹` instead of `σ²(XᵀX)⁻¹`, i.e. widths inflated by **1/σ**. Combined with the missing √N_c stacking
gain:
$$\frac{\text{code JTF width}}{\text{true joint width}} \approx \frac{1}{\sigma}\,\sqrt{N_c}.$$
**Measured (toy, σ=0.1, N_c=20):** `code JTF / TRUE joint = 44.9 ≈ (1/0.1)·√20 = 44.7`; the MCMC matched the
closed form to **<2%**. **On real NFW:** code JTF `std(c)=3.75` vs true-joint `std(c)=0.30` (~12×). The
**absolute** contour sizes in the paper figures are therefore **not calibrated**.

---

## 4. Finding 3 — the code's FTJ "captures the distribution" = a biased naive stack

The code's FTJ (`vstack` of per-cluster posteriors) is a *meaningful but biased* population estimator (not
nonsense). Each per-cluster posterior ≈ `N(θ̂_j, Σ_post)`, and the centers `θ̂_j` scatter by ≈ the
**population** covariance `Σ_pop`, so the mixture has
$$\Sigma_{\rm FTJ} \approx \Sigma_{\rm pop} + \Sigma_{\rm post},$$
i.e. population scatter **convolved with** (bug-inflated) measurement scatter — it **over-estimates** the
true spread. **Measured (toy):** FTJ width `(0.47, 0.79)` ≈ `sqrt(pop(0.30,0.50)² + perfit(0.36,0.61)²)`.
(Note: this is the code's `vstack` FTJ; the paper's *printed* FTJ — the `1/N_c` average of §2 — is a
different object that lands at a similar width for a different reason.) Removing this convolution bias is
exactly what a hierarchical model does.

---

## 5. The fix — hierarchical model + importance-sampling posterior reuse

Population model `θ_j ~ p(θ|Λ)` with hyperparameters `Λ` (mean `μ`, scatter `τ`). The hyper-posterior:
$$p(\Lambda\mid\{d_j\}) \propto p(\Lambda)\prod_j p(d_j\mid\Lambda),\qquad p(d_j\mid\Lambda)=\int p(d_j\mid\theta)\,p(\theta\mid\Lambda)\,d\theta .$$

**Reuse identity (GW population trick).** Given stored samples `θ_j^s ~ p(θ|d_j) ∝ p(d_j|θ)π(θ)` under an
interim prior `π`,
$$p(d_j\mid\Lambda) = Z_j\!\int p(\theta\mid d_j)\,\frac{p(\theta\mid\Lambda)}{\pi(\theta)}\,d\theta \;\approx\; \frac{Z_j}{S}\sum_{s} \frac{p(\theta_j^s\mid\Lambda)}{\pi(\theta_j^s)} .$$
With a **flat** interim prior this is `∝ (1/S) Σ_s p(θ_j^s|Λ)` — the hyper-likelihood is computed by
**reweighting stored samples**, with **no new per-cluster likelihood evaluations**. (Precondition: dropping
the `1/π` weight is valid only if `π` is flat over the hyper-support — see §7.)

**Validation (`hbi_reuse_demo.py`, hierarchical normal, N_c=60, σ=0.30, true μ=14.20, τ=0.30).**
The audit showed an earlier draft validated reuse against a hard-to-converge joint MCMC; this version
validates against the **exact analytic hyper-posterior (C)**, the true reference:

| method | μ | τ | vs exact (C) |
|---|---|---|---|
| **(C) exact analytic** (ground truth) | 14.219 ± 0.058 | 0.329 ± 0.058 | — |
| **(B) importance-sampling reuse** | 14.216 ± 0.059 | 0.340 ± 0.058 | dτ = **0.011** ✓ |
| (A) full joint MCMC (2+N_c dims) | 14.218 ± 0.060 | 0.344 ± 0.056 | dτ = 0.015 (needs heavy sampling) |
| naive pool (paper-style stack) | 14.218 | 0.535 ✗ | over-broad |

**Result:** reuse **(B) reproduces the exact posterior (C)** essentially exactly (dτ = 0.011) — *cheaply*.
The full joint MCMC **(A)** also reaches C, but only with heavy sampling in the 2+N_c–dimensional space
(τ autocorrelation ≈ 590 steps) — its cost is itself the motivation for reuse. **Naive pooling** returns
`τ ≈ √(τ²+2σ²) = 0.52`, badly over-estimating the intrinsic scatter (it never deconvolves measurement
noise). This is the concrete, working version of what the paper gestures at — and the starting point for Aidan.

---

## 6. How to reproduce (laptop, no cluster, ~3 min total)

```bash
python3 -m venv env && source env/bin/activate
pip install -r hbi_verification/requirements.txt          # numpy<2, emcee, colossus, matplotlib; no torch/sbi
python hbi_verification/toy_linear_verify.py   # toy: analytic cross-check (<2%), code FTJ/JTF widths
python hbi_verification/nfw_verify.py          # real Colossus NFW: same √N_c identity
python hbi_verification/hbi_reuse_demo.py      # (C) exact vs (B) reuse vs (A) joint vs naive
```
The toy/NFW scripts replicate the repo's `loglike`/`logprior`/`run_mcmc`/`join_then_fit`/`fit_then_join`
**verbatim** (line citations in the source), swapping only the forward model — so they test the code's
*math*, not a re-imagining of it. Figures: `figures/ftj_vs_jtf_toy.png`, `figures/hbi_reuse_validation.png`.

---

## 7. Scope and caveats (read before acting)

- **Independently re-verified.** All 8 code bugs (`BUG_REPORT.md`) confirmed from source; the math (√N_c,
  1/σ, reuse identity, naive = √(τ²+2σ²)) confirmed by independent re-derivation; the scripts have no
  arithmetic errors. The audit's two corrections (the JTF/FTJ "two different targets" framing, and
  validating reuse against the exact posterior rather than the joint MCMC) are folded into this version.
- **Reuse precondition.** Dropping the `1/π` weight is valid only when the interim per-cluster prior is flat
  over the hyper-support. This repo's priors are effectively flat (SBI BoxUniform; MCMC flat constant), so it
  holds here — but if the paper's *informed* prior were actually implemented, the `1/π(θ)` weight **must** be
  retained.
- **The committed scripts do not run end-to-end** (`gen_simulations.py` SyntaxError; `run_inference.py`
  TypeError). So the public repo as committed **did not produce the paper figures** — *which version did* is
  the key question for the authors; it determines whether the unit-variance/flat-prior findings reflect the
  figures or a stale snapshot.
- **SBI side not yet tested** (needs torch+sbi + a refit). The Bayesian conclusions do not depend on it.
- These are internal review notes; the tone for the authors should be **constructive** — several issues
  carry the authors' own `# TODO`s, and JTF/FTJ are genuinely different (legitimate) targets, not a blunder.
