"""Orchestrate a daily prep run: select -> rank -> compile resume -> prepare.

This produces the daily queue and writes a review-ready application packet into
each queued job note. It NEVER submits an application — submission is the
human-in-the-loop step driven by Claude in Chrome (see WORKFLOW.md).

Usage:
    python run.py            # full daily cap from Targeting.md
    python run.py --limit 5  # only prepare the top 5 (handy for a pilot)
    python run.py --select-only
"""
from __future__ import annotations

import argparse

import config
import prepare
import selector


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None,
                    help="cap how many top jobs to prepare this run")
    ap.add_argument("--select-only", action="store_true",
                    help="build the queue but skip preparing packets")
    ap.add_argument("--no-priority-write", action="store_true",
                    help="don't write priority back to notes (faster, read-only)")
    args = ap.parse_args()

    queue = selector.build_queue(write_priority=not args.no_priority_write)
    print(f"[select] {len(queue)} jobs queued -> {config.QUEUE_MD}")

    if args.select_only:
        return

    results = prepare.prepare_queue(limit=args.limit)
    flagged = sum(1 for r in results if r["unresolved"])
    print(f"[prepare] {len(results)} packets written; {flagged} need placeholder review.")
    print(f"\nNext: open the 'By Priority' / 'Needs Review' views in Obsidian, or run "
          f"the Cowork 'Apply' workflow to prefill + review each form in the browser.")


if __name__ == "__main__":
    main()
