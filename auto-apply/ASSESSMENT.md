---
tags:
  - pipeline
  - assessment
---

# Auto-Apply Pipeline — Assessment

> [!info] Snapshot Date
> ==2026-06-23== · Last verified working state.

> [!abstract] What It Is
> A two-stage, human-in-the-loop pipeline. It does everything up to the submit button and never auto-submits (the big hosts — Workday, Greenhouse, Lever, Ashby, LinkedIn — prohibit automated submission).

```mermaid
flowchart LR
    A[Stage 1 — Prep] -->|idempotent, file-only| B[Stage 2 — Apply]
    B -->|human reviews then clicks| A
```

---

## Module Map

| File | Role |
|------|------|
| `config.py` | Paths + scoring weights (ranking lives here) |
| `vault.py` | Safe frontmatter/body read-write (preserves scraped fields) |
| `profile_data.py` | Loads Profile, Targeting, Q&A bank, cover template |
| `selector.py` | Filters + ranks jobs, writes `priority`, emits queue |
| `build_resume.py` | Compiles `Profile/Resumes/*.tex` → PDF |
| `prepare.py` | Writes the `## Application <date>` packet into each note |
| `qa_store.py` | Q&A bank find/record (self-heal) |
| `run.py` | Stage 1 orchestrator |
| `out/` | Generated queue + compiled PDFs (git-ignored) |

## Current State

> [!success] Verified (2026-06-23)
> - Stage 1 runs clean under Python 3.14.5 (pyyaml 6.0.3)
> - Smoke test (`run.py --select-only --no-priority-write`) queued 25/1888 eligible
> - `out/queue.md` regenerated, `out/resumes/resume.pdf` compiled (109 KB)

> [!warning] Application Status
> - **3** applied, **3** apply_result=success, **2** needs-review, **~3374** still to-apply
> - Stage 1 runs daily; Stage 2 has barely run

---

## Open Issues

> [!danger] 1. Throughput Near Zero
> Only 3 successful submissions. Two stuck in needs-review:
> - *Rivian – Android Developer Intern*: Ashby flagged automated submission as spam; form fully prefilled, needs manual submit
> - *Zipline – Enterprise Systems SWE Intern*: Greenhouse sent email verification code to `kcao@tamu.edu` — enter it to finish

> [!danger] 2. Corrupted Note
> `Jobs/Cerebras - Software Engineer Intern.md` — 7,451 null bytes (sync/write interruption). Corruption is committed and present throughout git history; no pristine copy. Needs regeneration from the scraper source.

> [!danger] 3. Cross-Repo Preserved-Fields Dependency ^preserved-fields
> `priority`, `apply_method`, `apply_result`, `apply_error`, `confirmation`, `resume_used`, `needs_review` must be in the `kyler505/job-scraper` preserved-fields list, or the daily GitHub Actions scrape strips/overwrites them. The 41-file conflict resolved on 2026-06-23 was exactly local vs. scrape disagreeing on `priority`. **Will recur daily until the list is verified current.**

> [!warning] 4. Uncommitted Local Edits
> 212 uncommitted local edits (2026-06-22 packets + priority updates) sit unstaged — not pushed, not backed up.

> [!warning] 5. No LaTeX Engine on Interactive Shell PATH
> `pdflatex`/`tectonic`/`xelatex` not available from this shell. The scheduled run has one (PDF compiled at 08:17), so not broken — just can't compile manually from here.

---

## Suggested Order of Attack

1. **Verify preserved-fields list** in `kyler505/job-scraper` (stops daily conflicts)
2. **Finish the 2 needs-review** applications (Rivian, Zipline)
3. **Regenerate the corrupted** Cerebras note
4. **Run Stage 1 daily** to build up the applied count
