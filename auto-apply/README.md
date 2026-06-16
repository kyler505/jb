# auto-apply

Human-in-the-loop application pipeline for the `jb` job vault. Ranks jobs, drafts
answers + cover letters, compiles resumes, prefills forms for your review. It does
**not** auto-submit. Full process: see [WORKFLOW.md](WORKFLOW.md).

## Files
| File | Role |
|------|------|
| `config.py` | Paths + scoring weights (tune ranking here) |
| `vault.py` | Safe frontmatter/body read-write (preserves scraped fields) |
| `profile_data.py` | Loads Profile, Targeting, Q&A bank, cover template |
| `selector.py` | Filters + ranks jobs, writes `priority`, emits the queue |
| `build_resume.py` | Compiles `Profile/Resumes/*.tex` → PDF |
| `prepare.py` | Writes the `## Application <date>` packet into each job note |
| `run.py` | Orchestrator (Stage 1) |
| `out/` | Generated queue + compiled PDFs (git-ignored) |

## Quick start
```bash
cd auto-apply
pip install -r requirements.txt        # PyYAML; LaTeX engine for resume PDFs
python run.py --limit 5                # prep the top 5 jobs
```
Then run the **Apply** workflow in Cowork to prefill + review + submit each form.

## Requirements
- Python 3.10+ and `pyyaml`.
- A LaTeX engine (`pdflatex`, `xelatex`, or `tectonic`) for resume PDFs. Without
  one, prep still runs and points to the `.tex` to attach manually.
