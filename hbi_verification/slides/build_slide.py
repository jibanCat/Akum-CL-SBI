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
      <p class="sub">Follow-up to <i>Gill et al. (in prep.)</i> &mdash; their SBI pipeline produces per-cluster $(M,c)$ posteriors; we recycle those stored chains to infer population-level scaling relations <b>without re-fitting any cluster</b> and at a fraction of the cost of a full joint HBI.</p>
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
      <p>The paper's discussion (&sect;6 <i>Hierarchical Modeling</i>) flags population-level
      inference &mdash; the mass&ndash;observable relation, intrinsic scatter, ultimately cosmology
      &mdash; as the natural next step but leaves the formalism open.</p>
      <p><b>Our question:</b> can we build a <i>reuse framework</i> that combines these stored
      $\{M_j^{(s)}\}$ chains into population-level constraints, without re-running any per-cluster
      fit, and without paying the cost of a full joint $(\Lambda,\{M_j\})$ HBI?</p>
      <p class="tag">Stored per-cluster chains are also what Stage&nbsp;IV WL pipelines (Rubin/Euclid/CMB-S4) will produce at scale, so a posterior-reuse layer is broadly portable.</p>
    </div>

    <!-- 2. THE PROPOSAL: recycle stored posteriors -->
    <div class="card green">
      <h2>Hierarchical reuse: cheaper than joint HBI</h2>
      <p>Population parameters $\Lambda$ (e.g.&nbsp;MOR amplitude, slope, scatter). Hyper-posterior
      marginalising each cluster's latent mass:</p>
      <div class="eq">$$p(\Lambda\mid d)\;\propto\;\pi(\Lambda)\,\prod_j\!\int\! p(\mathrm{obs}_j\mid M_j,\Lambda)\,p(M_j\mid d_j)\,dM_j$$</div>
      <p><b>Recycling identity</b> &mdash; stored chains $\{M_j^{(s)}\}\sim p(M_j\!\mid\!d_j)$ under interim prior $\pi_0$ (GW population trick, Thrane&nbsp;&amp;&nbsp;Talbot&nbsp;2019):</p>
      <div class="eq">$$\!\int\!\!\cdot\,dM\;\approx\;\tfrac{\mathcal Z_j}{S}\!\sum_s\!p(\mathrm{obs}_j\!\mid\!M_j^{(s)},\Lambda)\,\tfrac{p(M_j^{(s)})}{\pi_0(M_j^{(s)})}$$</div>
      <p><b>Efficiency vs joint HBI.</b> Joint samples a $(2+N_c)$-dimensional posterior at every step
      (re-evaluates the per-cluster shear likelihood); reuse samples just $\dim(\Lambda)\!\sim\!3$ &mdash;
      per-cluster work is done <i>once, offline</i>, by CL-SBI.</p>
      <p>The weight <span class="callout">$p(M)/\pi_0 = dn/dM$</span> (halo mass function) carries
      cosmology and removes the Eddington bias <i>by construction</i>.</p>
    </div>

    <!-- 3. FUTURE-FACING: where reuse takes us -->
    <div class="card red">
      <h2>Future-facing: from MOR to cosmology</h2>
      <p>Once stored chains $+$ a population model are in hand, the same recycling machinery turns the
      hierarchy into the science output:</p>
      <ul>
        <li><b>Calibrate $P(\lambda\!\mid\!M)$ on real DES&nbsp;Y1&nbsp;/&nbsp;LSST clusters</b> using stored CL-SBI chains.</li>
        <li><b>Plug into the abundance likelihood</b> $\int dM\,dn/dM\cdot P(\lambda\!\mid\!M)$ to constrain $S_8$ &mdash; same hierarchical structure as Bocquet24.</li>
        <li><b>Multi-observable extension</b> (richness + SZ + X-ray) as drop-in additional factors.</li>
      </ul>
      <div class="grow">
        <img src="data:image/png;base64,__RICHNESS__" alt="toy: naive OLS / flat-prior recycle / recycle + dn/dM">
      </div>
      <p><small><b>Toy demonstration on the richness&ndash;mass relation</b>: naive OLS &amp; flat-prior recycle attenuate $B\!\to\!0.62$ (Eddington);
      recycle $+\,dn/dM$ recovers truth $B=1.00\pm0.10$, $\sigma_{\ln\lambda\mid M}=0.30\pm0.06$.</small></p>
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
