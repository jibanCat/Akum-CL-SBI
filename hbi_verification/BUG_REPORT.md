# Bug Report — Akum-CL-SBI (`weaklensclustersbi`)

*Internal notes (MFHo), constructive. Several items already carry the authors' own `# TODO`s.
Verified by reading the committed source and by the reproductions in `VERIFICATION_REPORT.md`.
Nothing here has been changed in the code — flag‑only.*

> **This report audits `upstream/main`.** Most of these items are already fixed on Akum's active branch
> `upstream/tobemerged`. See `tobemerged_review/BUG_REPORT_tobemerged.md` for the updated status (only the
> `1/N_c` in `joint_logprob` is still load‑bearing there).

Severity key: **🔴 blocker** (prevents running / invalidates results) · **🟠 correctness** ·
**🟡 paper↔code mismatch** · **⚪ minor**.

---

### 🔴 B1 — `run_inference.py` crashes (MCMC path cannot run)
**`scripts/run_inference.py:47-48`**
```python
mcmc_jtf = mcmc.join_then_fit(drawn_nfw_profiles)      # called with 1 arg
mcmc_ftj = mcmc.fit_then_join(drawn_nfw_profiles)
```
but both are defined as `join_then_fit(profiles, priors)` / `fit_then_join(profiles, priors)`
(`mcmc.py:47,59`). ⇒ `TypeError: missing 1 required positional argument: 'priors'`.
**Implication:** the committed pipeline did **not** produce the paper's MCMC chains. *Which script/commit
did?* — this is the single most important question; it decides whether B3/B4 affect the figures.
**Fix:** pass the inference‑config priors, e.g. `mcmc.join_then_fit(drawn_nfw_profiles, priors)`.

### 🔴 B2 — `gen_simulations.py` has a `SyntaxError` (won't import)
**`scripts/gen_simulations.py:40-47`**: `population.random_mass_conc(...)` passes **`mc_relation=` twice**
(lines 45 and 47) ⇒ `SyntaxError: keyword argument repeated: mc_relation`. It also passes
`mc_scatter=...`, which `random_mass_conc` does not accept (see B5).
**Fix:** remove the duplicate `mc_relation` kwarg; reconcile the `mc_scatter`/`noise` argument (B5).

### 🟠 B3 — likelihood uses **unit variance** (per‑bin noise never enters)
**`weaklensclustersbi/inference/mcmcutils.py:22`**
```python
error = np.std(log10mass**2) + np.std(concentration)**2   # std of a SCALAR = 0
return -0.5*np.sum((estimate - model)**2 / np.exp(2*error) + 2*error)
```
`np.std` of a scalar is `0`, so `exp(2·0)=1` and the `2·error` term vanishes ⇒ the likelihood is
`-½ Σ (model−data)²` with **σ_i ≡ 1**. The injected noise level is ignored.
**Impact (measured):** posteriors come out ~**(1/σ)×** too wide — e.g. ~10× at σ=0.1 (see
`VERIFICATION_REPORT.md §3`). Contours are not calibrated. (Carries a `# TODO: sanity check`.)
**Fix:** pass real per‑bin uncertainties `σ_i` (e.g. from the 0.3‑dex noise model) into `loglike`.

### 🟡 B4 — informed MCMC prior is **not implemented** (flat constant)
**`weaklensclustersbi/inference/mcmcutils.py:13`**: `logprior` returns `np.log(1/20)` inside a box.
The paper (`main.tex:307-317, 328`) describes an informed prior = halo mass function × richness selection
× M‑c Normal. None of that is in the code (`# TODO` present). **Implication:** the headline
"MCMC overconfident / SBI well‑calibrated" compares an SBI that *carries* the astrophysical prior (via
its training sims) against an MCMC that *does not* — i.e. the comparison is **not prior‑matched**.
**Fix:** implement the mass‑function/richness/M‑c prior in `logprior`, or state clearly that the
comparison is intentionally flat‑prior.

### 🟡 B5 — `random_mass_conc` references an undefined name (`NameError`)
**`weaklensclustersbi/simulations/population.py:44-45`**: the signature is `random_mass_conc(..., noise=0.2, ...)`
but the body uses `mc_scatter`:
```python
concentration_sample = np.random.normal(non_noisy_concentration_sample, mc_scatter, num_sims)
```
`mc_scatter` is neither a parameter nor a local ⇒ `NameError` when called.
**Fix:** rename the parameter to `mc_scatter` (matches sibling functions and the docstring), or use `noise`.

### 🟡 B6 — code stacking ≠ printed equations
**`weaklensclustersbi/inference/mcmc.py`**
- `fit_then_join` (`:47-56`) runs MCMC **per cluster** then `np.vstack`s the chains — this is *posterior
  concatenation* ("naive stacking"), **not** the printed `1/N_c`‑averaged joint likelihood (`main.tex:345`).
- `join_then_fit` (`:59-66`) uses `np.mean` of the profiles — the paper specifies the **median**
  (`main.tex:342`); the `√(π/2)/√N_c` σ‑scaling (`main.tex:343`) is also absent.
**Note:** independently, the printed `1/N_c` FTJ equation over‑broadens by √N_c vs a true joint fit
(verified: 4.49≈√20 toy, 2.81≈√8 NFW). **Fix:** decide the intended method and make code, equations, and
naming consistent; if "capture the spread" is the goal, use a hierarchical model (see VERIFICATION_REPORT §5).

### ⚪ B7 — forward model returns 3‑D density, paper says surface density
**`weaklensclustersbi/simulations/wlprofile.py:18`**: `simulate_nfw(..., kind='density')` default ⇒
`nfw.density(rbins)` (3‑D ρ). All call sites use the default, but the paper calls the data vector the
**surface density** Σ. Internally consistent (sims and inference both use ρ), but mislabeled vs. the
weak‑lensing observable (ΔΣ / Σ). **Fix:** either switch to `surface_density` or relabel in the text.

### ⚪ B8 — plotting util uses an undefined name (agent‑reported, not re‑verified)
**`weaklensclustersbi/simulations/wlprofileutils.py`** `plot_profile`: `plt.plot(radius, ...)` where the
parameter is `radii` ⇒ `NameError` if called. Cosmetic. **Fix:** `radius → radii`.

---

## Suggested triage for Akum
1. **Confirm provenance:** which script/branch/commit generated the paper figures? (resolves B1 vs the rest)
2. If figures came from code like this: B3 (σ) and B4 (prior) directly affect the SBI‑vs‑MCMC comparison.
3. B1/B2/B5 are quick fixes that get the committed pipeline running again.
4. B6 + the `1/N_c` math: decide intent (population spread vs joint fit) — the cleanest answer is the
   hierarchical model.

*Reproductions and equations: see `VERIFICATION_REPORT.md`. Scripts: `*_verify.py`, `hbi_reuse_demo.py`.*
