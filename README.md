# jb — Job Application Vault

Obsidian vault for tracking Fall 2026 internship and 2027 new grad applications. Populated daily by [job-scraper](https://github.com/kcao-gss/job-scraper) via GitHub Actions.

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
