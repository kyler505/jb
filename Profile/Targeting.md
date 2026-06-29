---
type: targeting
include_categories:
  - internship
  - new-grad
include_terms:
  - Fall 2026
include_locations: []
exclude_companies: []
exclude_keywords: []
daily_cap: 25
resume_by_category:
  internship: resume
  new-grad: resume
tags:
  - targeting
  - auto-apply
---

> [!info] Targeting Rules
> Edit the frontmatter to control which jobs the auto-apply pipeline targets. These fields are read by `auto-apply/selector.py` each run.

> [!example] Current Configuration
> - **Categories:** `internship`, `new-grad`
> - **Terms:** `Fall 2026`
> - **Locations:** `[]` (no filter — all locations)
> - **Daily Cap:** 25 jobs per run
> - **Resume:** `resume` for both internships and new-grads

> [!tip] Adding Resume Variants
> Drop variant resumes (e.g. `swe.tex`, `infra.tex`) into `Profile/Resumes/` and add entries to `resume_by_category` to auto-attach different resumes for different role categories.

> [!danger] Exclude Lists
> Use `exclude_companies` and `exclude_keywords` to block specific employers or roles. Empty lists = no exclusions.

> [!warning] Location Filter
> When `include_locations` is empty, all locations are eligible. Add entries (e.g. `Austin, TX`) to restrict to location-sorted listings. Requires listings to have location data in the scraper.
