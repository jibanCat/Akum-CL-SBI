"""
Cosmology- and colossus-INVARIANT verification of the FTJ vs JTF Bayesian question.

Strategy (per MFHo): the FTJ/JTF difference is a pure likelihood-combination math
question, independent of the forward model. So we replicate the repo's EXACT MCMC
inference logic verbatim (citations below) and replace ONLY the forward model
(simulate_nfw) with a trivial LINEAR map theta -> data vector. Linear+Gaussian lets
us cross-check the sampler against closed-form posteriors.

Repo functions replicated verbatim:
  - mcmcutils.logprior   (mcmcutils.py:5-13)   flat constant within a box
  - mcmcutils.loglike    (mcmcutils.py:16-23)  UNIT-VARIANCE: error=std(scalar)=0
  - mcmcutils.logprob    (mcmcutils.py:26-30)
  - mcmc.run_mcmc        (mcmc.py:18-44)        100 walkers, 500 burn + 2000 steps
  - mcmc.join_then_fit   (mcmc.py:59-66)        MEAN profile (not median), 1 fit
  - mcmc.fit_then_join   (mcmc.py:47-56)        per-cluster fit, np.vstack of chains
Only change: `forward(theta)` replaces `simulate_nfw(...)`.
"""
import numpy as np
import emcee
np.random.seed(2807)  # matches repo mcmc.py:5

# ---------------- TOY FORWARD MODEL (replaces simulate_nfw) ----------------
N_R = 30
xgrid = np.linspace(0.0, 1.0, N_R)
X = np.column_stack([np.ones(N_R), xgrid])   # col0 ~ "amplitude/mass", col1 ~ "tilt/conc"
def forward(theta):                          # stand-in for wlprofile.simulate_nfw
    return X @ np.asarray(theta, dtype=float)

# ---------------- VERBATIM REPLICAS OF REPO INFERENCE LOGIC ----------------
def logprior(params, priors):                # repo mcmcutils.py:5-13
    a, b = params
    if not priors['min_log10mass'] < a < priors['max_log10mass']:
        return -np.inf
    if not priors['min_concentration'] < b < priors['max_concentration']:
        return -np.inf
    return np.log(1 / 20)

def loglike(params, model):                  # repo mcmcutils.py:16-23 (unit-variance bug preserved)
    a, b = params
    estimate = forward([a, b])               # repo calls simulate_nfw(...) here
    error = np.std(a ** 2) + np.std(b) ** 2  # == 0 for scalars  (repo line 22)
    return -0.5 * np.sum((estimate - model) ** 2 / np.exp(2 * error) + 2 * error)

def logprob(params, priors, model):          # repo mcmcutils.py:26-30
    lp = logprior(params, priors)
    if not np.isfinite(lp):
        return -np.inf
    return lp + loglike(params, model)

def run_mcmc(truth_val, priors, starts=np.array([1.0, 1.0])):  # repo mcmc.py:18-44 config
    nwalkers, npar, nburn, nsteps = 100, 2, 500, 2000
    sampler = emcee.EnsembleSampler(nwalkers, npar, logprob, args=[priors, truth_val])
    p0 = starts + 0.1 * np.random.randn(nwalkers, npar)
    pos, _, _ = sampler.run_mcmc(p0, nburn, progress=False)
    sampler.reset()
    sampler.run_mcmc(pos, nsteps, progress=False)
    return sampler

def join_then_fit(profiles, priors):         # repo mcmc.py:59-66  (MEAN, then 1 fit)
    mean_profile = np.mean(profiles, keepdims=True, axis=0)
    return run_mcmc(mean_profile, priors).flatchain

def fit_then_join(profiles, priors):         # repo mcmc.py:47-56  (per-cluster fit + vstack)
    chains = [run_mcmc(p, priors).flatchain for p in profiles]
    return np.vstack(chains)

# ---------------- TOY POPULATION OF CLUSTERS ----------------
N_C = 20
pop_mean = np.array([2.0, 1.0])              # population mean of (amplitude, tilt)
pop_scatter = np.array([0.30, 0.50])         # population SPREAD across clusters (true M-c scatter analog)
sigma_noise = 0.10                           # per-bin measurement noise
theta_true = pop_mean + pop_scatter * np.random.randn(N_C, 2)
data = np.array([forward(t) + sigma_noise * np.random.randn(N_R) for t in theta_true])
PRIORS = {'min_log10mass': -100, 'max_log10mass': 100,
          'min_concentration': -100, 'max_concentration': 100}  # effectively flat

# ---------------- RUN THE REPO LOGIC ON THE TOY ----------------
print("running repo join_then_fit (code JTF) ...")
chain_jtf = join_then_fit(data, PRIORS)
print("running repo fit_then_join (code FTJ, vstack of %d per-cluster chains) ..." % N_C)
chain_ftj = fit_then_join(data, PRIORS)

# ---------------- CORRECT REFERENCE LIKELIHOODS (proper sigma) ----------------
# True joint posterior (sum of per-cluster log-L, proper sigma) -> the statistically correct combine.
def loglike_proper(params, model, s):
    return -0.5 * np.sum((forward(params) - model) ** 2 / s ** 2)
def run_custom(logp):
    sampler = emcee.EnsembleSampler(100, 2, logp)
    p0 = np.array([1., 1.]) + 0.1 * np.random.randn(100, 2)
    pos, _, _ = sampler.run_mcmc(p0, 500, progress=False); sampler.reset()
    sampler.run_mcmc(pos, 2000, progress=False)
    return sampler.flatchain
def lp_true_joint(p):
    if np.any(np.abs(p) > 100): return -np.inf
    return sum(loglike_proper(p, d, sigma_noise) for d in data)          # SUM, no 1/N_c
def lp_paper_ftj(p):
    if np.any(np.abs(p) > 100): return -np.inf
    return (1.0 / N_C) * sum(loglike_proper(p, d, sigma_noise) for d in data)  # paper Eq ~345: 1/N_c average
print("running TRUE joint posterior (sum, proper sigma) ...")
chain_true_joint = run_custom(lp_true_joint)
print("running PAPER FTJ eq (1/N_c-averaged, proper sigma) ...")
chain_paper_ftj = run_custom(lp_paper_ftj)

# ---------------- ANALYTIC CROSS-CHECK (linear-Gaussian, closed form) ----------------
XtX = X.T @ X
cov_unit   = np.linalg.inv(XtX)                       # code's unit-variance per-fit covariance
cov_single = sigma_noise ** 2 * np.linalg.inv(XtX)    # correct single-cluster covariance
cov_joint  = sigma_noise ** 2 * np.linalg.inv(N_C * XtX)   # correct joint (sum) -> 1/N_c tighter
cov_paper  = sigma_noise ** 2 * np.linalg.inv(XtX)    # paper 1/N_c-avg -> = single-cluster width
# code FTJ mixture variance ~ per-fit cov_unit + covariance of the per-cluster centers theta_hat_j
theta_hat = np.array([np.linalg.solve(XtX, X.T @ d) for d in data])
cov_centers = np.cov(theta_hat.T)
cov_codeFTJ_pred = cov_unit + cov_centers

def std2(chain): return np.std(chain[:, 0]), np.std(chain[:, 1])
def a(cov): return np.sqrt(cov[0, 0]), np.sqrt(cov[1, 1])

print("\n" + "=" * 78)
print("POSTERIOR WIDTHS (std of theta0, theta1)   [N_c=%d clusters, sigma_noise=%.2f]" % (N_C, sigma_noise))
print("=" * 78)
rows = [
    ("code JTF  (repo: mean profile, unit-var)", std2(chain_jtf),        a(cov_unit)),
    ("code FTJ  (repo: per-cluster vstack)     ", std2(chain_ftj),        a(cov_codeFTJ_pred)),
    ("PAPER FTJ (1/N_c avg, proper sigma)      ", std2(chain_paper_ftj),  a(cov_paper)),
    ("TRUE joint (sum, proper sigma)           ", std2(chain_true_joint), a(cov_joint)),
]
print("%-42s | %-19s | %-19s" % ("method", "MCMC std (th0,th1)", "analytic (th0,th1)"))
print("-" * 78)
for name, (e0, e1), (p0, p1) in rows:
    print("%-42s | %7.4f %7.4f   | %7.4f %7.4f" % (name, e0, e1, p0, p1))
print("-" * 78)
print("population spread (true theta_j)          | %7.4f %7.4f   |  (the thing FTJ claims to 'capture')"
      % (pop_scatter[0], pop_scatter[1]))

j0, _ = std2(chain_jtf); f0, _ = std2(chain_ftj)
tj0, _ = std2(chain_true_joint); pf0, _ = std2(chain_paper_ftj)
print("\nKEY RATIOS (theta0):")
print("  code FTJ / code JTF          = %.2f   <- the gap you see in the paper" % (f0 / j0))
print("  PAPER FTJ / TRUE joint       = %.2f   (expected sqrt(N_c) = %.2f)  <- the 1/N_c inflation" % (pf0 / tj0, np.sqrt(N_C)))
print("  code JTF / TRUE joint        = %.2f   (code JTF does NOT tighten by sqrt(N_c): unit-variance bug)" % (j0 / tj0))

# ---------------- FIGURE ----------------
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6.4, 6.0))
    ax.scatter(chain_ftj[::40, 0], chain_ftj[::40, 1], s=3, alpha=0.15, color="tab:orange", label="code FTJ (vstack)")
    ax.scatter(chain_jtf[::40, 0], chain_jtf[::40, 1], s=3, alpha=0.25, color="tab:blue", label="code JTF (mean fit)")
    ax.scatter(chain_true_joint[::40, 0], chain_true_joint[::40, 1], s=3, alpha=0.4, color="tab:green", label="TRUE joint (sum, proper $\\sigma$)")
    ax.scatter(theta_true[:, 0], theta_true[:, 1], marker="*", s=120, color="black", zorder=5, label="true $\\theta_j$ (population)")
    ax.set_xlabel(r"$\theta_0$ (amplitude / 'mass')"); ax.set_ylabel(r"$\theta_1$ (tilt / 'concentration')")
    ax.set_title("FTJ vs JTF is a likelihood-combination artifact\n(toy linear forward model; repo MCMC logic verbatim)")
    ax.legend(loc="upper right", fontsize=8, framealpha=0.9)
    fig.tight_layout(); fig.savefig("/tmp/clsbi_bayes_verify.png", dpi=130)
    print("\nfigure saved -> /tmp/clsbi_bayes_verify.png")
except Exception as e:
    print("\n(plot skipped: %s)" % e)
