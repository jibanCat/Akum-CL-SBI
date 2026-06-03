"""
#1  Confirm the FTJ vs JTF gap on the REAL colossus NFW forward model.
Same comparison as the toy, but forward = repo's simulate_nfw (colossus NFW).
We work in log10(density) space (well-conditioned; matches the paper's dex noise)
and use the repo's exact stacking structure: JTF = fit the MEAN profile,
FTJ = vstack per-cluster chains. Reference: TRUE joint (sum, proper sigma) and
PAPER FTJ (1/N_c-averaged) to re-confirm the sqrt(N_c) inflation on real NFW.
"""
import numpy as np, emcee
from colossus.cosmology import cosmology
from colossus.halo import profile_nfw
cosmology.setCosmology('planck18')                    # repo simulations/__init__.py:3
np.random.seed(2807)

RBINS = 10**np.arange(0, 3, 0.1)                       # 30 bins, as in repo
def simulate_nfw(log10mass, concentration):           # repo wlprofile.simulate_nfw (kind='density')
    nfw = profile_nfw.NFWProfile(M=10**log10mass, c=concentration, z=0.0, mdef='vir')
    return nfw.density(RBINS)
def fwd(theta):                                        # log10 profile (well-conditioned data vector)
    return np.log10(simulate_nfw(theta[0], theta[1]))

def loglike_unit(p, model):                            # repo mcmcutils.loglike form (unit variance)
    lm, c = p
    error = np.std(lm**2) + np.std(c)**2               # == 0
    return -0.5*np.sum((fwd(p)-model)**2/np.exp(2*error) + 2*error)
def loglike_proper(p, model, s):
    return -0.5*np.sum((fwd(p)-model)**2/s**2)
def inb(p): return (10 < p[0] < 18) and (0.5 < p[1] < 30)

def run(logp, starts=np.array([14.2, 5.0]), nb=200, ns=700):
    s = emcee.EnsembleSampler(100, 2, logp)
    p0 = starts + np.array([0.05, 0.3])*np.random.randn(100, 2)
    pos, _, _ = s.run_mcmc(p0, nb, progress=False); s.reset()
    s.run_mcmc(pos, ns, progress=False)
    return s.flatchain

# population of clusters + noisy log10 profiles (0.3 dex Gaussian == 0.3 dex lognormal)
N_C, SIG = 8, 0.3
m_true = 14.2 + 0.08*np.random.randn(N_C)
c_true = 5.0 + 0.5*np.random.randn(N_C)
clean = np.array([fwd([m_true[j], c_true[j]]) for j in range(N_C)])
data = clean + SIG*np.random.randn(N_C, len(RBINS))

print("running code JTF (mean profile, unit-var) ...")
chain_jtf  = run(lambda p: loglike_unit(p, data.mean(axis=0)) if inb(p) else -np.inf)
print("running code FTJ (vstack of %d per-cluster fits) ..." % N_C)
chain_ftj  = np.vstack([run(lambda p, d=d: loglike_unit(p, d) if inb(p) else -np.inf) for d in data])
print("running TRUE joint (sum, proper sigma) ...")
chain_jnt  = run(lambda p: (sum(loglike_proper(p, d, SIG) for d in data) if inb(p) else -np.inf))
print("running PAPER FTJ (1/N_c avg, proper sigma) ...")
chain_pap  = run(lambda p: ((1.0/N_C)*sum(loglike_proper(p, d, SIG) for d in data) if inb(p) else -np.inf))

def s2(c): return np.std(c[:, 0]), np.std(c[:, 1])
print("\n=== REAL NFW forward model | N_c=%d | 0.3 dex noise ===" % N_C)
for name, c in [("code JTF  (mean, unit-var)", chain_jtf), ("code FTJ  (vstack)", chain_ftj),
                ("PAPER FTJ (1/Nc, proper) ", chain_pap), ("TRUE joint (sum, proper) ", chain_jnt)]:
    a, b = s2(c); print("  %-26s  std(log10M)=%.4f  std(c)=%.4f" % (name, a, b))
print("  %-26s  std(log10M)=%.4f  std(c)=%.4f  (true population spread)" % ("population", np.std(m_true), np.std(c_true)))
fj, jt, tj, pf = s2(chain_ftj)[0], s2(chain_jtf)[0], s2(chain_jnt)[0], s2(chain_pap)[0]
print("\nRATIOS (log10M):  code FTJ / code JTF = %.2f   |   PAPER FTJ / TRUE joint = %.2f  (sqrt(N_c)=%.2f)"
      % (fj/jt, pf/tj, np.sqrt(N_C)))
