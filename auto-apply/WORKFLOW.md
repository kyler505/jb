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

### Self-healing Q&A (learn-once, reuse-forever)
When the Apply step hits a question that **isn't covered by `Profile/` and has no
confident match in the Q&A bank** — e.g. "expected hourly rate?", "willing to
relocate?", "security clearance?", "preferred start date?" — Claude does NOT
guess. It:
1. Looks up the question first: `python qa_store.py find "<question>"`.
2. If no confident match, **asks you** for the answer.
3. Records your answer to the bank: `python qa_store.py record "<question>" "<answer>"`
   → creates `Profile/QA/<slug>.md` (`category: learned`, `source: self-heal`).
4. Uses it now, and **auto-answers it next time** — the bank grows with every
   application, so the same question never interrupts you twice.

Matching is token-overlap + keyword-phrase based, so paraphrases ("salary
expectations" vs "expected hourly rate") still resolve to the stored answer.
Edit or delete any `source: self-heal` note in `Profile/QA/` to correct what was
learned.

### Browser-step gotchas (learned the hard way)
- **Always type into fields with real keystrokes**, never set values
  programmatically. Frameworks like Ashby track their own internal state via
  input events; a directly-set value shows on screen but fails validation as
  "missing" on submit. (This bit the 1Password Full Name field.) Use real
  click + type; for typeahead/combobox fields, type then click the option.
- **Scan for duplicate required questions before submitting.** Some postings
  repeat a question in both a general section and a role-specific section (the
  1Password form had "What brought you to this job posting" twice). Fill every
  instance, then submit — the validation banner only lists what's still empty,
  so re-check it after each submit attempt until it clears.
- **Verify after submit.** A real submission ends on a success page / green
  confirmation. If the form re-renders with a red "needs corrections" banner,
  it did NOT submit — read the banner, fix, resubmit.
- **Upload the resume BEFORE typing other fields (Ashby).** Ashby's "autofill
  from resume" re-renders the form on upload and wipes anything typed just
  before. Attach the resume first, let it settle, then fill the text fields.
- **Native dropdowns: select with the keyboard, not a value-set.** On sites like
  Tesla, programmatically setting a `<select>` value often doesn't register with
  the component. Click the field, type the option text, press Enter. (Holds for
  country, months, gender/EEO selects, etc.)
- **Don't press Enter/Return inside a date textbox on Tesla** — it navigates to
  the previous step and clears that step. Use the calendar picker instead, or
  type then click away.
- **Acknowledgement checkboxes may be gated behind a scrollable disclosure.**
  Tesla's EEO acknowledgement stays disabled until the disclosure box is scrolled
  to its very bottom. Scroll inside that box first, then check it.
- **Multi-step forms re-mint element refs on each step change.** After clicking
  Next/Previous, re-read the page for fresh refs before acting.

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

---

## Workday (`myworkdayjobs.com`) handling

Workday powers most large enterprises. Detect it by `*.myworkdayjobs.com` in the
`url`. Flow: **Apply → "Start Your Application" modal → "Apply Manually"** (also
offers "Autofill with Resume" / "Use My Last Application"), then a 6-step wizard:

`My Information → My Experience → Application Questions → Voluntary Disclosures → Self Identify → Review`

### The account wall is tenant-dependent (and is the hard stop)
- **Defer-type** (e.g. Adobe `wd5`): you can fill all 6 steps; account creation
  (email + password) is only demanded at the final **Submit**. Fill everything,
  stop at Submit.
- **Gate-type** (e.g. GE Appliances `haier.wd3`): a **Create Account** screen
  (email + password) is step 0, before any form fields. Hard stop immediately.

Either way, **never create the account or enter a password** — that's the user's
action, same as any submit. Fill up to the account/Submit boundary and hand off.

### Field-handling notes (learned on Adobe `wd5`)
- **"How Did You Hear About Us?"** is a nested picklist: pick a category
  (Job Board, Social Media, Through my University...) then an option. No generic
  "Other" under Job Board; LinkedIn is a reasonable default but it's a
  per-application judgment call.
- **State** is a native `<select>`: type-ahead works (click, type "Texas", Enter).
- **Country / Country Phone Code** usually default to US; **Phone Device Type**
  defaults to Mobile.
- **Address** (street, line 2, city, state, postal) is often *optional* — fill
  City/State from Profile; Profile has no street address or ZIP, so if a tenant
  marks them required, self-heal (ask + record).
- **My Experience**: Job Title / Company / Location + "I currently work here";
  employment start dates aren't in Profile — self-heal if required. Also has an
  Education block and a resume upload (attach `out/resumes/<name>.pdf`).
- **Application Questions / Voluntary Disclosures / Self Identify**: map from
  Profile + QA bank exactly like the other platforms (work auth, sponsorship =
  No, grad date 2027-05, gender/race/veteran/disability).

### Gotcha
Workday is heavy; `Page.captureScreenshot` and ref reads time out intermittently
even though the page is fine. Retry after a short wait; prefer keyboard selection
for dropdowns; re-read refs after each step transition.
