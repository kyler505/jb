# Cowork workflow — job application pipeline

A **human-in-the-loop** pipeline. It does everything up to the submit button:
ranks jobs, compiles the right resume, drafts every answer, prefills the form in
your browser — then **you review and click submit**. It never submits on its own.

> Why not fully automatic? The big application hosts (Workday, Greenhouse, Lever,
> Ashby, LinkedIn) prohibit automated submission, and auto-firing answers to
> work-authorization, EEO, and screening questions under your name risks
> submitting wrong information. Prefill + review keeps you fast *and* in control.

---

## The two stages

### Stage 1 — Prep (file-only, safe to automate / schedule)
```
cd auto-apply
python run.py                 # full daily cap from Profile/Targeting.md
python run.py --limit 5       # just the top 5 (good for a pilot)
python run.py --select-only   # rebuild the ranked queue, don't write packets
```
This:
1. Filters `Jobs/*.md` by `Profile/Targeting.md` and ranks them (`priority` score).
2. Writes the ranked daily queue to `auto-apply/out/queue.md` + `queue.json`.
3. Compiles the resume (`Profile/Resumes/<name>.tex` → `out/resumes/<name>.pdf`).
4. Writes an `## Application <date>` packet into each queued job note:
   autofill data, screening answers, a drafted cover letter, and a review
   checklist with every company-specific placeholder flagged.

Nothing is submitted. Re-running is idempotent (it replaces the day's packet).

### Stage 2 — Apply (interactive, in Cowork with Claude in Chrome)
Ask Cowork: **"Run the apply workflow on today's queue"** (or "…on the top 3").
For each job, Claude will:
1. Open the job note's `Apply URL` in your connected browser.
2. Research the company and fill the flagged `{{placeholders}}` (the
   "why this company" lines) so the answers are specific and true.
3. Prefill the form from the **Autofill data** and **Screening answers** blocks,
   and attach `out/resumes/<name>.pdf`.
4. **Stop and show you the filled form for review.**
5. Only after you confirm, you click submit. Claude then writes the result back:
   - `status: applied`, `applied_date: <today>`
   - `apply_method: auto` (pipeline-prefilled) or `manual` (you did most of it)
   - `apply_result: success`, `confirmation: <id if shown>`
   - on any blocker: `apply_result: needs-review`, `needs_review: true`,
     `apply_error: <what happened>` — it surfaces in the **Needs Review** view.

---

## Daily routine
1. (Optional, automated) Stage 1 runs each morning and refreshes the queue.
2. Open Obsidian → `Jobs.base` → **By Priority** to see today's ranked targets,
   or **Needs Review** for anything that stalled.
3. In Cowork, run the apply workflow; review and submit each form.
4. Check **Auto-Applied** / **Applied** to confirm write-backs landed.

## Tuning
- **Targets:** edit `Profile/Targeting.md` (categories, terms, locations,
  `exclude_companies`, `exclude_keywords`, `daily_cap`, `resume_by_category`).
- **Ranking:** edit weights in `auto-apply/config.py` (`DISCIPLINE_WEIGHTS`,
  `CATEGORY_WEIGHTS`, recency, location bonus).
- **Answers:** edit `Profile/QA/*.md`; fill blank ones (e.g. salary).
- **Resumes:** add variants (e.g. `swe.tex`) to `Profile/Resumes/` and map them
  in `Targeting.resume_by_category`.

## ⚠ Cross-repo dependency
The pipeline writes these frontmatter fields:
`priority, apply_method, apply_result, apply_error, confirmation, resume_used, needs_review`.
They **must** be added to the preserved-fields list in the `kyler505/job-scraper`
repo, or the daily scrape will strip them. (Body `## Application` sections already
survive re-scrapes.)
