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

> **Sync:** This vault is updated daily by GitHub Actions (job-scraper repo). Pull the latest via the obsidian-git plugin (`Ctrl+P` → "Obsidian Git: Pull"). Scraped fields (company, role, locations, url, etc.) are refreshed each run; your `status`, `deadline`, `applied_date`, `notes`, and body text are always preserved.
