"""
#2  The constructive fix: hierarchical Bayesian inference by POSTERIOR REUSE.
Toy hierarchical normal model (mass-observable-relation analog):
    population:  m_j ~ N(mu, tau^2)        # mu = mean log-mass, tau = intrinsic scatter
    data:        d_j | m_j ~ N(m_j, sigma^2)
Goal (the project's central claim): recovering the hyperparameters (mu, tau) by
IMPORTANCE-SAMPLING reuse of stored per-cluster posteriors p(m_j|d_j) gives the
same answer as a full joint hierarchical MCMC over (mu, tau, {m_j}) -- with no new
per-cluster likelihood calls. Also shows naive pooling overestimates tau.
"""
import numpy as np, emcee, math
np.random.seed(7)

N_C, SIGMA, MU_TRUE, TAU_TRUE = 60, 0.30, 14.20, 0.30
m_true = MU_TRUE + TAU_TRUE*np.random.randn(N_C)
d = m_true + SIGMA*np.random.randn(N_C)                       # one scalar observable per cluster

# Stored per-cluster posteriors p(m_j|d_j)=N(d_j, sigma^2) under a FLAT prior.
# (stand-in for Akum's SBI/MCMC posterior samples -- the thing we reuse)
S = 4000
post = np.array([d[j] + SIGMA*np.random.randn(S) for j in range(N_C)])   # (N_C, S)

# ---------- (A) FULL JOINT hierarchical MCMC over (mu, log tau, m_1..m_Nc) ----------
def logp_joint(p):
    mu, logtau, m = p[0], p[1], p[2:]
    tau = math.exp(logtau)
    if tau > 5: return -np.inf
    like = -0.5*np.sum(((d - m)/SIGMA)**2)
    pop  = -0.5*np.sum(((m - mu)/tau)**2) - N_C*logtau
    return like + pop + logtau                                # +logtau = Jacobian
ndim = 2 + N_C; nw = 2*ndim
p0 = np.column_stack([MU_TRUE + 0.1*np.random.randn(nw), np.log(0.3) + 0.1*np.random.randn(nw),
                      d[None, :] + 0.1*np.random.randn(nw, N_C)])
sA = emcee.EnsembleSampler(nw, ndim, logp_joint)
pos, _, _ = sA.run_mcmc(p0, 1500, progress=False); sA.reset(); sA.run_mcmc(pos, 3000, progress=False)
A = sA.get_chain(flat=True); muA, tauA = A[:, 0], np.exp(A[:, 1])

# ---------- (B) POSTERIOR REUSE via importance sampling ----------
# Hyper-likelihood (flat per-cluster prior cancels):
#   L(mu,tau) = prod_j  (1/S) sum_s  N(m_j^s | mu, tau^2)
def loghyper(p):
    mu, logtau = p; tau = math.exp(logtau)
    if tau > 5: return -np.inf
    ll = 0.0
    for j in range(N_C):
        w = np.exp(-0.5*((post[j] - mu)/tau)**2)/tau
        ll += math.log(w.mean() + 1e-300)
    return ll + logtau
p0 = np.column_stack([MU_TRUE + 0.1*np.random.randn(10), np.log(0.3) + 0.1*np.random.randn(10)])
sB = emcee.EnsembleSampler(10, 2, loghyper)
pos, _, _ = sB.run_mcmc(p0, 1500, progress=False); sB.reset(); sB.run_mcmc(pos, 4000, progress=False)
B = sB.get_chain(flat=True); muB, tauB = B[:, 0], np.exp(B[:, 1])

# ---------- naive stack (paper-style): pool all per-cluster samples ----------
pooled = post.ravel()
mu_naive, tau_naive = pooled.mean(), pooled.std()

mu_an, sd_an = d.mean(), math.sqrt((SIGMA**2 + TAU_TRUE**2)/N_C)   # analytic mu posterior
print("truth:                 mu=%.3f  tau=%.3f" % (MU_TRUE, TAU_TRUE))
print("analytic mu posterior: mu=%.3f +/- %.3f" % (mu_an, sd_an))
print("-"*64)
print("(A) full joint MCMC :  mu=%.3f +/- %.3f    tau=%.3f +/- %.3f" % (muA.mean(), muA.std(), tauA.mean(), tauA.std()))
print("(B) posterior REUSE :  mu=%.3f +/- %.3f    tau=%.3f +/- %.3f" % (muB.mean(), muB.std(), tauB.mean(), tauB.std()))
print("-"*64)
print("naive pool (paper)  :  mu=%.3f             tau=%.3f   <- OVERestimates tau" % (mu_naive, tau_naive))
print("   (naive tau ~ sqrt(tau^2+2*sigma^2) = %.3f: measurement noise enters TWICE, not deconvolved)" % math.sqrt(TAU_TRUE**2 + 2*SIGMA**2))
print("\nAGREEMENT (A vs B):  d_mu=%.4f   d_tau=%.4f   (should be ~0 -> reuse validated)"
      % (abs(muA.mean()-muB.mean()), abs(tauA.mean()-tauB.mean())))

try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(9, 4))
    ax[0].hist(muA, 60, density=True, alpha=.5, label="(A) full joint MCMC")
    ax[0].hist(muB, 60, density=True, alpha=.5, label="(B) posterior reuse")
    ax[0].axvline(MU_TRUE, color="k", ls="--"); ax[0].set_title(r"population mean $\mu$"); ax[0].legend(fontsize=8)
    ax[1].hist(tauA, 60, density=True, alpha=.5, label="(A) full joint MCMC")
    ax[1].hist(tauB, 60, density=True, alpha=.5, label="(B) posterior reuse")
    ax[1].axvline(TAU_TRUE, color="k", ls="--")
    ax[1].axvline(tau_naive, color="r", ls=":", label="naive pool (biased)")
    ax[1].set_title(r"population scatter $\tau$"); ax[1].legend(fontsize=8)
    fig.suptitle("HBI posterior reuse (B) matches full joint MCMC (A); naive pooling over-broadens $\\tau$")
    fig.tight_layout(); fig.savefig("/tmp/clsbi_hbi_compare.png", dpi=130)
    print("figure -> /tmp/clsbi_hbi_compare.png")
except Exception as e:
    print("(plot skipped: %s)" % e)
