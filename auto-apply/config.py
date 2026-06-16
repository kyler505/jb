"""Central configuration for the auto-apply pipeline.

All paths are resolved relative to the vault root (the parent of this folder),
so the pipeline works regardless of where the vault is checked out.
"""
from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PKG_DIR = Path(__file__).resolve().parent          # <vault>/auto-apply
VAULT = PKG_DIR.parent                              # <vault>

JOBS_DIR = VAULT / "Jobs"
PROFILE_DIR = VAULT / "Profile"
PROFILE_MD = PROFILE_DIR / "Profile.md"
TARGETING_MD = PROFILE_DIR / "Targeting.md"
QA_DIR = PROFILE_DIR / "QA"
RESUMES_DIR = PROFILE_DIR / "Resumes"
MATERIALS_DIR = PROFILE_DIR / "Materials"
COVER_TEMPLATE = MATERIALS_DIR / "Cover Letter Template.md"

# Generated outputs (git-ignored). Never commit compiled PDFs or the live queue.
OUT_DIR = PKG_DIR / "out"
QUEUE_JSON = OUT_DIR / "queue.json"
QUEUE_MD = OUT_DIR / "queue.md"
RESUME_PDF_DIR = OUT_DIR / "resumes"

# ---------------------------------------------------------------------------
# Priority scoring weights
# ---------------------------------------------------------------------------
# Higher score = applied to first. Tunable; transparent on purpose.
DISCIPLINE_WEIGHTS = {
    "swe": 30,
    "ml": 28,
    "backend": 26,
    "data": 24,
    "frontend": 22,
    "mobile": 18,
    "devops": 18,
    "security": 16,
    "hardware": 8,
    "other": 6,
}

CATEGORY_WEIGHTS = {
    "internship": 12,   # graduating Spring 2027 -> Fall 2026 internship is the priority
    "new-grad": 10,
}

# Recency: points decay by days since posting.
RECENCY_MAX_POINTS = 20
RECENCY_HALF_LIFE_DAYS = 21

# Bonus when a job location matches Targeting include_locations (if any set).
LOCATION_MATCH_BONUS = 15

# Cap how many top-ranked notes get a `priority` written back (keeps the daily
# run fast; the "By Priority" view only needs the strongest candidates ranked).
PRIORITY_WRITE_LIMIT = 200

# Write-back / pipeline-managed frontmatter fields. These MUST be added to the
# preserved-fields list in the job-scraper repo or the daily scrape strips them.
WRITEBACK_FIELDS = [
    "priority",
    "apply_method",
    "apply_result",
    "apply_error",
    "confirmation",
    "resume_used",
    "needs_review",
]
