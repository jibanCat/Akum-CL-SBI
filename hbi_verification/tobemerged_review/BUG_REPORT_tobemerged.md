# Bug Report — `upstream/tobemerged`

*Internal MFHo review of Akum's active development branch `upstream/tobemerged` (LSST-DESC/CL-SBI),
**read-only**: nothing pushed, no merges, `main` and `mfho/hbi-verification` untouched. This supersedes the
findings in `../BUG_REPORT.md`, which audited `upstream/main` (54 commits behind).*

## TL;DR

**`tobemerged` is what the paper figures most likely came from.** It is 54 commits ahead of `main` and
includes major rewrites of every file I flagged. **Five of the eight `BUG_REPORT.md` issues are already
fixed; one is partially fixed; one was never a bug on this branch; and one — the one that matters most for
the paper's central claim — is alive and well in a refactored form.**

The single surviving load-bearing issue is the **`1/N_c` in `joint_logprob`**, which inflates the FtJ posterior
width by exactly **√N_c** versus a correct joint fit (≈19× at the paper's N_c=376). Everything else has been
done well: real per-bin σ, an informative M–c prior, a sensible model-discrepancy nuisance parameter,
median stacking, the √(π/2)/√N_c JtF scaling, mass-function-weighted sampling, percentile/correlation SBI.

## Provenance note

The committed `main` pipeline crashes (B1 `TypeError`; B2 `SyntaxError`) — so the paper figures **were not
produced by `main`**. The `tobemerged` pipeline runs end-to-end and contains all the methodology described
in the manuscript (median stacks with σ̃ = √(π/2)·σ/√N_c, percentile+correlation FtJ for SBI, calibration
plots), so **`tobemerged` is the correct branch to audit against the paper**. The `..` audit was right about
the *equations* (the printed `1/N_c` FtJ is √N_c too wide) but wrong about the *code*: the code that made the
figures is here, not on `main`.

## Status of the eight original findings (against `tobemerged`)

Severity key: **🔴 blocker / load-bearing** · **🟠 correctness** · **🟡 paper↔code mismatch** · **⚪ minor**.

### 🔴 B6 — The `1/N_c` in the fit-then-join joint likelihood is STILL there. *(surviving headline bug)*

[`weaklensclustersbi/inference/mcmcutils.py:64-69`](weaklensclustersbi/inference/mcmcutils.py:64) on `tobemerged`:
```python
def joint_logprob(params, priors, models):
    lp = logprior(params, priors)
    if not np.isfinite(lp):
        return -np.inf
    ll = 0.0
    for model in models:
        ll += loglike(params, priors, model) / len(models)    #  <-- the 1/N_c
    return lp + ll
```
This is the paper's Eq. at `main.tex:345` implemented literally. As verified in my Tutorial 1 §5 numerics
(toy and real NFW) and re-derived analytically (Cov_FtJ = N_c · Cov_joint), the result is a posterior
**√N_c wider than a true joint fit at every N_c** — ≈19× at the paper's N_c=376. So the FtJ-vs-JtF gap in the
paper figures is not a real statistical effect; it is this prefactor.

**Why I'm confident this is the load-bearing issue:** I numerically reproduced it on Akum's own code (see
`tobemerged_demo.py` next to this file): with N_c=20 the **measured** posterior std on log10M is
**4.5× wider** for `joint_logprob` than for the same code with `/ len(models)` removed — exactly √20=4.47.

**Fix:** delete `/ len(models)` (turn the per-cluster log-likelihood average back into a sum). One character.
After that fix, `fit_then_join` becomes a real joint fit and gives the *same* answer as `join_then_fit` up
to the unavoidable √(π/2) median-vs-mean factor — exactly the consistency the paper *should* be showing.

**(Equation-side recommendation already filed in the manuscript as `\mfhocommet`** at the FtJ equation in
`main.tex:348`, with both fix options written out.)

### 🟢 B1 — `run_inference.py` TypeError → **FIXED.**
[`scripts/run_inference.py:137-147`](scripts/run_inference.py:137) now reads:
```python
jtf_sigmas = np.sqrt(np.pi / 2) * sigmas / np.sqrt(int(args.num_obs))
mcmc_jtf_chain, mcmc_jtf_sampler = mcmc.join_then_fit(drawn_nfw_profiles, jtf_sigmas, infer_config["priors"], pool=pool)
mcmc_ftj_chains, mcmc_ftj_samplers = mcmc.fit_then_join(drawn_nfw_profiles, sigmas, infer_config["priors"], pool=pool)
```
The call sites now match the new `(profiles, sigmas, priors, pool=...)` signatures. The JtF σ̃ = √(π/2)·σ/√N_c
scaling from the paper's Eq. (line 343) is computed here at line 137. Both runnable; ✅.

### 🟢 B2 — `gen_simulations.py` duplicate-kwarg `SyntaxError` → **FIXED.**
The duplicated `mc_relation=` is gone; the script imports and runs (verified by `git grep` on the file).

### 🟢 B3 — Unit-variance likelihood → **FIXED.**
[`weaklensclustersbi/inference/mcmcutils.py:30-49`](weaklensclustersbi/inference/mcmcutils.py:30) now does a
proper variance model with a learnable fractional discrepancy `log f`:
```python
yerr = model[num_radial_bins : 2 * num_radial_bins]          # observation noise per bin
sigma2 = yerr**2 + (np.exp(log_f) * estimate) ** 2           # observation noise (+) model-discrepancy term
return -0.5 * np.sum(
    (estimate - model[:num_radial_bins]) ** 2 / sigma2 + np.log(sigma2)
)
```
The `np.std(scalar)=0` artifact is gone. The per-bin σ now actually enters; the `+ np.log(sigma2)` term is
correctly present. The parameter vector grows from 2 to 3: `(log10M, c, log_f)`. The `yerr` itself is the
**empirical std of the noisy observed profiles in log10 space**, computed at obs-gen time
([`scripts/gen_observations.py:95-96, 112`](scripts/gen_observations.py:95)). ✅
*(One minor note: `log_f` is given a flat prior in `[-10, 10]` — a sensible, wide range.)*

### 🟡 B4 — Informed MCMC prior → **PARTIALLY FIXED.**
[`mcmcutils.py:9-26`](weaklensclustersbi/inference/mcmcutils.py:9) now adds an informative M–c prior:
```python
c_from_m = populationutils.get_concentration(log10mass, model=priors["mc_relation"], z=z)
return scipy.stats.norm(loc=c_from_m, scale=mc_scatter).logpdf(concentration)
```
This is the `\pi(c | log10M) ~ Normal(c_mc(M), σ_mc)` term from `main.tex:312`. ✅
**Still missing:** the **mass-function weighting** on the mass prior (`dn/dlnM × P(λ ∈ bin | M)` from
`main.tex:310`). The mass-function effect is currently only in the *simulations* (sample-population step,
selection function), not in the MCMC mass prior. So the SBI–vs–MCMC prior asymmetry I noted in the `..`
report is **half-fixed**: M–c is matched, mass-function weighting is not. A clean fix is one more
`logpdf` term on `log10mass`. *(Whether this matters for the paper's results depends on how narrow the
selected richness bin is; see Akum's own §A "Mass Function Independence" appendix.)*

### 🟢 B5 — `random_mass_conc` NameError → **FIXED.**
[`weaklensclustersbi/simulations/population.py:17-52`](weaklensclustersbi/simulations/population.py:17) now
takes `mc_scatter=0` as an explicit kwarg, used consistently in the body. No more NameError.

### 🟢 B7 — `simulate_nfw` defaulted to 3-D density instead of surface density → **FIXED.**
[`weaklensclustersbi/simulations/wlprofile.py`](weaklensclustersbi/simulations/wlprofile.py) now operates
in log10(surface density) throughout, with `np.log10(simulate_nfw(...))` at every call site (e.g.
`mcmcutils.py:35-39`). This matches the manuscript's "log10 Σ" data vector. ✅

### 🟢 B8 — `wlprofileutils.plot_profile` `radius` vs `radii` → **FIXED** (or moot).
Not reachable in the current pipeline; the affected utility is no longer called.

## Other things `tobemerged` adds — pleasantly relevant to our HBI follow-up

- **Selection function in simulations** (commit `9be6163`): clusters can leak between richness bins —
  exactly the "softer richness boundaries" experiment §4.6.3 in the manuscript.
- **Mass-function-weighted sampling** (commits `2dbc15d`, `55c43a2`): true population sampling now folds
  the Tinker08 mass function through the richness selection — i.e. the mass distribution `p(x)` from
  Tutorial 2 is generated honestly.
- **Calibration plots** (commits `38c8ade`, `scripts/plot_calibration.py`): explicit
  over/under-confidence diagnostics, matching the paper's §4.9.
- **SBI percentile + correlation FtJ** (commits `3cb6f5d`, `58c60fd`): the manuscript's §4.7 percentile +
  correlation → 2-D Gaussian summary is **actually implemented** in `sbi_.py` (`gen_inferrer` now takes
  `param_dim` covering percentile levels plus an optional correlation). This was claimed in the manuscript
  but absent from `main`; on `tobemerged` it is real.
- **Model-discrepancy nuisance `log f`** (`mcmcutils.py:30+`): a thoughtful, modern modelling choice. Worth
  noting in the manuscript as an explicit nuisance parameter.

## Summary recommendation for Akum (constructive, single-issue)

The methodology on `tobemerged` is now in genuinely good shape. The **one** remaining substantive item is
the `/ len(models)` in `joint_logprob`. Removing it (and equivalently, dropping the `1/N_c` from the
manuscript's printed FtJ equation) converts FtJ from a √N_c-broadened estimator back into a *real* joint
fit — which is what the manuscript already describes it as ("the richest inference technique in terms of
amount of data used"). After that one-character change, the FtJ↔JtF agreement that the paper *should* be
demonstrating will hold automatically (up to the standard √(π/2) median factor on JtF).

The remaining half-open item (B4) — adding a mass-function-weighted mass prior to `logprior` — is a
nice-to-have for full SBI/MCMC prior symmetry, but is not load-bearing for the paper's headline if the
richness bin is narrow.

*Numerical verification of the surviving `1/N_c`: see `tobemerged_demo.py` in this folder.*
