---
title: Job Search Dashboard
type: moc
tags: [moc]
---

# Job Search Dashboard

Fall 2026 Internships · 2027 New Grad · Graduating Spring 2027

## Database

Open [[Jobs.base]] to browse and filter all listings.

| View | Purpose |
|------|---------|
| **To Apply** | Active listings you haven't acted on yet |
| **Applied** | Submitted applications |
| **Interviewing** | In-progress interviews |
| **Internships** | All Fall 2026 internship listings |
| **New Grad** | All 2027 new grad listings |
| **All** | Everything |

## How to use

1. Open `Jobs.base` → **To Apply** view.
2. Click any row to open the note.
3. Set `status:` to one of: `to-apply` · `applied` · `interviewing` · `offer` · `rejected` · `skip`
4. Fill in `deadline:` and `applied_date:` (format `YYYY-MM-DD`) so the view sorts correctly.
5. Add free-text notes in the body below the frontmatter — they survive daily re-scrapes.
6. Use the **Discipline** column to filter by tech role: `swe` · `ml` · `data` · `devops` · `security` · `hardware` · `mobile` · `frontend` · `backend` · `other`

> **Sync:** This vault is updated daily by GitHub Actions (job-scraper repo). Pull the latest via the obsidian-git plugin (`Ctrl+P` → "Obsidian Git: Pull"). Scraped fields (company, role, locations, url, etc.) are refreshed each run; your `status`, `deadline`, `applied_date`, `notes`, and body text are always preserved.


---

## Auto-applier

The pipeline reads applicant data from `Profile/` and writes results back into job notes.

| Resource | Purpose |
|----------|---------|
| [[Profile/Profile]] | Contact info, links, work authorization, EEO answers |
| [[Profile/Targeting]] | Auto-apply rules (categories, caps, resume-to-category mapping) |
| [[Profile.base]] | Q&A bank — questions and reusable answers the pipeline submits |
| `Profile/Resumes/` | LaTeX resume source files (pipeline compiles to PDF) |

### New Jobs.base views

| View | Shows |
|------|-------|
| **Needs Review** | Jobs the pipeline could not complete — requires your manual action |
| **Auto-Applied** | All jobs where `apply_method == auto` |

**Write-back fields** set by the pipeline on each job note: `apply_method`, `apply_result`, `apply_error`, `confirmation`, `resume_used`, `needs_review`. Generated answers are written into the note body under `## Application <date>`.

> **Sync reminder:** Write-back fields must be added to the preserved-fields list in `job-scraper` before relying on them surviving a daily scrape.