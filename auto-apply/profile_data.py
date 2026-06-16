"""Load applicant data: profile, targeting rules, and the Q&A answer bank."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import config
from vault import parse_frontmatter, split_note


@dataclass
class QAEntry:
    question: str
    keywords: list[str]
    category: str
    answer: str
    source: str  # filename


def load_profile() -> dict[str, Any]:
    return parse_frontmatter(config.PROFILE_MD.read_text(encoding="utf-8"))


def load_targeting() -> dict[str, Any]:
    t = parse_frontmatter(config.TARGETING_MD.read_text(encoding="utf-8"))
    t.setdefault("include_categories", ["internship", "new-grad"])
    t.setdefault("include_terms", [])
    t.setdefault("include_locations", [])
    t.setdefault("exclude_companies", [])
    t.setdefault("exclude_keywords", [])
    t.setdefault("daily_cap", 25)
    t.setdefault("resume_by_category", {})
    return t


def load_qa_bank() -> list[QAEntry]:
    entries: list[QAEntry] = []
    if not config.QA_DIR.exists():
        return entries
    for p in sorted(config.QA_DIR.glob("*.md")):
        text = p.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        _, body = split_note(text)
        # Skip empty/placeholder answers (only HTML comments / whitespace).
        answer = _strip_placeholder(body)
        entries.append(
            QAEntry(
                question=str(fm.get("question", p.stem)),
                keywords=[str(k).lower() for k in (fm.get("keywords") or [])],
                category=str(fm.get("category", "general")),
                answer=answer,
                source=p.name,
            )
        )
    return entries


def _strip_placeholder(body: str) -> str:
    import re

    cleaned = re.sub(r"<!--.*?-->", "", body, flags=re.S).strip()
    return cleaned


def load_cover_template() -> str:
    if not config.COVER_TEMPLATE.exists():
        return ""
    text = config.COVER_TEMPLATE.read_text(encoding="utf-8")
    _, body = split_note(text)
    # The reusable letter sits between the first and second '---' rule in the body.
    parts = body.split("\n---\n")
    return parts[1].strip() if len(parts) >= 2 else body.strip()
