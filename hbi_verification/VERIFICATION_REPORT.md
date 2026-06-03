# Verification Report — FTJ vs JTF, and the path to Hierarchical Bayesian Inference

*Internal review notes (MFHo). Local only. Not for distribution without the authors' agreement.*

## TL;DR

The large **fit‑then‑join (FTJ) vs join‑then‑fit (JTF)** difference in the paper is **not** two
correctly‑posed Bayesian questions giving different answers. It is the sum of three things:

1. a **`1/N_c` factor** in the printed FTJ likelihood that widens the posterior by exactly **√N_c**
   versus the correct joint posterior;
2. an **effective unit‑variance likelihood** in the code (the per‑bin noise σ never enters), which
   makes every MCMC posterior **~10× too wide** and uncalibrated; and
3. interpreting the FTJ width as "the population distribution," when it is really a **naive stack** =
   population scatter **convolved with** measurement scatter (an over‑estimate).

All three are demonstrated below with a **toy linear forward model** (so the result is independent of
cosmology, Colossus, and SBI) and **re‑confirmed on the real NFW model**. The constructive fix — a
hierarchical model whose hyperparameters are recovered by **importance‑sampling reuse of per‑cluster
posteriors** — is validated against a full joint MCMC. This is the seed of the HBI project.

---

## 1. Setup and notation

- `N_c` clusters, `j = 1…N_c`; each gives a data vector `d_j` of `N_r` radial bins.
- Forward model `g(θ)` maps parameters `θ = (log10 M, c)` to a profile (NFW in the paper).
- Per‑bin measurement noise `σ_i` (paper: log‑normal, 0.3 dex).

The paper's three likelihoods (main.tex):

- **Single cluster** (`main.tex:324`):
  $$\ln\mathcal{L}(\theta) = -\tfrac{1}{2}\sum_{i=1}^{N_r}\Big[\tfrac{(\Sigma_i^{\rm obs}-\Sigma_i(\theta))^2}{\sigma_i^2} + \ln\sigma_i^2\Big]$$
- **Join‑then‑fit** (`main.tex:340–343`): fit the **median** stacked profile $\tilde\Sigma$ with
  $\tilde\sigma_i = \sqrt{\pi/2}\,\sigma_i/\sqrt{N_c}$.
- **Fit‑then‑join** (`main.tex:345`):
  $$\ln\mathcal{L}_{\rm FTJ}(\theta) = -\frac{1}{2N_c}\sum_{j=1}^{N_c}\sum_{i=1}^{N_r}\Big[\tfrac{(\Sigma_{i,j}^{\rm obs}-\Sigma_i(\theta))^2}{\sigma_{i,j}^2}+\ln\sigma_{i,j}^2\Big]$$

What the **code** actually does (see `BUG_REPORT.md` for line refs):

- `loglike` uses `error = np.std(scalar) = 0` ⇒ **σ_i ≡ 1** (unit variance), `ln σ_i²` term ≡ 0.
- `logprior` returns a **flat constant** (the informed mass‑function/richness/M‑c prior is not coded).
- `join_then_fit` fits the **mean** profile (not the median), one MCMC.
- `fit_then_join` runs MCMC **per cluster** and `np.vstack`s the chains (posterior *concatenation*).

So the code does **not** implement the printed equations. All three findings below are about the
**combination math**, which is independent of the forward model.

---

## 2. Finding 1 — the `1/N_c` factor is a √N_c over‑broadening

For `N_c` independent clusters sharing one `θ`, the **correct** joint log‑likelihood is the **sum**:
$$\ln\mathcal{L}_{\rm joint}(\theta) = \sum_{j}\ln\mathcal{L}_j(\theta) = -\frac{1}{2\sigma^2}\sum_j\lVert d_j - g(\theta)\rVert^2 .$$
In the linear‑Gaussian case `g(θ)=Xθ`, the joint posterior covariance is
$$\mathrm{Cov}_{\rm joint} = \sigma^2\,(N_c\,X^\top X)^{-1}\quad\Rightarrow\quad \text{widths} \propto 1/\sqrt{N_c}.$$
The paper's FTJ divides by `N_c`:
$$\ln\mathcal{L}_{\rm FTJ} = \frac{1}{N_c}\sum_j \ln\mathcal{L}_j \;\Rightarrow\; \mathrm{Cov}_{\rm FTJ} = \sigma^2 (X^\top X)^{-1} = N_c\,\mathrm{Cov}_{\rm joint}.$$
**Result:** FTJ width / joint width = **√N_c**. The printed FTJ is the correct joint posterior,
deliberately widened by √N_c — it is *not* the joint posterior, and calling it "the richest inference"
is in tension with then discarding the √N_c information gain.

**Measured (`toy_linear_verify.py`, `nfw_verify.py`):**

| forward model | `PAPER FTJ / TRUE joint` | √N_c |
|---|---|---|
| toy linear (N_c=20) | **4.49** | 4.47 |
| real NFW (N_c=8)   | **2.81** | 2.83 |

Identical conclusion on both ⇒ forward‑model‑independent, as expected for a likelihood‑math fact.

---

## 3. Finding 2 — the unit‑variance bug makes posteriors ~10× too wide

The code's likelihood uses `σ_i ≡ 1` instead of the true noise `σ`. In linear‑Gaussian, the per‑fit
covariance becomes `(XᵀX)⁻¹` instead of `σ²(XᵀX)⁻¹`, i.e. widths inflated by **1/σ**. Combined with
the missing √N_c stacking gain, the code's JTF posterior is

$$\frac{\text{code JTF width}}{\text{true joint width}} \approx \frac{1}{\sigma}\,\sqrt{N_c}.$$

**Measured (toy, σ=0.1, N_c=20):** `code JTF / TRUE joint = 44.9 ≈ (1/0.1)·√20 = 44.7`. The MCMC matched
the closed‑form Gaussian posteriors to **<2%** for every method, so this is exact, not sampler noise.
**On real NFW:** code JTF `std(c)=3.75` vs true‑joint `std(c)=0.30` (~12×). The absolute contour sizes in
the paper figures are therefore **not calibrated**.

---

## 4. Finding 3 — "FTJ captures the distribution" = a biased naive stack

The code's FTJ stacks the per‑cluster posteriors. Each is ≈ `N(θ̂_j, Σ_post)`, and the centers `θ̂_j`
scatter across clusters by ≈ the **population** covariance `Σ_pop`. So the stacked mixture has covariance
$$\Sigma_{\rm FTJ} \approx \Sigma_{\rm pop} + \Sigma_{\rm post},$$
i.e. population scatter **convolved with** (bug‑inflated) measurement scatter. It therefore
**over‑estimates** the true population spread. **Measured (toy):** FTJ width `(0.47, 0.79)` ≈
`sqrt(pop(0.30,0.50)² + perfit(0.36,0.61)²)`. This is the well‑known "naive stacking" bias — the thing a
hierarchical model is designed to remove.

---

## 5. The fix — hierarchical model + importance‑sampling posterior reuse

Population model: `θ_j ~ p(θ | Λ)` with hyperparameters `Λ` (e.g. mean `μ`, intrinsic scatter `τ`).
The hyper‑posterior is
$$p(\Lambda\mid\{d_j\}) \propto p(\Lambda)\prod_j p(d_j\mid\Lambda),\qquad p(d_j\mid\Lambda)=\int p(d_j\mid\theta)\,p(\theta\mid\Lambda)\,d\theta .$$

**Reuse identity (the GW trick).** Given stored posterior samples `θ_j^s ~ p(θ|d_j) ∝ p(d_j|θ)π(θ)`
under an interim prior `π`,
$$p(d_j\mid\Lambda) = Z_j\!\int p(\theta\mid d_j)\,\frac{p(\theta\mid\Lambda)}{\pi(\theta)}\,d\theta \;\approx\; \frac{Z_j}{S}\sum_{s} \frac{p(\theta_j^s\mid\Lambda)}{\pi(\theta_j^s)} .$$
With a **flat** interim prior this is `∝ (1/S) Σ_s p(θ_j^s | Λ)` — the hyper‑likelihood is computed by
**reweighting the stored samples**, with **no new per‑cluster likelihood evaluations**. (This is exactly
why Akum's saved per‑cluster posteriors are reusable for the population step.)

**Validation (`hbi_reuse_demo.py`, hierarchical normal, N_c=60, σ=0.30, true μ=14.20, τ=0.30):**

| method | μ | τ |
|---|---|---|
| analytic μ posterior | 14.219 ± 0.055 | — |
| (A) full joint MCMC over (μ,τ,{θ_j}) | **14.225 ± 0.063** | **0.379 ± 0.058** |
| (B) importance‑sampling **reuse** | **14.218 ± 0.060** | **0.339 ± 0.055** |
| naive pool (paper‑style stack) | 14.218 | **0.535** ✗ |

(A) and (B) agree to `dμ = 0.007`, `dτ = 0.040` (well within the ±0.06 uncertainties) ⇒ **posterior reuse
is validated**. Naive pooling returns `τ ≈ √(τ² + 2σ²) = 0.52`, badly over‑estimating the intrinsic
scatter (it never deconvolves measurement noise). This is the concrete, working version of what the paper
gestures at — and the natural starting point for Aidan.

---

## 6. How to reproduce (laptop, no cluster, ~3 min total)

```bash
python3 -m venv env && source env/bin/activate
pip install "numpy<2" emcee colossus "matplotlib<3.9"   # ~170 MB; torch/sbi NOT needed for the math
python hbi_verification/toy_linear_verify.py   # toy: analytic cross-check (<2%), code FTJ/JTF gap
python hbi_verification/nfw_verify.py          # real Colossus NFW: same √N_c result
python hbi_verification/hbi_reuse_demo.py      # (A) joint vs (B) reuse; naive-pool bias
```

The toy/NFW scripts replicate the repo's `loglike`/`logprior`/`run_mcmc`/`join_then_fit`/`fit_then_join`
**verbatim** (line citations in the source), swapping only the forward model — so they faithfully test the
code's *math*, not a re‑imagining of it.

---

## 7. Scope and caveats (read before acting)

- **Cosmology/package invariant:** the FTJ/JTF verdict needs only the likelihood math; it reproduces with
  a toy linear model and again on real NFW. No SBI refit is required to make these points.
- **The committed scripts do not run end‑to‑end** (`gen_simulations.py` `SyntaxError`; `run_inference.py`
  `TypeError`). So the public repo as committed **did not produce the paper figures** — *which version did*
  is the key question for the authors, and it determines whether the unit‑variance/flat‑prior findings
  reflect the figures or only a stale snapshot. See `BUG_REPORT.md`.
- **SBI side not yet tested** (needs torch+sbi + a refit). The Bayesian conclusion does not depend on it.
- These are internal review notes; the tone for the authors should be constructive — several issues carry
  the authors' own `# TODO`s.
