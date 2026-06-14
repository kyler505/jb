# jb — Job Application Vault

Obsidian vault for tracking Fall 2026 internship and 2027 new grad applications. Populated daily by [job-scraper](https://github.com/kyler505/job-scraper) via GitHub Actions.

## Structure

```
Jobs/          one .md note per active listing (auto-generated)
Jobs.base      Obsidian Bases database — views by status, category
Dashboard.md   home note with navigation and usage guide
```

## Sync setup (one-time)

1. Install the **obsidian-git** community plugin in this vault.
2. Configure it to pull from this repo on startup or on a schedule.
3. Grant the `job-scraper` workflow access: create a fine-grained GitHub PAT with **Contents: read/write** scoped to this repo, and add it as secret `JB_REPO_TOKEN` in the `job-scraper` repo settings.

## How notes work

Each `Jobs/*.md` note has a YAML frontmatter block with two kinds of fields:

- **Scraped fields** (`company`, `role`, `locations`, `terms`, `url`, `active`, `date_posted`, `date_updated`) — refreshed on every daily run.
- **User-owned fields** (`status`, `applied_date`, `deadline`, `notes`) — written once on creation, then never overwritten. Set these in Obsidian.

A listing removed from the source feed is marked `active: false` but never deleted, so your application history is preserved.


## Auto-applier pipeline contract

This vault is the data layer for an external auto-applier pipeline. The pipeline reads applicant data from `Profile/` and writes results back into `Jobs/` notes.

### Pipeline reads (inputs)

| File | Purpose |
|------|---------|
| `Profile/Profile.md` | Applicant contact info, links, work authorization, EEO answers |
| `Profile/Targeting.md` | Auto-apply rules: categories, terms, locations, daily cap, resume mapping |
| `Profile/QA/*.md` | Reusable answers (frontmatter: question/keywords/category; body: answer text) |
| `Profile/Resumes/*.tex` | LaTeX resume source — pipeline compiles to PDF and attaches |

### Pipeline write-back (into `Jobs/*.md` frontmatter)

| Field | Values | Purpose |
|-------|--------|---------|
| `apply_method` | `auto` \| `manual` | How the application was submitted |
| `apply_result` | `success` \| `error` \| `needs-review` | Outcome of the apply attempt |
| `apply_error` | string \| null | Error message if `apply_result == error` |
| `confirmation` | string \| null | Confirmation number/ID returned by the site |
| `resume_used` | string \| null | Which `Resumes/<name>.tex` was attached |
| `needs_review` | bool | True = pipeline could not finish; requires manual action |

Generated answers and cover letters are written to the **note body** under `## Application <date>`. Bodies survive daily re-scrapes.

> **Cross-repo dependency:** All write-back fields above must be added to the preserved-fields list in the `kyler505/job-scraper` repo. If not, the daily scrape will strip them.