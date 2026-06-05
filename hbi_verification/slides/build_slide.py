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
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/white.css">
<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js"></script>
<style>
:root { --accent:#1f4e79; --accent2:#16864a; --accent3:#b22222; --soft:#f4f6fa; }
.reveal { font-family: -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif; }
.reveal section { text-align: left; }
.reveal h1, .reveal h2, .reveal h3 { text-transform: none; letter-spacing: -0.01em; color: var(--accent); }
.reveal h1 { font-size: 1.5em; margin: 0 0 .25em 0; }
.reveal h2 { font-size: 1.1em; margin: 0 0 .25em 0; }
.reveal h3 { font-size: .95em; color: #333; }
.reveal p, .reveal li { font-size: 0.6em; line-height: 1.4; }
.reveal small { font-size: 0.52em; color: #555; }
.reveal sup a, .reveal a { color: var(--accent); }
.grid3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; }
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.card { background: var(--soft); border-radius: 10px; padding: 10px 14px; border-left: 4px solid var(--accent); }
.card.green { border-left-color: var(--accent2); }
.card.red   { border-left-color: var(--accent3); }
.eq { background: #fff; border: 1px solid #d8dde6; padding: 6px 8px; border-radius: 6px; }
.callout { display:inline-block; background:#ffe9a1; padding:2px 6px; border-radius:4px; font-weight:600; }
.pill { display:inline-block; background:#e6efff; color:var(--accent); padding:1px 8px; border-radius:99px; font-size:0.55em; font-weight:600; letter-spacing:.04em; }
.footer { position: fixed; right: 16px; bottom: 10px; font-size: 0.45em; color: #777; }
img.tile { width:100%; border-radius:6px; box-shadow: 0 1px 3px rgba(0,0,0,.12); }
.hero { width:100%; border-radius:8px; }
.tag { font-size:0.55em; color:#666; }
ul { margin: .2em 0 .2em 1.1em; padding: 0; }
</style>
</head>
<body>
<div class="reveal"><div class="slides">

<!-- ============================ SLIDE 1: THE PITCH ============================ -->
<section>
  <div style="display:flex; align-items:baseline; justify-content:space-between;">
    <h1>Hierarchical Bayesian Inference for the Cluster&nbsp;Richness-Mass Relation</h1>
    <span class="pill">project pitch &middot; Ming-Feng Ho</span>
  </div>
  <h3 style="margin-top:-4px; color:#555;">Recycle each cluster's weak-lensing mass posterior to calibrate the mass-observable relation that feeds cluster cosmology</h3>

  <!-- pipeline / direction-of-inference diagram -->
  <img class="hero" src="data:image/png;base64,__PIPELINE__" style="margin: 6px 0 10px 0; max-height:160px; object-fit:contain;">

  <!-- 3-column body -->
  <div class="grid3" style="margin-top:4px;">

    <!-- COL 1 : WHY -->
    <div class="card">
      <h2>Why hierarchical?</h2>
      <p>Cluster cosmology lives or dies by the <b>mass-observable relation</b> (MOR):
      $$\langle\ln\lambda\mid M\rangle = A + B\ln(M/M_{\rm piv}),\;\;\sigma_{\ln\lambda\mid M}$$
      </p>
      <p>Fitting it from noisy per-cluster WL masses with a flat prior produces a <b>Eddington-biased</b> slope (regression dilution).</p>
      <p>The honest answer is a <b>hyper-posterior</b> on $\Lambda=(A,B,\sigma)$ that marginalises each cluster's latent mass &mdash; and folds in the <b>halo mass function</b> $dn/dM$ (the carrier of $\sigma_8$, $\Omega_m$, $S_8$).</p>
      <p class="tag">Refs: <a href="https://arxiv.org/abs/1707.01907">Murata 2018</a>, <a href="https://arxiv.org/abs/1810.09456">Costanzi 2019</a>, <a href="https://arxiv.org/abs/1812.01679">Bocquet 2019</a> / <a href="https://arxiv.org/abs/2310.12213">2024</a></p>
    </div>

    <!-- COL 2 : METHOD -->
    <div class="card green">
      <h2>The recycling identity</h2>
      <p>Hyper-posterior <small>(Thrane &amp; Talbot 2019)</small>:</p>
      <div class="eq">$$p(\Lambda\mid\{d_j,\lambda_j\})\;\propto\;\pi(\Lambda)\prod_j\!\int\! p(\lambda_j\mid M_j,\Lambda)\,p(M_j\mid d_j)\,dM_j$$</div>
      <p>With stored per-cluster posterior samples $M_j^{(s)}\sim p(M_j\mid d_j)$ under interim prior $\pi_0$:</p>
      <div class="eq">$$\int\cdots dM\approx\frac{\mathcal Z_j}{S}\sum_s p(\lambda_j\mid M_j^{(s)},\Lambda)\,\frac{p(M_j^{(s)})}{\pi_0(M_j^{(s)})}$$</div>
      <p>The weight <span class="callout">$p(M)/\pi_0$ = halo mass function</span> is what kills the Eddington bias &mdash; and is where cosmology enters.</p>
      <p class="tag">No re-fitting of any cluster &mdash; recycle Akum's stored SBI/MCMC posteriors.</p>
    </div>

    <!-- COL 3 : RESULT -->
    <div class="card red">
      <h2>Toy result (Tutorial 2)</h2>
      <p>Recover the true $(A,B,\sigma_{\ln\lambda|M})$ from a 3-richness-bin sample by recycling:</p>
      <img class="tile" src="data:image/png;base64,__RICHNESS__" alt="richness-mass calibration toy result">
      <p style="margin-top:6px;"><b>Naive OLS</b> / <b>flat-prior recycle</b>: slope attenuated $B\!\to\!0.62$ (Eddington). <b>Recycle + mass function</b>: recovers truth $B=1.00\pm0.10$, $\sigma_{\ln\lambda|M}=0.30\pm0.06$.</p>
    </div>
  </div>

  <p style="margin-top:8px; font-size:0.55em; color:#444;">
    <span class="pill">deliverables</span>
    DESC Note on the formalism &middot; 2 student-facing tutorials with code &middot;
    seed for joint MCMC vs reuse validation paper &middot; plugs directly into Akum's SBI / MCMC pipeline (LSSTDESC/CL-SBI).
  </p>
  <div class="footer">HTML deck (single file) &mdash; open in any browser &middot; arrow keys to navigate &middot; <code>?</code> for shortcuts</div>
</section>

<!-- ============================ SLIDE 2: BONUS / BACKUP ============================ -->
<section>
  <h1>Backup: stacking bug surfaced along the way</h1>
  <p>The same hierarchical machinery flags a <span class="callout">$1/N_c$ over-broadening</span> in the paper's printed fit-then-join (FtJ) likelihood.</p>
  <div class="grid2">
    <div>
      <h2>The diagnostic &mdash; width vs $N_c$</h2>
      <img class="tile" src="data:image/png;base64,__WIDTH_NC__" alt="width vs Nc; FtJ flat, JtF tightens">
      <p style="font-size:0.55em;">JtF and the correct joint both shrink as $1/\sqrt{N_c}$; the printed FtJ is <b>flat in $N_c$</b> &mdash; single-cluster width forever. At the paper's $N_c=376$ this is $\sim 19\times$ too wide.</p>
    </div>
    <div>
      <h2>Hyper-posterior recovers the truth</h2>
      <img class="tile" src="data:image/png;base64,__HBI_MT__" alt="mu, tau hyper-posterior">
      <p style="font-size:0.55em;">Posterior reuse $\Lambda=(\mu,\tau)$ matches the <i>exact</i> analytic hyper-posterior; naive pooling over-broadens $\tau$ as $\sqrt{\tau^2+2\sigma^2}$.</p>
    </div>
  </div>
  <p style="margin-top:8px; font-size:0.55em;">Fix is one character (drop $1/N_c$); already filed as a $\backslash$mfhocommet note next to the equation. <i>This is an appendix &mdash; the project pitch is the slide before.</i></p>
</section>

</div></div>

<script>
Reveal.initialize({
  hash: true, slideNumber: 'c/t', controls: true, progress: true,
  width: 1280, height: 720, margin: 0.04, transition: 'fade'
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
