"""Compile a LaTeX resume to PDF for attachment.

Resolves which resume a job should use from Targeting.resume_by_category (falling
back to Profile.default_resume), compiles the matching Profile/Resumes/<name>.tex,
and returns the PDF path. Degrades gracefully if no LaTeX engine is installed.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import config
import profile_data


def resume_name_for_category(category: str) -> str:
    profile = profile_data.load_profile()
    targeting = profile_data.load_targeting()
    mapping = targeting.get("resume_by_category") or {}
    return str(mapping.get(category) or profile.get("default_resume") or "resume")


def _engine() -> str | None:
    for eng in ("pdflatex", "xelatex", "tectonic"):
        if shutil.which(eng):
            return eng
    return None


def compile_resume(name: str, force: bool = False) -> Path | None:
    """Compile Profile/Resumes/<name>.tex -> out/resumes/<name>.pdf.

    Returns the PDF path, or None if the source/engine is missing.
    """
    tex = config.RESUMES_DIR / f"{name}.tex"
    if not tex.exists():
        print(f"[resume] source not found: {tex}", file=sys.stderr)
        return None

    config.RESUME_PDF_DIR.mkdir(parents=True, exist_ok=True)
    out_pdf = config.RESUME_PDF_DIR / f"{name}.pdf"
    if out_pdf.exists() and not force and out_pdf.stat().st_mtime >= tex.stat().st_mtime:
        return out_pdf

    engine = _engine()
    if not engine:
        print("[resume] no LaTeX engine (pdflatex/xelatex/tectonic) installed; "
              "skipping PDF compile. Attach the .tex or a manually exported PDF.",
              file=sys.stderr)
        return None

    if engine == "tectonic":
        cmd = [engine, "--outdir", str(config.RESUME_PDF_DIR), str(tex)]
        runs = 1
    else:
        cmd = [engine, "-interaction=nonstopmode", "-halt-on-error",
               "-output-directory", str(config.RESUME_PDF_DIR), str(tex)]
        runs = 2  # second pass resolves refs/layout

    for _ in range(runs):
        proc = subprocess.run(cmd, capture_output=True, text=True)
    if not out_pdf.exists():
        tail = (proc.stdout or "")[-800:]
        print(f"[resume] compile failed for {name}:\n{tail}", file=sys.stderr)
        return None
    # Tidy aux files (best-effort; some mounts disallow unlink).
    for ext in (".aux", ".log", ".out"):
        try:
            (config.RESUME_PDF_DIR / f"{name}{ext}").unlink(missing_ok=True)
        except OSError:
            pass
    return out_pdf


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else resume_name_for_category("internship")
    pdf = compile_resume(name, force=True)
    print(f"Compiled: {pdf}" if pdf else "No PDF produced.")
