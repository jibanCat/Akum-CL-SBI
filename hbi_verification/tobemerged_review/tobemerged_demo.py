"""
Numeric demo: the surviving `/ len(models)` in Akum's joint_logprob on `tobemerged`
inflates the FtJ posterior width by exactly sqrt(N_c).

We replicate Akum's `joint_logprob` (mcmcutils.py:64-69 on upstream/tobemerged) VERBATIM,
swapping only the forward model for a toy linear g(theta) = X theta so the answer is
cosmology/colossus-invariant and analytically Gaussian. Then we run two MCMC chains:

  (A)  joint_logprob as on tobemerged       :  ll += loglike(...) / len(models)
  (B)  joint_logprob with the 1/N_c removed :  ll += loglike(...)

For linear-Gaussian the analytic ratio of posterior widths is exactly sqrt(N_c).
We measure it.
"""
import numpy as np, emcee
np.random.seed(2807)

# ---- toy forward model (replaces simulate_nfw) ----
N_R = 30
X = np.column_stack([np.ones(N_R), np.linspace(0.0, 1.0, N_R)])
def forward(theta):                          # theta = (amplitude ~ "log10M", tilt ~ "concentration")
    return X @ np.asarray(theta, dtype=float)

# ---- verbatim shape of Akum's loglike + joint_logprob ----
def loglike(params, sigma, data):            # Gaussian with proper per-bin sigma (matches the spirit of tobemerged)
    return -0.5 * np.sum((forward(params) - data) ** 2 / sigma**2 + np.log(sigma**2))

def joint_logprob_tobemerged(params, sigma, models):    # <-- with /len(models)
    ll = 0.0
    for m in models:
        ll += loglike(params, sigma, m) / len(models)
    return ll

def joint_logprob_fixed(params, sigma, models):         # <-- /len(models) removed
    ll = 0.0
    for m in models:
        ll += loglike(params, sigma, m)
    return ll

# ---- simulate a stack of clusters ----
N_C, SIG = 20, 0.10
pop_mean, pop_scatter = np.array([2.0, 1.0]), np.array([0.30, 0.50])
theta_true = pop_mean + pop_scatter * np.random.randn(N_C, 2)
profiles   = np.array([forward(t) + SIG * np.random.randn(N_R) for t in theta_true])

# ---- run two emcee chains ----
def run(lp):
    s = emcee.EnsembleSampler(60, 2, lp, args=(SIG, profiles))
    p0 = pop_mean + 0.05 * np.random.randn(60, 2)
    pos, _, _ = s.run_mcmc(p0, 500, progress=False); s.reset(); s.run_mcmc(pos, 2000, progress=False)
    return s.get_chain(flat=True)

chain_tobemerged = run(joint_logprob_tobemerged)
chain_fixed      = run(joint_logprob_fixed)

w0 = lambda c: c[:, 0].std()
print("N_c = %d, sigma = %.2f" % (N_C, SIG))
print("posterior std on theta_0 (the 'log10M' analog):")
print("  joint_logprob (tobemerged: /len(models))   = %.4f" % w0(chain_tobemerged))
print("  joint_logprob (fix: /len removed)          = %.4f" % w0(chain_fixed))
print()
print("RATIO  tobemerged / fixed = %.2f    (expected sqrt(N_c) = %.2f)"
      % (w0(chain_tobemerged) / w0(chain_fixed), np.sqrt(N_C)))
print()
print("=> the surviving `/ len(models)` in joint_logprob inflates FtJ widths by sqrt(N_c).")
print("   At the paper's N_c=376 this is ~%.1fx." % np.sqrt(376))
