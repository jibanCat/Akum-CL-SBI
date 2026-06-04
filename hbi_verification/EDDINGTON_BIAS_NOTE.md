# Do cluster cosmologists account for Eddington bias?

*Short answer for the project pitch (compiled from a focused arXiv-citation research pass).*

**Yes — universally, but under different names than the GW community uses.** The cluster literature has
been correcting for the same statistical effect that GW population inference calls "selection bias /
Eddington bias" for over 20 years; cluster people just call it **"mass-function weighting"**,
**"selection function"**, **"projection effects"**, or **"intrinsic vs observed scatter"**, and only the
X-ray flux-limited tradition (Stanek 2006, Mantz 2010, Allen-Evrard-Mantz 2011) and the Sereno CoMaLit
regression papers say "Malmquist" / "Eddington" / "regression dilution" out loud.

**Why it feels more GW than cluster:** Thrane & Talbot (2019) put hierarchical selection-bias front and
centre as the *headline* of GW population pedagogy, so the term is unavoidable in any LIGO
compact-binary analysis. Cluster cosmologists bake the same correction into the abundance likelihood as
the convolution
$$\langle N\rangle = \int dM\;n(M,z)\,P(\lambda^{\rm obs}\mid M,z)$$
without always naming it.

## Robust vs not-robust formulations

| Formulation | Used by | Robust to Eddington bias? | Why |
|---|---|---|---|
| **Forward** P(observable\|M) × dn/dM, jointly with cosmology | Murata 2018, Costanzi 2019a/b, Bocquet 2019/2024, Mantz 2010 | **Yes, by construction** | The mass-function weighting *is* the correction |
| **Stacked** ⟨M\|λ⟩ from stacked WL with flat mass prior in wide bins | McClintock 2019, Simet 2017 | Only in the **narrow-bin** limit | Eddington residual unless propagated downstream by a cosmology code (e.g. Costanzi 2019b) |

## Citation-dense reference list (clickable arXiv)

| Paper | Where the bias is addressed | Literal phrase used |
|---|---|---|
| [Murata 2018](https://arxiv.org/abs/1707.01907) (SDSS redMaPPer) | Lognormal P(ln λ\|M) convolved with n(M,z), joint abundance+WL fit | "intrinsic scatter", "P(ln λ\|M)" |
| [McClintock 2019](https://arxiv.org/abs/1805.00039) (DES Y1) | Stacked ⟨M\|λ⟩ in narrow (λ,z) bins; projection/triaxiality/centering | "stacked weak lensing signal", "projection effects" |
| [Simet 2017](https://arxiv.org/abs/1603.06953) (SDSS) | Long systematics budget; narrow bins implicitly correct | "projection effects", "dilution" |
| [Costanzi 2019a](https://arxiv.org/abs/1807.07072) (modelling) | Eq. 1: counts = ∫ dM n(M,z) P(λ_ob\|M); calibrates projection contribution from sims | "P(λ_ob\|M,z)", "halo mass function n(M,z)", "projection effects" |
| [Costanzi 2019b](https://arxiv.org/abs/1810.09456) (DES-Y1 methods + SDSS cosmology) | Full hierarchical likelihood with explicit selection function | "selection function", "richness–mass relation" |
| [Bocquet 2019](https://arxiv.org/abs/1812.01679) (SPT-SZ) | Hierarchical multi-observable scaling relations with lognormal intrinsic scatter and ξ-selection | "intrinsic scatter", "observable–mass relations" |
| [Bocquet 2024 Paper I](https://arxiv.org/abs/2310.12213) + [Paper II](https://arxiv.org/abs/2401.02075) | Bayesian population modeling across SZ + WL shear profiles + abundance | "Bayesian population modeling", "multi-observable likelihood" |
| [Mantz 2010](https://arxiv.org/abs/0909.3098) (X-ray) | **Explicitly** names Eddington & Malmquist; self-consistent joint likelihood | *"Malmquist and Eddington biases are ubiquitous"* |
| [Allen, Evrard & Mantz 2011 ARA&A](https://arxiv.org/abs/1103.4829) | Review-level discussion of selection + scaling-relations | "survey selection", "systematic error" |
| [Sereno & Ettori 2015 CoMaLit-I](https://arxiv.org/abs/1407.7868) + [IV](https://arxiv.org/abs/1502.05413) | Regression-dilution-style analysis of scaling relations; Bayesian regression with mass-function prior | "intrinsic scatter", "regression" |
| [Stanek 2006](https://arxiv.org/abs/astro-ph/0602324) (early L_X–M) | Lognormal P(L\|M); attributes L_X–M shift to Malmquist bias of HIFLUGCS flux limit | *"Malmquist bias of the X-ray flux-limited sample"* |

## Bottom line for the project

What you noticed is real: GW makes it the headline; cluster cosmology hides it inside the abundance
likelihood. Both communities are doing the **same hierarchical inference with a population prior** — the
GW "divide by detectable fraction" and the cluster "convolve with dn/dM" are dialects of the same thing.
For an HBI follow-up paper on cluster mass calibration, the modern citations to anchor it to are
**Murata 2018**, **Costanzi 2019a/b**, **Bocquet 2019/2024** (cluster forward-modelling), and
**Thrane & Talbot 2019**, **Mandel, Farr & Gair 2019** (GW formalism). Together they form the
"hierarchical likelihood with selection" framework that Tutorial 2 demonstrates in toy form.
