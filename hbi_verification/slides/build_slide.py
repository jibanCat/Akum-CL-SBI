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
.body3{display:grid; grid-template-columns: 0.95fr 1.20fr 1.55fr; gap:1.0vw; min-height:0;}
.card{background:var(--soft); border-radius:12px; padding:1.4vh 1.0vw;
  border-left:5px solid var(--accent); display:flex; flex-direction:column; min-height:0;
  box-shadow: 0 1px 2px rgba(0,0,0,.04);}
.card.green{border-left-color:var(--accent2);}
.card.red  {border-left-color:var(--accent3);}
.card h2{font-size:clamp(13px, 1.32vw, 19px); color:var(--accent);
  margin:0 0 .4em 0; line-height:1.15; font-weight:700; letter-spacing:-0.005em;}
.card p, .card li{font-size:clamp(11.5px, 1.05vw, 16px); line-height:1.4; margin:.4em 0;}
.card small{font-size:clamp(8.5px, 0.78vw, 12px); color:var(--muted);}
.card .eq{background:#fff; border:1px solid var(--line); border-radius:6px;
  padding:0.4vh 0.6vw; margin:.4em 0;}
.card .eq .katex{font-size:clamp(10px, 1.05vw, 16px) !important;}
.callout{display:inline-block; background:#ffe9a1; padding:1px 5px;
  border-radius:4px; font-weight:600;}
.card a{color:var(--accent); text-decoration:underline; text-decoration-thickness:1px;}
.card .grow{flex:1 1 auto; min-height:0; display:flex; align-items:center; justify-content:center; margin-top:.5em;}
.card .grow img{max-height:100%; max-width:100%; width:auto; height:auto; object-fit:contain; border-radius:6px;
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
      <h1>A population-inference layer on top of <span style="color:var(--accent2);">CL-SBI</span>: reuse per-cluster posteriors hierarchically</h1>
      <p class="sub">Follow-up to <i>Gill et&nbsp;al. (in&nbsp;prep.)</i> &mdash; recycle &#x267B;&#xFE0F; stored $\{\theta_j^{(s)}\}$ chains into a population hyper-posterior on $\Lambda$, without re-fitting any cluster.</p>
    </div>
    <div style="text-align:right; line-height:1.3;">
      <span class="pill">project pitch &middot; Ming-Feng Ho</span><br>
      <span style="font-size:clamp(8.5px, 0.7vw, 11.5px); color:var(--muted); font-style:italic;">student: Aidan Behmer &nbsp;&middot;&nbsp; PI: Camille Avestruz &nbsp;(U.&nbsp;Michigan)</span>
    </div>
  </div>

  <!-- HERO PIPELINE -->
  <div class="hero">
    <img src="data:image/png;base64,__PIPELINE__" alt="CL-SBI per-cluster posteriors -> hierarchical reuse -> scaling relation -> cosmology">
  </div>

  <!-- THREE CARDS -->
  <div class="body3">

    <!-- 1. THE PROBLEM -->
    <div class="card">
      <h2>The problem</h2>
      <p><b>Gill et al. (in prep.)</b>: <a href="https://github.com/LSSTDESC/CL-SBI">CL-SBI</a> trains SBI on NFW profiles &rarr; per-cluster $(M,c)$ posterior chains $\theta_j^{(s)}$.</p>
      <ol style="margin:.4em 0 0 1.2em; padding:0;">
        <li>How do we do <b>population-level inference</b> on top of these per-cluster SBI posteriors?</li>
        <li>Re-doing joint-SBI or joint MCMC on the whole sample is <b>computationally wasteful</b>.</li>
        <li>Memory footprint <b>scales fast with $N_c$</b> &mdash; the sampler space is $\dim\Lambda + 2N_c$.</li>
      </ol>
    </div>

    <!-- 2. THE FRAMEWORK -->
    <div class="card green">
      <h2>Obvious solution: recycle &#x267B;&#xFE0F; the per-cluster posteriors</h2>
      <p>Hyper-posterior on population parameters $\Lambda$, marginalising each $\theta_j$:</p>
      <div class="eq">$$p(\Lambda\mid \mathrm{data})\;\propto\;\pi(\Lambda)\,\prod_j\!\int\! p(d_j\mid\theta_j)\,p(\theta_j\mid\Lambda)\,d\theta_j$$</div>
      <p>The integral is expensive&mdash;<i>unless</i> we already have stored chains $\theta_j^{(s)}$ under prior $\pi_0$. Reuse them by importance re-weighting (Thrane&nbsp;&amp;&nbsp;Talbot&nbsp;2019):</p>
      <div class="eq">$$p(\Lambda\mid \mathrm{data})\;\propto\;\pi(\Lambda)\,\prod_j\,\tfrac1S\!\sum_s\!\tfrac{p(\theta_j^{(s)}\mid\Lambda)}{\pi_0(\theta_j^{(s)})}$$</div>
      <div class="eq" style="margin-top:0.5em; background:#fff7d6; border-color:#e0c068; line-height:1.55;">
        <b>Bonus &mdash; bridge to richness&ndash;mass.</b>
        Add observed $\lambda_j$; promote $\Lambda\!\to\!(A,B,\sigma_{\ln\lambda\mid M})$ + cosmology:<br>
        $\;p(\Lambda\!\mid\!\mathrm{data})\,\propto\,\pi(\Lambda)\,\prod_j\,\tfrac1S\!\sum_s\!\tfrac{\mathcal N(\ln\lambda_j;\,A+B\ln M_j^{(s)},\,\sigma^2)\,\cdot\,\boxed{n_{\rm HMF}(M_j^{(s)};\,\Omega_m,\sigma_8)}}{\pi_0(M_j^{(s)})}$<br>
        The boxed halo mass function carries cosmology &mdash; <i>this is how $S_8$ enters</i>.
      </div>
    </div>

    <!-- 3. FIRST USE CASE -->
    <div class="card red">
      <h2>First use case: the $(M,c)$ population</h2>
      <div class="grow">
        <img src="data:image/png;base64,__HBI_MC__" alt="inferred population (M,c) distribution: recycle matches truth; naive stacking too wide">
      </div>
      <div class="eq" style="margin-top:0.5em; line-height:1.55;">
        <span style="color:var(--accent3);"><b>naive&nbsp;stack</b></span> &mdash; pool all per-cluster samples:<br>
        $\widehat{\rm Var} = \tau^2 + 2\sigma_{\rm post}^2$ <i>(biased)</i><br>
        <span style="color:var(--accent2);"><b>HBI recycle &#x267B;&#xFE0F;</b></span> &mdash; hierarchical likelihood:<br>
        $\widehat{\rm Var} = \tau^2$ <i>(deconvolves to truth)</i>
      </div>
    </div>

  </div>

  <!-- SPEAKER NOTES (collapsible, hidden by default; for the presenter) -->
  <details style="position:fixed; right:1.5vw; bottom:9vh; max-width:36vw; font-size:0.42em; line-height:1.5; background:#fffbe6; border:1px solid #e0c068; border-radius:8px; padding:0.6em 0.9em; box-shadow:0 2px 6px rgba(0,0,0,.10); z-index:50;">
    <summary style="cursor:pointer; font-weight:600; color:#8a6c10;">&#x1F4DD; speaker notes (click to toggle)</summary>
    <ul style="margin:.4em 0 0 .9em; padding:0; color:#4a3d10;">
      <li><b>400&times; speed</b>: Gill+ fig.&nbsp;13.</li>
      <li><b>Joint HBI dim</b>: $\dim\Lambda + 2N_c$ &mdash; two latents per cluster.</li>
      <li><b>Mass def</b>: Akum stores $M_{\rm vir}$&nbsp;[$h^{-1}M_\odot$]; convert to $M_{200{\rm m}}$ at the population layer to use Tinker08 HMF and DES/SPT MOR fits.</li>
      <li><b>Selection</b>: assume known $\Theta(\lambda \in {\rm bin})$. Full selection-function inference (Costanzi19, Bocquet24) is a drop-in extension.</li>
      <li><b>Toy regime</b>: $z\!=\!0.3$, $\mu_M\!=\!14.30$, $\mu_c\!=\!5$, $\rho_{Mc}\!=\!-0.3$ (Bhattacharya13, Diemer&ndash;Kravtsov15). $\tau_M\!=\!0.25\,$dex chosen for figure legibility &mdash; realistic intrinsic spread in a $30\!&lt;\!\lambda\!&lt;\!45$ bin is $\sim\!0.10$&ndash;$0.15\,$dex.</li>
      <li><b>$\sigma_{\rm post}$</b>: mean per-cluster posterior $1\sigma$ width (Gaussian, well-calibrated). Factor 2 in $\tau^2+2\sigma_{\rm post}^2$ = (within-cluster width)$^2$ + (variance of posterior centers around truth).</li>
      <li><b>$\pi_0$ stability</b>: Akum's training prior is BoxUniform in $\log_{10}M\!\in\![12,17]$, so the HMF weight $n_{\rm HMF}(M)/\pi_0$ is well-behaved at $\log_{10}M\!\sim\!14$ (effective sample size $\gtrsim\!0.5S$). Monitor ESS.</li>
    </ul>
  </details>

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
