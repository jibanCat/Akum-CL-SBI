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
.card p, .card li{font-size:clamp(10px, 0.92vw, 14px); line-height:1.4; margin:.35em 0;}
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
      <p class="sub">Follow-up to <i>Gill et&nbsp;al. (in&nbsp;prep.)</i> &mdash; recycle stored $\{\theta_j^{(s)}\}$ chains into a population hyper-posterior on $\Lambda$, without re-fitting any cluster.</p>
    </div>
    <span class="pill">project pitch &middot; Ming-Feng Ho</span>
  </div>

  <!-- HERO PIPELINE -->
  <div class="hero">
    <img src="data:image/png;base64,__PIPELINE__" alt="CL-SBI per-cluster posteriors -> hierarchical reuse -> scaling relation -> cosmology">
  </div>

  <!-- THREE CARDS -->
  <div class="body3">

    <!-- 1. WHAT CL-SBI GIVES US -->
    <div class="card">
      <h2>What <a href="https://github.com/LSSTDESC/CL-SBI">CL-SBI</a> gives us</h2>
      <p><b>Gill et al. (in prep.)</b> train an SBI emulator on NFW shear profiles &rarr; per-cluster
      $(M,c)$ posterior chains $\theta_j^{(s)}\!\sim\!p(\theta_j\!\mid\!d_j)$, at $\gtrsim\!400\times$ MCMC speed.</p>
      <p>The chains are <b>already produced and stored</b>. Gill et&nbsp;al. flag population-level
      inference as the next step but leave the formalism open.</p>
      <p><b>Our question:</b> can we combine $\{\theta_j^{(s)}\}_j$ into population constraints
      <i>without re-fitting any cluster</i>, and without the cost of a joint $(\Lambda,\{\theta_j\})$&nbsp;HBI?</p>
    </div>

    <!-- 2. THE FRAMEWORK -->
    <div class="card green">
      <h2>The recycle framework</h2>
      <p>Population hyper-parameters $\Lambda$. <b>Hyper-posterior</b> marginalising each cluster's
      latent $\theta_j$:</p>
      <div class="eq">$$p(\Lambda\mid \mathrm{data})\;\propto\;\pi(\Lambda)\,\prod_j\!\int\! p(d_j\mid\theta_j)\,p(\theta_j\mid\Lambda)\,d\theta_j$$</div>
      <p>The integral is expensive&mdash;<i>unless</i> we already have stored chains $\theta_j^{(s)}\!\sim\!p(\theta_j\!\mid\!d_j)$ from some prior $\pi_0$. <b>Recycle them</b> by importance re-weighting (Thrane&nbsp;&amp;&nbsp;Talbot&nbsp;2019):</p>
      <div class="eq">$$p(\Lambda\mid \mathrm{data})\;\propto\;\pi(\Lambda)\,\prod_j\,\tfrac1S\!\sum_s\!\tfrac{p(\theta_j^{(s)}\mid\Lambda)}{\pi_0(\theta_j^{(s)})}$$</div>
      <p><b>Joint HBI</b> samples $(\Lambda,\{\theta_j\})$ &rarr; $\dim=\dim\Lambda+N_c$ at every step.
      <b>Recycle</b> samples $\Lambda$ only &mdash; per-cluster work done <i>once, offline</i>, by CL-SBI.</p>
    </div>

    <!-- 3. FIRST USE CASE -->
    <div class="card red">
      <h2>First use case: population $(M,c)$ recovery</h2>
      <div class="grow">
        <img src="data:image/png;base64,__HBI_MC__" alt="inferred population (M,c) distribution: recycle matches truth; naive stacking too wide">
      </div>
      <p style="margin-top:0.4em;"><b>Recycle (blue)</b> sits on the <b>truth (black)</b>.
      <b>Naive mean stack (red)</b> and <b>OLS on posterior means (orange)</b> are visibly
      wider &mdash; they fold per-cluster posterior noise into the population scatter once (OLS) or twice (pool).</p>
      <p style="margin-top:0.3em;"><small>Adding $\lambda_j$ promotes $\Lambda$ to the richness&ndash;mass
      relation &rarr; bridges to $S_8$ (see diagram above).</small></p>
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
