# auto-apply pipeline — assessment (2026-06-23)

Snapshot of the job-application pipeline in the `jb` vault, what it does, its
current state, and the open issues found during review.

## What it is

A two-stage, human-in-the-loop pipeline. It does everything up to the submit
button and never auto-submits (the big hosts — Workday, Greenhouse, Lever,
Ashby, LinkedIn — prohibit automated submission).

- **Stage 1 — Prep** (`run.py`, file-only, safe to schedule)
  1. Filter `Jobs/*.md` by `Profile/Targeting.md` and rank them (`priority` score).
  2. Write the ranked daily queue → `out/queue.md` + `out/queue.json`.
  3. Compile the resume `Profile/Resumes/<name>.tex` → `out/resumes/<name>.pdf`.
  4. Write an `## Application <date>` packet into each queued note (autofill data,
     screening answers, drafted cover letter, placeholder review checklist).
- **Stage 2 — Apply** (interactive, "Cowork" = Claude driving Chrome)
  Opens each `Apply URL`, prefills the form, stops for human review, then writes
  back `status/apply_result/confirmation/...`. Self-healing Q&A bank learns
  answers once and reuses them.

## Module map

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

## Current state (verified 2026-06-23)

- Stage 1 runs clean under Python 3.14.5 (pyyaml 6.0.3). Smoke test
  (`run.py --select-only --no-priority-write`) queued 25/1888 eligible.
- `out/queue.md` regenerated 2026-06-23 13:16; `out/resumes/resume.pdf` compiled
  2026-06-23 08:17 (109 KB).
- Vault application status: **3 applied, 3 apply_result=success, 2 needs-review,
  ~3374 still to-apply.** Stage 1 runs daily; Stage 2 has barely run.

## Open issues

1. **Throughput near zero.** Only 3 successful submissions. Two stuck in
   needs-review (both legitimate human-handoff cases):
   - *Rivian – Android Developer Intern*: Ashby flagged automated submission as
     spam; form fully prefilled, needs manual submit.
   - *Zipline – Enterprise Systems SWE Intern*: Greenhouse sent an 8-char email
     verification code to kcao@tamu.edu — enter it to finish.
2. **Corrupted note** `Jobs/Cerebras - Software Engineer Intern.md` — 7,451 null
   bytes (sync/write interruption). Corruption is committed and present (20+
   nulls) throughout git history; no pristine copy. Needs regeneration from the
   scraper source.
3. **Cross-repo preserved-fields dependency (root cause of the daily merge
   conflicts).** `priority, apply_method, apply_result, apply_error,
   confirmation, resume_used, needs_review` must be in the
   `kyler505/job-scraper` preserved-fields list, or the daily GitHub Actions
   scrape strips/overwrites them. The 41-file conflict resolved on 2026-06-23 was
   exactly local vs. scrape disagreeing on `priority`. Will recur daily until the
   list is verified current.
4. **212 uncommitted local edits** (2026-06-22 packets + priority updates) sit
   unstaged — not pushed, not backed up.
5. **No LaTeX engine on the interactive shell PATH** (pdflatex/tectonic/xelatex).
   The scheduled run has one (PDF compiled at 08:17), so not broken — just can't
   compile manually from this shell.

## Suggested order of attack

1. Verify the preserved-fields list in `kyler505/job-scraper` (stops the daily conflicts).
2. Finish the 2 needs-review applications.
3. Regenerate the corrupted Cerebras note.
