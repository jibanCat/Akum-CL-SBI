"""
Single-page HTML pitch slide for cluster cosmologists.

- No Reveal.js: just a static HTML page laid out with CSS Grid + viewport units
  (vw/vh), so it ALWAYS fills the screen on any aspect ratio (16:9, 16:10, 4:3, ...)
- KaTeX (not MathJax) for equations: synchronous, no positioning glitches
- Content reframed for cluster cosmologists: the math + cosmology connection,
  not a tutorial walkthrough
"""
import base64, os

def b64(path): return base64.b64encode(open(path, "rb").read()).decode("ascii")

F = {
    "PIPELINE": b64("/tmp/pipeline_diagram.png"),
    "HBI_MC":   b64("/Users/jibanmac/Documents/GitHub/Akum-CL-SBI/hbi_verification/figures/hbi_mc_population.png"),
    "RICHNESS": b64("/Users/jibanmac/Documents/GitHub/Akum-CL-SBI/hbi_verification/figures/richness_mass_calibration.png"),
}

HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>HBI for cluster mass calibration via posterior reuse</title>
<meta name="viewport" content="width=device-width,initial-scale=1">

<!-- KaTeX (synchronous, reliable) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" crossorigin="anonymous">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" crossorigin="anonymous"
        onload="renderMathInElement(document.body, {delimiters:[
          {left:'$$',right:'$$',display:true},
          {left:'\\[',right:'\\]',display:true},
          {left:'$',right:'$',display:false},
          {left:'\\(',right:'\\)',display:false}
        ], throwOnError:false});"></script>

<style>
:root{
  --accent:#1f4e79; --accent2:#16864a; --accent3:#b22222; --soft:#f4f6fa;
  --ink:#1d2330; --muted:#5b6473; --line:#d8dde6;
}
*{box-sizing:border-box}
html,body{margin:0; padding:0; width:100vw; height:100vh; overflow:hidden;
  background:#fff; color:var(--ink);
  font-family:-apple-system,"Segoe UI","Helvetica Neue",Arial,sans-serif;}

/* One page laid out as a CSS grid that fills the entire viewport.
   Rows: header / hero / body / footer.  Heights are %s of vh => fits ANY aspect. */
.deck{
  width:100vw; height:100vh;
  display:grid;
  grid-template-rows: 8vh 22vh 1fr 7vh;
  gap: 0.8vh;
  padding: 1.5vh 1.6vw 0.8vh 1.6vw;
}

/* HEADER */
.head{display:flex; align-items:baseline; justify-content:space-between; gap:1.6vw;}
.head h1{font-size:clamp(18px, 2.2vw, 34px); color:var(--accent);
  margin:0; line-height:1.12; letter-spacing:-0.01em; font-weight:700;}
.head .sub{font-size:clamp(11px, 1.05vw, 16px); color:var(--muted);
  margin:0.2em 0 0 0; font-weight:500;}
.pill{display:inline-block; background:#e6efff; color:var(--accent);
  padding:.25em .75em; border-radius:99px;
  font-size:clamp(9px, 0.8vw, 12px); font-weight:600; letter-spacing:.04em;
  white-space:nowrap; align-self:flex-start;}

/* HERO BAND */
.hero{display:flex; align-items:center; justify-content:center;
  border:1px solid var(--line); border-radius:10px; padding:0.5vh 1vw; background:#fafbfd;}
.hero img{max-height:21vh; max-width:96vw; width:auto; object-fit:contain;}

/* BODY: 3 cards in a row */
.body3{display:grid; grid-template-columns: 1fr 1.15fr 1.05fr; gap:1.0vw; min-height:0;}
.card{background:var(--soft); border-radius:12px; padding:1.4vh 1.0vw;
  border-left:5px solid var(--accent); display:flex; flex-direction:column; min-height:0;
  box-shadow: 0 1px 2px rgba(0,0,0,.04);}
.card.green{border-left-color:var(--accent2);}
.card.red  {border-left-color:var(--accent3);}
.card h2{font-size:clamp(13px, 1.32vw, 19px); color:var(--accent);
  margin:0 0 .4em 0; line-height:1.15; font-weight:700; letter-spacing:-0.005em;}
.card p, .card li{font-size:clamp(10px, 0.92vw, 14px); line-height:1.4; margin:.35em 0;}
.card small{font-size:clamp(8.5px, 0.78vw, 12px); color:var(--muted);}
.card .eq{background:#fff; border:1px solid var(--line); border-radius:6px;
  padding:0.4vh 0.6vw; margin:.4em 0;}
.card .eq .katex{font-size:clamp(10px, 1.05vw, 16px) !important;}
.callout{display:inline-block; background:#ffe9a1; padding:1px 5px;
  border-radius:4px; font-weight:600;}
.card a{color:var(--accent); text-decoration:underline; text-decoration-thickness:1px;}
.card .grow{flex:1 1 auto; min-height:0; display:flex; align-items:center; justify-content:center; margin-top:.5em;}
.card .grow img{max-height:100%; max-width:100%; width:auto; border-radius:6px;
  box-shadow:0 1px 3px rgba(0,0,0,.10);}
.card .tag{font-size:clamp(9px, 0.78vw, 12px); color:var(--muted); margin-top:.4em;}
ul{margin:.3em 0 .3em 1.0em; padding:0;}
ul li{margin:.2em 0;}

/* FOOTER */
.foot{display:flex; align-items:center; justify-content:space-between; gap:1.6vw;
  color:var(--muted); font-size:clamp(9.5px, 0.88vw, 13px); padding-top:.4em;
  border-top:1px solid var(--line);}
.foot .refs a{color:var(--accent); margin-right:.7em; text-decoration:none;}
.foot .refs a:hover{text-decoration:underline;}
</style>
</head>
<body>

<div class="deck">

  <!-- HEADER -->
  <div class="head">
    <div>
      <h1>A population-inference framework on top of <span style="color:var(--accent2);">CL-SBI</span>: reusing per-cluster posteriors hierarchically</h1>
      <p class="sub">Follow-up to <i>Gill et al. (in prep.)</i> &mdash; their SBI pipeline produces per-cluster mass&ndash;concentration $(M_{200c},c_{200c})$ posteriors; we recycle those stored chains to infer population-level parameters $\Lambda$ <b>without re-fitting any cluster</b>, at a fraction of the cost of a full joint HBI.</p>
    </div>
    <span class="pill">project pitch &middot; Ming-Feng Ho</span>
  </div>

  <!-- HERO PIPELINE -->
  <div class="hero">
    <img src="data:image/png;base64,__PIPELINE__" alt="CL-SBI per-cluster posteriors -> hierarchical reuse -> scaling relation -> cosmology">
  </div>

  <!-- THREE CARDS -->
  <div class="body3">

    <!-- 1. THE STARTING POINT: WHAT AKUM'S PAPER GIVES US -->
    <div class="card">
      <h2>What <a href="https://github.com/LSSTDESC/CL-SBI">CL-SBI</a> already gives us</h2>
      <p><b>Gill et al. (in prep.)</b> validate SBI for per-cluster weak-lensing mass inference: train a
      neural posterior $p(M,c\!\mid\! d_j)$ once on simulated NFW shear profiles, then evaluate on
      observed clusters at $\gtrsim\!400\times$ MCMC speed. <b>Each fitted cluster ships with a stored
      posterior chain.</b></p>
      <p>Gill et&nbsp;al. flag population-level inference as the next step but leave the formalism open
      &mdash; <i>that's our entry point</i>.</p>
      <p><b>Our question:</b> can we build a <i>reuse framework</i> that combines these stored
      $\{M_j^{(s)}\}$ chains into population-level constraints, without re-running any per-cluster
      fit, and without paying the cost of a full joint $(\Lambda,\{M_j\})$ HBI?</p>
    </div>

    <!-- 2. THE PROPOSAL: recycle stored posteriors -->
    <div class="card green">
      <h2>Hierarchical reuse: cheaper than joint HBI</h2>
      <p>Population (hyper-)parameters $\Lambda=(A,B,\sigma_{\rm intr})$ &mdash; the parameters of a
      mass&ndash;observable relation $\langle\ln O\mid M\rangle = A + B\ln(M/M_{\rm piv})$ with intrinsic
      scatter $\sigma_{\rm intr}$. <b>Hyper-posterior</b>, marginalising each cluster's latent mass $M_j$:</p>
      <p style="font-size:0.92em;"><i>($d_j$ = WL shear profile of cluster $j$, the SBI summary; $O_j$ = a second observable per cluster &mdash; richness $\lambda_j$, or SZ $\xi_j$, $T_{X,j}$ &hellip;)</i></p>
      <div class="eq">$$p(\Lambda\mid \{d_j,O_j\})\;\propto\;\pi(\Lambda)\,\prod_j\!\int\! p(O_j\mid M_j,\Lambda)\,p(M_j\mid d_j)\,dM_j$$</div>
      <p><b>Recycling identity.</b> Stored chains $\{M_j^{(s)}\}$ were drawn under the SBI training prior
      $\pi_0(M)$ (flat in $\log M$ in Gill et&nbsp;al.); importance re-weighting (Thrane&nbsp;&amp;&nbsp;Talbot&nbsp;2019) gives</p>
      <div class="eq">$$\!\int\!\!\cdot\,dM\;\propto\;\tfrac1S\!\sum_s\!p(O_j\!\mid\!M_j^{(s)},\Lambda)\,\tfrac{p(M_j^{(s)}\mid\Lambda)}{\pi_0(M_j^{(s)})}$$</div>
      <p>When the population mass prior is taken to be the halo mass function, the importance weight
      $p(M\mid\Lambda)/\pi_0(M)\propto dn/dM$&nbsp;&mdash; cosmology enters the re-weighting, and Eddington
      bias is absorbed by construction. <b>Efficiency vs joint HBI:</b> joint samples $(2+N_c)$ dims
      every step; reuse samples just $\dim\Lambda\!\sim\!3$ &mdash; per-cluster work done <i>once, offline</i>.</p>
      <p class="tag">Selection enters as an extra $P(\text{detected}\mid M,O)$ factor inside the same product &mdash; deferred to the DESC Note.</p>
    </div>

    <!-- 3. FIRST USE CASE + SCIENCE EXTENSION -->
    <div class="card red">
      <h2>First use case &rarr; science extension</h2>
      <p><b>First demonstration</b> &mdash; the population $(M,c)$ of the calibration sample, from stored
      CL-SBI chains alone (no new observable):</p>
      <div class="grow">
        <img src="data:image/png;base64,__HBI_MC__" alt="HBI population (M,c) hyper-posterior from CL-SBI chains">
      </div>
      <p style="margin-top:0.4em;"><small><i>Left:</i> per-cluster CL-SBI posteriors. <i>Right:</i>
      hyper-posterior on the population mean $(\mu_M,\mu_c)$; recycle (blue) brackets the truth (&starf;),
      OLS on posterior means (red &times;) is biased.</small></p>
      <p style="margin-top:0.5em;"><b>Science extension</b> &mdash; add a second observable per cluster:</p>
      <ul style="margin-top:0.2em;">
        <li><b>Calibrate $P(\lambda\!\mid\!M)$</b> on DES&nbsp;Y1&nbsp;/&nbsp;LSST clusters from stored CL-SBI chains $+$ catalog richnesses
        <span style="display:inline-block; vertical-align:middle; margin:0 0.3em;">
          <img src="data:image/png;base64,__RICHNESS__" alt="richness-mass toy: naive OLS / flat / recycle+dn/dM" style="height:6vh; border-radius:4px; box-shadow:0 1px 2px rgba(0,0,0,.12); vertical-align:middle;">
        </span>
        (toy: recycle$+dn/dM$ recovers $B=1.00\pm0.10$, $\sigma_{\ln\lambda\mid M}=0.30\pm0.06$; naive OLS attenuates to $B=0.62$).</li>
        <li><b>Cluster-count likelihood</b> $\langle N(\lambda)\rangle=\!\int dM\,(dn/dM)\,P(\lambda\!\mid\!M)$ &rarr; $S_8\!\equiv\!\sigma_8(\Omega_m/0.3)^{1/2}$ &mdash; same hierarchical structure as <a href="https://arxiv.org/abs/2310.12213">Bocquet&nbsp;et&nbsp;al.&nbsp;2024</a>.</li>
        <li><b>Multi-observable</b> ($\lambda$ + SZ + $T_X$) as additional drop-in factors.</li>
      </ul>
    </div>

  </div>

  <!-- FOOTER -->
  <div class="foot">
    <div><b>Roadmap.</b> (i) validate reuse vs joint Bocquet-style MCMC on realistic NFW shear profiles using CL-SBI chains; (ii) DESC Note formalising the recycle layer; (iii) Aidan-led notebook tutorials; (iv) extend to multi-observable population inference.</div>
    <div class="refs">
      <a href="https://arxiv.org/abs/1809.02293">Thrane&amp;Talbot19</a>
      <a href="https://arxiv.org/abs/1809.02063">MandelFarrGair19</a>
      <a href="https://arxiv.org/abs/1707.01907">Murata18</a>
      <a href="https://arxiv.org/abs/1810.09456">Costanzi19</a>
      <a href="https://arxiv.org/abs/2310.12213">Bocquet24</a>
    </div>
  </div>

</div>
</body>
</html>
"""

for k, v in F.items():
    HTML = HTML.replace("__" + k + "__", v)

out = "/tmp/HBI_pitch_slide.html"
open(out, "w").write(HTML)
print(f"wrote {out}  ({os.path.getsize(out)/1024:.0f} KB, self-contained)")
