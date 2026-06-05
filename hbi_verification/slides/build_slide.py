"""
Build a self-contained Reveal.js pitch slide for the HBI cluster-mass project.
Layout uses a flex column so the slide always fits a 1280x720 (16:9) viewport
without clipping; hero band ~28% of height, body grid 1fr, footer pinned.
"""
import base64, os

def b64(path): return base64.b64encode(open(path, "rb").read()).decode("ascii")
F = {
    "PIPELINE":  b64("/tmp/pipeline_diagram.png"),
    "RICHNESS":  b64("/Users/jibanmac/Documents/GitHub/Akum-CL-SBI/hbi_verification/figures/richness_mass_calibration.png"),
    "WIDTH_NC":  b64("/Users/jibanmac/Documents/GitHub/Akum-CL-SBI/hbi_verification/figures/fig_width_vs_Nc.png"),
    "HBI_MT":    b64("/Users/jibanmac/Documents/GitHub/Akum-CL-SBI/hbi_verification/figures/fig_hbi_mu_tau.png"),
}

HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>HBI for Cluster Mass Calibration -- Pitch</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/white.css">
<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js"></script>
<style>
:root { --accent:#1f4e79; --accent2:#16864a; --accent3:#b22222; --soft:#f4f6fa; }
.reveal { font-family: -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif; }
.reveal section { text-align: left; }
.reveal h1, .reveal h2, .reveal h3 { text-transform: none; letter-spacing: -0.01em; color: var(--accent); }
.reveal h1 { font-size: 1.35em; margin: 0; }
.reveal h2 { font-size: 0.85em; margin: 0 0 .15em 0; }
.reveal h3 { font-size: 0.65em; color: #555; font-weight:500; margin: 0; }
.reveal p, .reveal li { font-size: 0.45em; line-height: 1.32; margin: .25em 0; }
.reveal small { font-size: 0.40em; color: #555; }
.reveal a { color: var(--accent); }

/* slide as flex column so everything sums to 100% height exactly */
.slide-flex { display:flex; flex-direction:column; height:100%; gap: 8px; }
.head  { flex: 0 0 auto; }
.hero  { flex: 0 0 26%; display:flex; align-items:center; justify-content:center; }
.hero img { max-height:100%; width:auto; max-width:100%; border-radius:6px; }
.body  { flex: 1 1 auto; min-height:0; }
.foot  { flex: 0 0 auto; }

.grid3 { display: grid; grid-template-columns: 1.05fr 1.20fr 1.40fr; gap: 12px; height:100%; }
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.card  { background: var(--soft); border-radius: 10px; padding: 8px 12px; border-left: 4px solid var(--accent);
         display:flex; flex-direction:column; min-height:0; }
.card.green { border-left-color: var(--accent2); }
.card.red   { border-left-color: var(--accent3); }
.card > * { flex: 0 0 auto; }
.card .grow { flex: 1 1 auto; min-height:0; display:flex; align-items:center; justify-content:center; }
.card .grow img { max-height:100%; max-width:100%; width:auto; border-radius:6px; box-shadow: 0 1px 3px rgba(0,0,0,.12); }

.eq { background: #fff; border: 1px solid #d8dde6; padding: 4px 6px; border-radius: 6px;
      font-size: 0.85em; }
.eq * { font-size: 0.85em; }
.callout { display:inline-block; background:#ffe9a1; padding:1px 5px; border-radius:4px; font-weight:600; }
.pill { display:inline-block; background:#e6efff; color:var(--accent); padding:1px 8px; border-radius:99px;
        font-size:0.42em; font-weight:600; letter-spacing:.04em; }
.tag { font-size:0.40em; color:#666; margin-top:.3em; }
.foot p { font-size: 0.40em; color:#444; margin: 0; }
</style>
</head>
<body>
<div class="reveal"><div class="slides">

<!-- ============================ SLIDE 1: THE PITCH ============================ -->
<section>
 <div class="slide-flex">

  <div class="head" style="display:flex; align-items:baseline; justify-content:space-between; gap:14px;">
    <div>
      <h1>Hierarchical Bayesian Inference for the Cluster Richness-Mass Relation</h1>
      <h3>Recycle each cluster's weak-lensing mass posterior to calibrate the MOR that feeds cluster cosmology</h3>
    </div>
    <span class="pill">project pitch &middot; Ming-Feng Ho</span>
  </div>

  <div class="hero">
    <img src="data:image/png;base64,__PIPELINE__" alt="pipeline: lambda observed -> M latent -> Lambda -> cosmology">
  </div>

  <div class="body">
    <div class="grid3">

      <div class="card">
        <h2>Why hierarchical?</h2>
        <p>Cluster cosmology turns counts into $\sigma_8, \Omega_m$ via the <b>mass-observable relation</b> (MOR):
           $\langle\ln\lambda\mid M\rangle = A + B\ln(M/M_{\rm piv})$ + intrinsic scatter $\sigma_{\ln\lambda\mid M}$.</p>
        <p>Fitting the MOR from noisy per-cluster WL masses with a flat prior is <b>Eddington-biased</b>
           (regression dilution).</p>
        <p>Honest answer: a <b>hyper-posterior</b> on $\Lambda=(A,B,\sigma)$ that marginalises each cluster's
           latent mass and folds in the halo mass function $dn/dM$ -- the carrier of cosmology.</p>
        <p class="tag">Refs: <a href="https://arxiv.org/abs/1707.01907">Murata18</a>,
           <a href="https://arxiv.org/abs/1810.09456">Costanzi19</a>,
           <a href="https://arxiv.org/abs/1812.01679">Bocquet19</a>/<a href="https://arxiv.org/abs/2310.12213">24</a></p>
      </div>

      <div class="card green">
        <h2>The recycling identity</h2>
        <p><small>Thrane &amp; Talbot 2019</small></p>
        <div class="eq">$$p(\Lambda\mid\{d_j,\lambda_j\})\;\propto\;\pi(\Lambda)\prod_j\!\int\!\! p(\lambda_j\mid M_j,\Lambda)\,p(M_j\mid d_j)\,dM_j$$</div>
        <p>Recycle stored per-cluster samples $M_j^{(s)}\!\sim\! p(M_j\mid d_j)$ from interim prior $\pi_0$:</p>
        <div class="eq">$$\int\!\cdots dM\,\approx\,\tfrac{\mathcal Z_j}{S}\!\sum_s p(\lambda_j\mid M_j^{(s)},\Lambda)\,\tfrac{p(M_j^{(s)})}{\pi_0(M_j^{(s)})}$$</div>
        <p>The weight <span class="callout">$p(M)/\pi_0 = dn/dM$</span> kills the Eddington bias -- and is
           where cosmology enters.</p>
        <p class="tag">No re-fitting of any cluster -- recycle Akum's stored SBI/MCMC posteriors.</p>
      </div>

      <div class="card red">
        <h2>Toy result (Tutorial 2)</h2>
        <div class="grow"><img src="data:image/png;base64,__RICHNESS__" alt="three attempts: naive, flat-recycle, recycle+mass function"></div>
        <p><b>Naive OLS</b> &amp; <b>flat-prior recycle</b>: slope attenuated $B\!\to\!0.62$ (Eddington).
           <b>Recycle + $dn/dM$</b>: recovers truth $B=1.00\!\pm\!0.10$, $\sigma_{\ln\lambda\mid M}=0.30\!\pm\!0.06$.</p>
      </div>

    </div>
  </div>

  <div class="foot">
    <p><span class="pill">deliverables</span>
       DESC Note on the formalism &middot; 2 student-facing tutorials with code &middot;
       joint MCMC vs reuse validation paper &middot; plugs into Akum's SBI/MCMC pipeline (LSSTDESC/CL-SBI).</p>
  </div>

 </div>
</section>

<!-- ============================ SLIDE 2: BACKUP ============================ -->
<section>
 <div class="slide-flex">
  <div class="head">
    <h1>Backup: stacking bug surfaced along the way</h1>
    <h3>The same hierarchical machinery flags a <span class="callout">$1/N_c$ over-broadening</span> in the paper's printed FtJ likelihood.</h3>
  </div>
  <div class="body">
    <div class="grid2" style="height:100%;">
      <div class="card">
        <h2>The diagnostic -- width vs $N_c$</h2>
        <div class="grow"><img src="data:image/png;base64,__WIDTH_NC__" alt="width vs Nc; FtJ flat, JtF tightens"></div>
        <p>JtF and the correct joint both shrink as $1/\sqrt{N_c}$; the printed FtJ is <b>flat in $N_c$</b>
           -- single-cluster width forever. At the paper's $N_c=376$ this is $\sim 19\times$ too wide.</p>
      </div>
      <div class="card green">
        <h2>Hyper-posterior recovers the truth</h2>
        <div class="grow"><img src="data:image/png;base64,__HBI_MT__" alt="mu, tau hyper-posterior"></div>
        <p>Posterior reuse $\Lambda=(\mu,\tau)$ matches the <i>exact</i> analytic hyper-posterior;
           naive pooling over-broadens $\tau$ as $\sqrt{\tau^2+2\sigma^2}$.</p>
      </div>
    </div>
  </div>
  <div class="foot"><p>Fix is one character (drop $1/N_c$); filed as a $\backslash$mfhocommet note next to the equation.
                     <i>Appendix only -- the project pitch is the slide before.</i></p></div>
 </div>
</section>

</div></div>

<script>
Reveal.initialize({
  hash: true, slideNumber: 'c/t', controls: true, progress: true,
  width: 1280, height: 720, margin: 0.02, minScale: 0.2, maxScale: 2.0,
  transition: 'fade'
});
</script>
</body>
</html>
"""

for k, v in F.items():
    HTML = HTML.replace("__" + k + "__", v)

out = "/tmp/HBI_pitch_slide.html"
open(out, "w").write(HTML)
print(f"wrote {out}  ({os.path.getsize(out)/1024:.0f} KB, self-contained)")
