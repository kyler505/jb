# jb — Job Application Vault

> [!abstract] What This Is
> An [[Obsidian]] vault for tracking **Fall 2026 internship** and **2027 new grad** applications. Populated daily by [job-scraper](https://github.com/kyler505/job-scraper) via GitHub Actions.

## Structure

```
jb/
├── Dashboard.md              # Home page — MOC, views, pipeline status
├── README.md                 # This file — setup, sync, contract
├── Jobs/                     # One .md note per listing (~1900+)
├── Jobs.base                 # Obsidian Bases database — filterable views
│
├── Profile/
│   ├── Profile.md            # Applicant contact info & demographics
│   ├── Targeting.md          # Auto-apply rules & constraints
│   ├── QA/                   # Reusable answer bank (self-healing)
│   ├── Resumes/              # LaTeX resume source (.tex → .pdf)
│   └── Materials/            # Cover letters, interview prep, STAR stories
│
├── Profile.base              # Bases DB for QA files
├── auto-apply/               # Human-in-the-loop pipeline scripts
├── Workflow.canvas           # Pipeline flow visualization
└── Strategy.canvas           # Job search strategy mind map
```

> [!tip] Quick Start
> Open **[[Dashboard]]** in Obsidian.

---

## Setup (one-time)

1. Install the **obsidian-git** community plugin in this vault.
2. Configure it to pull from this repo on startup or on a schedule.
3. Grant the `job-scraper` workflow access: create a fine-grained GitHub PAT with **Contents: read/write** scoped to this repo, and add it as secret `JB_REPO_TOKEN` in the `job-scraper` repo settings.

---

## How Notes Work

Each `Jobs/*.md` note has YAML frontmatter with two field categories:

> [!note] Scraped Fields (refreshed daily)
> `company` · `role` · `locations` · `terms` · `url` · `active` · `date_posted` · `date_updated`

> [!warning] User-Owned Fields (preserved across syncs)
> `status` · `applied_date` · `deadline` · `notes`

A listing removed from the source feed is marked `active: false` but **never deleted**, so your application history is preserved.

---

## Auto-Apply Pipeline Contract

This vault is the data layer for an external auto-apply pipeline. The pipeline reads applicant data from `Profile/` and writes results back into `Jobs/` notes.

### Pipeline Reads (Inputs)

| File | Purpose |
|------|---------|
| `Profile/Profile.md` | Applicant contact info, links, work authorization, EEO answers |
| `Profile/Targeting.md` | Auto-apply rules: categories, terms, locations, daily cap, resume mapping |
| `Profile/QA/*.md` | Reusable answers (frontmatter: question/keywords/category; body: answer text) |
| `Profile/Resumes/*.tex` | LaTeX resume source — pipeline compiles to PDF and attaches |

### Pipeline Write-Back (into `Jobs/*.md` frontmatter)

| Field | Values | Purpose |
|-------|--------|---------|
| `apply_method` | `auto` \| `manual` | How the application was submitted |
| `apply_result` | `success` \| `error` \| `needs-review` | Outcome of the apply attempt |
| `apply_error` | string \| null | Error message if `apply_result == error` |
| `confirmation` | string \| null | Confirmation number/ID returned by the site |
| `resume_used` | string \| null | Which `Resumes/<name>.tex` was attached |
| `needs_review` | bool | True = pipeline could not finish; requires manual action |

> [!danger] Cross-Repo Dependency
> All write-back fields above **must** be added to the preserved-fields list in the `kyler505/job-scraper` repo. If they're not, the daily scrape strips them.

Generated answers and cover letters are written to the **note body** under `## Application <date>`. Bodies survive daily re-scrapes.
