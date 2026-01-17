#!/usr/bin/env python3
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

import fitz  # PyMuPDF


def slugify(text: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower())
    normalized = normalized.strip("-")
    return normalized or "section"


def load_existing_config(config_path: Path) -> dict:
    if not config_path.exists():
        return {}
    try:
        return json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_config(config_path: Path, config: dict) -> None:
    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def build_sections(doc: fitz.Document, toc_entries: list, requested_level: int) -> Tuple[Optional[int], list]:
    if not toc_entries:
        return None, []

    levels = sorted({entry["level"] for entry in toc_entries})
    effective_level = requested_level if requested_level in levels else levels[0]

    sections = []
    page_count = doc.page_count

    for idx, entry in enumerate(toc_entries):
        level = entry["level"]
        if level != effective_level:
            continue
        title = entry["title"]
        start_page = max(1, min(page_count, int(entry["page"])))
        end_page = page_count
        for next_idx in range(idx + 1, len(toc_entries)):
            next_entry = toc_entries[next_idx]
            next_level = next_entry["level"]
            if next_level <= effective_level:
                end_page = max(1, min(page_count, int(next_entry["page"]) - 1))
                break
        if end_page < start_page:
            end_page = start_page
        sections.append(
            {
                "title": str(title).strip() or f"Section {len(sections) + 1}",
                "start_page": start_page,
                "end_page": end_page,
            }
        )
    return effective_level, sections


def write_sections(
    doc: fitz.Document,
    sections: list[dict],
    sections_dir: Path,
    dry_run: bool,
) -> list[dict]:
    if not sections:
        return []
    width = len(str(len(sections)))
    outputs = []
    for index, section in enumerate(sections, start=1):
        slug = slugify(section["title"])
        filename = f"{index:0{width}d}_{slug}.pdf"
        output_path = sections_dir / filename
        if not dry_run:
            new_doc = fitz.open()
            new_doc.insert_pdf(
                doc,
                from_page=section["start_page"] - 1,
                to_page=section["end_page"] - 1,
            )
            new_doc.save(output_path)
            new_doc.close()
        outputs.append(
            {
                "index": index,
                "title": section["title"],
                "slug": slug,
                "start_page": section["start_page"],
                "end_page": section["end_page"],
                "output_pdf": str(output_path),
            }
        )
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Split a PDF into sections using its TOC.")
    parser.add_argument("--pdf", required=True, help="Path to the PDF to split.")
    parser.add_argument("--toc-level", type=int, default=1, help="TOC level to split on (default: 1).")
    parser.add_argument("--out-dir", help="Output directory (default: <pdf-stem>__out).")
    parser.add_argument("--dry-run", action="store_true", help="Inspect TOC and ranges without writing PDFs.")
    args = parser.parse_args()

    pdf_path = Path(args.pdf).expanduser().resolve()
    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}", file=sys.stderr)
        return 1

    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else pdf_path.parent / f"{pdf_path.stem}__out"
    sections_dir = out_dir / "sections"
    if not args.dry_run:
        sections_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    toc = doc.get_toc()
    toc_entries = [{"level": t[0], "title": t[1], "page": t[2]} for t in toc]

    if not toc_entries:
        print("No TOC detected; falling back to full PDF.")
        sections = [
            {
                "title": pdf_path.stem,
                "start_page": 1,
                "end_page": doc.page_count,
            }
        ]
        effective_level = None
    else:
        effective_level, sections = build_sections(doc, toc_entries, args.toc_level)
        print(f"TOC entries: {len(toc_entries)}. Using level {effective_level} for splitting.")

    outputs = write_sections(doc, sections, sections_dir, args.dry_run)
    if outputs:
        for output in outputs:
            print(
                f"[{output['index']}] {output['title']} "
                f"(pages {output['start_page']}-{output['end_page']}) -> {output['output_pdf']}"
            )

    config_path = out_dir / "config.json"
    existing_config = load_existing_config(config_path)
    config = {
        "source_pdf": str(pdf_path),
        "source_name": pdf_path.name,
        "page_count": doc.page_count,
        "toc_found": bool(toc_entries),
        "toc_level_requested": args.toc_level,
        "toc_level_used": effective_level,
        "toc": toc_entries,
        "sections": outputs,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "notes": existing_config.get("notes", ""),
    }
    for key in ("parse_runs", "parser_runs"):
        if key in existing_config:
            config[key] = existing_config[key]
    if not args.dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)
        save_config(config_path, config)
        print(f"Wrote config: {config_path}")

    doc.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
