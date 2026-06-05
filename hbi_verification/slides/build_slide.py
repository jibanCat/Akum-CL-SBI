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
      <h1>Hierarchical Bayesian mass calibration of clusters via posterior reuse</h1>
      <p class="sub">Recycle stored per-cluster WL mass posteriors to infer the mass&ndash;observable relation that feeds cluster cosmology &mdash; <i>no per-cluster re-fits per cosmology step</i>.</p>
    </div>
    <span class="pill">project pitch &middot; Ming-Feng Ho</span>
  </div>

  <!-- HERO PIPELINE -->
  <div class="hero">
    <img src="data:image/png;base64,__PIPELINE__" alt="lambda observed -> M latent -> Lambda -> cosmology">
  </div>

  <!-- THREE CARDS -->
  <div class="body3">

    <!-- 1. THE PROBLEM (cluster cosmologists already know this) -->
    <div class="card">
      <h2>The mass-calibration bottleneck</h2>
      <p>Cluster counts pin $S_8 = \sigma_8\sqrt{\Omega_m/0.3}$ via the
      abundance integral</p>
      <div class="eq">$$\langle N(\lambda^{\rm obs}\!\in\!\text{bin},z)\rangle = \!\!\int\!\! dM\;\tfrac{dn}{dM}(M,z;\sigma_8,\Omega_m)\,P(\lambda^{\rm obs}\!\mid\! M)$$</div>
      <p>So $P(\lambda\mid M)$ &mdash; the mass&ndash;observable relation (MOR) &mdash; is the
      load-bearing object.</p>
      <p>Per-cluster WL masses are noisy. <b>Point-mass fits</b> of
      $\langle M\mid\lambda\rangle$ attenuate the slope (Eddington / regression dilution).
      <b>Forward-modeling</b> $P(\lambda\mid M)\!\otimes\!dn/dM$
      (Murata18, Costanzi19, Bocquet24) is unbiased &mdash; but re-evaluates the
      per-cluster likelihood at <i>every</i> $\Lambda$-proposal in the
      cosmology MCMC.</p>
      <p class="tag">Refs:
        <a href="https://arxiv.org/abs/1707.01907">Murata18</a>,
        <a href="https://arxiv.org/abs/1810.09456">Costanzi19</a>,
        <a href="https://arxiv.org/abs/1812.01679">Bocquet19</a>/<a href="https://arxiv.org/abs/2310.12213">24</a>.
      </p>
    </div>

    <!-- 2. THE PROPOSAL: recycle stored posteriors -->
    <div class="card green">
      <h2>Proposal: recycle stored posteriors</h2>
      <p>Treat $(A,B,\sigma_{\ln\lambda\mid M})$ as <b>hyper-parameters</b> $\Lambda$ and
      marginalise the latent $M_j$ analytically:</p>
      <div class="eq">$$p(\Lambda\mid d)\propto\pi(\Lambda)\,\prod_j\!\int\! p(\lambda_j\mid M_j,\Lambda)\,p(M_j\mid d_j)\,dM_j$$</div>
      <p>With stored chains $\{M_j^{(s)}\}\sim p(M_j\mid d_j)$ from an interim prior $\pi_0$
      (the GW population trick, Thrane&nbsp;&amp;&nbsp;Talbot 2019):</p>
      <div class="eq">$$\!\int\! \!\cdot\!\,dM\;\approx\;\frac{\mathcal Z_j}{S}\!\sum_s\! p(\lambda_j\mid M_j^{(s)},\Lambda)\,\frac{p(M_j^{(s)})}{\pi_0(M_j^{(s)})}$$</div>
      <p>The weight <span class="callout">$p(M)/\pi_0 = dn/dM$</span> &mdash; the halo mass function &mdash; is
      <i>where cosmology enters</i>, and is what kills the Eddington bias.
      <b>No per-cluster likelihood call at any $\Lambda$.</b></p>
      <p class="tag">Refs: <a href="https://arxiv.org/abs/1809.02293">Thrane&nbsp;&amp;&nbsp;Talbot19</a>,
      <a href="https://arxiv.org/abs/1809.02063">Mandel&nbsp;Farr&nbsp;Gair19</a>.</p>
    </div>

    <!-- 3. WHY THIS FITS THE FIELD NOW + toy result -->
    <div class="card red">
      <h2>Why this matters for clusters now</h2>
      <ul>
        <li><b>Computational:</b> decouples per-cluster WL fit from cosmology MCMC; same chains serve any $\Lambda$.</li>
        <li><b>Modular:</b> works for any pipeline that already stores chains &mdash; SBI <i>or</i> MCMC (e.g. LSSTDESC/CL-SBI).</li>
        <li><b>Stage&nbsp;IV ready:</b> Rubin/Euclid/CMB-S4 will produce per-cluster posteriors at scale; reuse turns them into an MOR likelihood for free.</li>
        <li><b>Extensible:</b> drop-in for Bocquet24-style multi-observable population modelling ($\lambda$ + SZ + X-ray).</li>
      </ul>
      <div class="grow">
        <img src="data:image/png;base64,__RICHNESS__" alt="three attempts: naive OLS / flat recycle / recycle + dn/dM">
      </div>
      <p><small>Toy: <b>naive OLS</b> &amp; <b>flat-prior recycle</b> attenuate $B\!\to\!0.62$ (Eddington);
      <b>recycle + $dn/dM$</b> recovers truth $B=1.00\pm0.10$, $\sigma_{\ln\lambda\mid M}=0.30\pm0.06$.</small></p>
    </div>

  </div>

  <!-- FOOTER -->
  <div class="foot">
    <div><b>Roadmap.</b> (i) validate reuse vs joint Bocquet-style MCMC on realistic NFW shear profiles; (ii) multi-observable extension; (iii) DESC Note + open-source notebooks.</div>
    <div class="refs">
      <a href="https://arxiv.org/abs/1707.01907">Murata18</a>
      <a href="https://arxiv.org/abs/1810.09456">Costanzi19</a>
      <a href="https://arxiv.org/abs/1812.01679">Bocquet19</a>
      <a href="https://arxiv.org/abs/2310.12213">Bocquet24</a>
      <a href="https://arxiv.org/abs/1809.02293">Thrane&amp;Talbot19</a>
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
