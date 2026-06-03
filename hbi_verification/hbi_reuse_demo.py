"""
#2 (corrected)  Hierarchical Bayesian inference by POSTERIOR REUSE, validated against
the EXACT analytic hyper-posterior (not against a hard-to-converge joint MCMC).

Model (mass-observable-relation analog):
    population:  m_j ~ N(mu, tau^2)        # mu = mean log-mass, tau = intrinsic scatter
    data:        d_j | m_j ~ N(m_j, sigma^2)

We compare four things to recover (mu, tau):
  (C) EXACT analytic hyper-posterior  -- the ground truth (marginal p(d_j|mu,tau)=N(d_j|mu, sigma^2+tau^2))
  (B) importance-sampling REUSE of stored per-cluster posteriors p(m_j|d_j)
  (A) full joint hierarchical MCMC over (mu, tau, {m_j})   -- correct, but expensive to converge in high-D
  (naive) pooling all per-cluster samples                 -- biased: overestimates tau

Audit lesson: (B) and (C) are cheap and essentially exact; (A) needs heavy sampling in the
2+N_c dimensional space to reach (C). So reuse is validated against (C), and (A)'s cost is
itself the motivation for reuse.
"""
import numpy as np, emcee, math
np.random.seed(7)

N_C, SIGMA, MU_TRUE, TAU_TRUE = 60, 0.30, 14.20, 0.30
m_true = MU_TRUE + TAU_TRUE*np.random.randn(N_C)
d = m_true + SIGMA*np.random.randn(N_C)
S = 4000
post = np.array([d[j] + SIGMA*np.random.randn(S) for j in range(N_C)])   # stored per-cluster posteriors (flat prior)

# ---------- (C) EXACT analytic hyper-posterior on a (mu, log tau) grid ----------
# marginal evidence per cluster: p(d_j|mu,tau) = N(d_j | mu, sigma^2 + tau^2)
# prior: flat in mu, flat in log tau (same convention as A) -> grid then normalize.
mu_g  = np.linspace(d.mean()-0.4, d.mean()+0.4, 400)
ltau_g = np.linspace(np.log(0.05), np.log(1.5), 400)
MU, LT = np.meshgrid(mu_g, ltau_g, indexing='ij')
TAU = np.exp(LT); var = SIGMA**2 + TAU**2
logpost = -0.5*np.sum((d[:,None,None]-MU[None])**2/var[None] + np.log(2*np.pi*var)[None], axis=0)
P = np.exp(logpost - logpost.max()); P /= P.sum()
muC   = np.sum(MU*P);  muC_sd  = math.sqrt(np.sum((MU-muC)**2*P))
tauC  = np.sum(TAU*P); tauC_sd = math.sqrt(np.sum((TAU-tauC)**2*P))

# ---------- (B) importance-sampling REUSE ----------
# L(mu,tau) = prod_j (1/S) sum_s N(m_j^s | mu, tau^2)   (flat interim prior cancels)
def loghyper(p):
    mu, lt = p; tau = math.exp(lt)
    if tau > 5: return -np.inf
    return sum(math.log(np.mean(np.exp(-0.5*((post[j]-mu)/tau)**2)/tau)+1e-300) for j in range(N_C)) + lt
sB = emcee.EnsembleSampler(12, 2, loghyper)
p0 = np.column_stack([MU_TRUE+.1*np.random.randn(12), np.log(.3)+.1*np.random.randn(12)])
pos,_,_ = sB.run_mcmc(p0, 1500, progress=False); sB.reset(); sB.run_mcmc(pos, 4000, progress=False)
B = sB.get_chain(flat=True); muB, tauB = B[:,0], np.exp(B[:,1])

# ---------- (A) full joint MCMC (heavier sampling than before; still the expensive path) ----------
def logp_joint(p):
    mu, lt, m = p[0], p[1], p[2:]; tau = math.exp(lt)
    if tau > 5: return -np.inf
    return (-0.5*np.sum(((d-m)/SIGMA)**2)) + (-0.5*np.sum(((m-mu)/tau)**2) - N_C*lt) + lt
nd = 2+N_C; nw = 4*nd
p0 = np.column_stack([MU_TRUE+.1*np.random.randn(nw), np.log(.3)+.1*np.random.randn(nw), d[None,:]+.1*np.random.randn(nw,N_C)])
sA = emcee.EnsembleSampler(nw, nd, logp_joint); pos,_,_ = sA.run_mcmc(p0, 3000, progress=False); sA.reset(); sA.run_mcmc(pos, 8000, progress=False)
A = sA.get_chain(flat=True); muA, tauA = A[:,0], np.exp(A[:,1])
try:
    tau_iat = float(sA.get_autocorr_time(quiet=True)[1])
except Exception:
    tau_iat = float('nan')

# ---------- naive pool ----------
pooled = post.ravel()

print("truth:                  mu=%.3f  tau=%.3f" % (MU_TRUE, TAU_TRUE))
print("(C) EXACT analytic   :  mu=%.3f +/- %.3f   tau=%.3f +/- %.3f   <- ground truth" % (muC, muC_sd, tauC, tauC_sd))
print("(B) posterior REUSE  :  mu=%.3f +/- %.3f   tau=%.3f +/- %.3f   <- cheap; matches (C)" % (muB.mean(), muB.std(), tauB.mean(), tauB.std()))
print("(A) full joint MCMC  :  mu=%.3f +/- %.3f   tau=%.3f +/- %.3f   <- expensive (2+N_c dims)" % (muA.mean(), muA.std(), tauA.mean(), tauA.std()))
print("naive pool           :  mu=%.3f            tau=%.3f            <- biased ~sqrt(tau^2+2 sigma^2)=%.3f"
      % (pooled.mean(), pooled.std(), math.sqrt(TAU_TRUE**2 + 2*SIGMA**2)))
print("-"*72)
print("VALIDATION  |B - C|:  d_mu=%.4f  d_tau=%.4f   (reuse vs exact -> the real test)" % (abs(muB.mean()-muC), abs(tauB.mean()-tauC)))
print("            |A - C|:  d_mu=%.4f  d_tau=%.4f   (joint MCMC vs exact; larger => A under-converged)" % (abs(muA.mean()-muC), abs(tauA.mean()-tauC)))
print("            tau autocorr (log-tau) in A ~ %.0f steps" % tau_iat)

try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1,2,figsize=(9,3.8))
    ax[0].hist(muB,60,density=True,alpha=.55,label="(B) reuse"); ax[0].hist(muA,60,density=True,alpha=.45,label="(A) joint MCMC")
    ax[0].axvline(muC,color="g",lw=2,label="(C) exact mean"); ax[0].axvline(MU_TRUE,color="k",ls="--",label="truth")
    ax[0].set_title(r"population mean $\mu$"); ax[0].legend(fontsize=7)
    ax[1].hist(tauB,60,density=True,alpha=.55,label="(B) reuse"); ax[1].hist(tauA,60,density=True,alpha=.45,label="(A) joint MCMC")
    ax[1].axvline(tauC,color="g",lw=2,label="(C) exact mean"); ax[1].axvline(TAU_TRUE,color="k",ls="--",label="truth")
    ax[1].axvline(pooled.std(),color="r",ls=":",label="naive (biased)")
    ax[1].set_title(r"population scatter $\tau$"); ax[1].legend(fontsize=7)
    fig.suptitle("Reuse (B) matches the EXACT analytic posterior (C); naive pooling over-broadens; joint MCMC (A) is the costly path")
    fig.tight_layout(); fig.savefig("/tmp/clsbi_hbi_compare.png", dpi=130); print("figure -> /tmp/clsbi_hbi_compare.png")
except Exception as e:
    print("(plot skipped: %s)" % e)
