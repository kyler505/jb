"""Self-healing Q&A store.

When the apply step meets a question it can't answer from the Profile or the
existing Q&A bank, it asks the user once, then records the answer here so the
question is answered automatically next time.

  find_answer(question)  -> QAEntry | None   (high-confidence match only)
  record_answer(q, a)    -> Path             (creates/updates a Profile/QA note)

Storage format matches the existing bank: Profile/QA/<slug>.md with frontmatter
{type, question, keywords, category, source, recorded} and the answer as the body.
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import config
import profile_data
from profile_data import QAEntry

_STOPWORDS = {
    "the", "a", "an", "and", "or", "to", "of", "in", "on", "for", "with", "is",
    "are", "do", "you", "your", "we", "our", "us", "at", "this", "that", "have",
    "has", "any", "be", "will", "would", "can", "could", "what", "why", "how",
    "when", "where", "which", "who", "if", "as", "it", "i", "me", "my", "about",
    "please", "tell", "describe", "ever", "their", "them", "there",
}


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", " ", text.lower())


def _tokens(text: str) -> set[str]:
    return {w for w in _normalize(text).split() if w and w not in _STOPWORDS}


def _slug(question: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", question.lower()).strip("-")
    return (s or "question")[:60]


def _derive_keywords(question: str, extra: list[str] | None = None) -> list[str]:
    kws = list(dict.fromkeys(list(_tokens(question)) + [w.lower() for w in (extra or [])]))
    # Always include a compact form of the full question for exact recall.
    full = _normalize(question).strip()
    if full and full not in kws:
        kws.append(full)
    return kws


def find_answer(question: str, threshold: float = 0.6) -> QAEntry | None:
    """Return the best-matching answered Q&A entry, or None if low confidence.

    Scores by token overlap (Jaccard) against each entry's question + keywords,
    and treats a stored keyword appearing verbatim in the question as a strong hit.
    """
    q_tokens = _tokens(question)
    q_norm = _normalize(question)
    if not q_tokens:
        return None

    best: tuple[float, QAEntry] | None = None
    for entry in profile_data.load_qa_bank():
        if not entry.answer:
            continue
        entry_tokens = _tokens(entry.question) | {t for kw in entry.keywords for t in _tokens(kw)}
        if not entry_tokens:
            continue
        overlap = q_tokens & entry_tokens
        jaccard = len(overlap) / len(q_tokens | entry_tokens)
        score = jaccard
        # Strong signal: a stored keyword phrase appears in the question.
        for kw in entry.keywords:
            kw_norm = _normalize(kw).strip()
            if len(kw_norm) >= 4 and kw_norm in q_norm:
                score = max(score, 0.75)
        if best is None or score > best[0]:
            best = (score, entry)

    if best and best[0] >= threshold:
        return best[1]
    return None


def record_answer(question: str, answer: str, *, keywords: list[str] | None = None,
                  category: str = "learned") -> Path:
    """Create or update a Profile/QA note capturing a user-provided answer."""
    config.QA_DIR.mkdir(parents=True, exist_ok=True)

    # Reuse an existing note for the same question if one matches strongly.
    existing = find_answer(question, threshold=0.85)
    if existing:
        path = config.QA_DIR / existing.source
    else:
        path = config.QA_DIR / f"{_slug(question)}.md"
        n = 1
        while path.exists():
            path = config.QA_DIR / f"{_slug(question)}-{n}.md"
            n += 1

    kw_lines = "\n".join(f"  - {k}" for k in _derive_keywords(question, keywords))
    q_escaped = question.replace('"', '\\"')
    content = (
        "---\n"
        "type: qa\n"
        f'question: "{q_escaped}"\n'
        "keywords:\n"
        f"{kw_lines}\n"
        f"category: {category}\n"
        "source: self-heal\n"
        f"recorded: {date.today().isoformat()}\n"
        "---\n\n"
        f"{answer.strip()}\n"
    )
    path.write_text(content, encoding="utf-8")
    return path


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 3 and sys.argv[1] == "find":
        hit = find_answer(" ".join(sys.argv[2:]))
        print(f"MATCH: {hit.question}\n\n{hit.answer}" if hit else "No confident match.")
    elif len(sys.argv) >= 4 and sys.argv[1] == "record":
        p = record_answer(sys.argv[2], sys.argv[3])
        print(f"Recorded -> {p}")
    else:
        print('Usage: qa_store.py find "<question>" | record "<question>" "<answer>"')
