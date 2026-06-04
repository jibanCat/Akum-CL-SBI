# tobemerged_review/

Read-only audit of Akum's current development branch **`upstream/tobemerged`** (LSST-DESC/CL-SBI). Branch
not merged; nothing pushed; `main` and `mfho/hbi-verification` untouched.

## Files
- **`BUG_REPORT_tobemerged.md`** — status of the eight original `../BUG_REPORT.md` findings against the new
  branch (5 fixed, 1 partially, 1 moot, **1 surviving load-bearing** = the `1/N_c` in `joint_logprob`).
- **`tobemerged_demo.py`** — numeric demo that replicates Akum's `joint_logprob` (verbatim shape) and
  confirms `joint_logprob_tobemerged / joint_logprob_fixed = √N_c` (measured 4.51 vs √20 = 4.47).

## How I read tobemerged without merging anything
```bash
git remote add upstream git@github.com:LSSTDESC/CL-SBI.git
git remote set-url --push upstream "DO_NOT_PUSH_to_upstream__readonly_only"   # safety net
git fetch upstream --prune
git show upstream/tobemerged:weaklensclustersbi/inference/mcmcutils.py        # inspect without checkout
```
Both `main` and `mfho/hbi-verification` remain on `origin`-only.
