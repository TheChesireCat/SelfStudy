#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont

try:
    from google import genai
    from google.genai import types
    from google.genai import errors as genai_errors
except ImportError:  # pragma: no cover - runtime dependency
    genai = None
    types = None
    genai_errors = None
try:
    from tqdm import tqdm
except ImportError:  # pragma: no cover - optional dependency
    tqdm = None


INLINE_SIZE_LIMIT = 18 * 1024 * 1024
BBOX_ORDER = "ymin,xmin,ymax,xmax"
RATE_LIMIT_RETRIES = 3


def slugify(text: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower())
    normalized = normalized.strip("-")
    return normalized or "section"


def load_dotenv_if_available() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv()


def load_api_key(explicit_key: Optional[str]) -> Optional[str]:
    if explicit_key:
        return explicit_key
    load_dotenv_if_available()
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def ensure_genai() -> None:
    if genai is None or types is None:
        print("Missing google-genai. Install with: pip install google-genai", file=sys.stderr)
        raise SystemExit(1)


class GeminiRateLimitError(RuntimeError):
    pass


def progress_iter(iterable: Any, desc: Optional[str] = None, unit: Optional[str] = None) -> Any:
    if tqdm is None:
        return iterable
    kwargs: Dict[str, Any] = {}
    if desc:
        kwargs["desc"] = desc
    if unit:
        kwargs["unit"] = unit
    return tqdm(iterable, **kwargs)


def extract_retry_delay(details: Any) -> Optional[float]:
    if not isinstance(details, dict):
        return None
    error = details.get("error", details)
    if not isinstance(error, dict):
        return None
    for item in error.get("details", []):
        if not isinstance(item, dict):
            continue
        retry = item.get("retryDelay")
        if isinstance(retry, str) and retry.endswith("s"):
            try:
                return float(retry[:-1])
            except ValueError:
                return None
    return None


def extract_quota_id(details: Any) -> Optional[str]:
    if not isinstance(details, dict):
        return None
    error = details.get("error", details)
    if not isinstance(error, dict):
        return None
    for item in error.get("details", []):
        if not isinstance(item, dict):
            continue
        if item.get("@type") != "type.googleapis.com/google.rpc.QuotaFailure":
            continue
        for violation in item.get("violations", []):
            if not isinstance(violation, dict):
                continue
            quota_id = violation.get("quotaId") or violation.get("quotaMetric")
            if isinstance(quota_id, str):
                return quota_id
    return None


def is_daily_quota(details: Any) -> bool:
    quota_id = extract_quota_id(details) or ""
    return "perday" in quota_id.lower()


def parse_json_payload(text: str) -> Any:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    for open_char, close_char in (("{", "}"), ("[", "]")):
        start = cleaned.find(open_char)
        end = cleaned.rfind(close_char)
        if start != -1 and end != -1 and end > start:
            candidate = cleaned[start : end + 1]
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                continue
    return json.loads(cleaned)


def load_prompt(prompt_path: Path, **kwargs: str) -> str:
    template = prompt_path.read_text(encoding="utf-8")
    return template.format(**kwargs)


def normalize_bbox(bbox: List[float], width: int, height: int) -> Tuple[int, int, int, int]:
    ymin, xmin, ymax, xmax = bbox
    x0 = int(max(0, min(width, xmin / 1000.0 * width)))
    y0 = int(max(0, min(height, ymin / 1000.0 * height)))
    x1 = int(max(0, min(width, xmax / 1000.0 * width)))
    y1 = int(max(0, min(height, ymax / 1000.0 * height)))
    if x1 <= x0:
        x1 = min(width, x0 + 1)
    if y1 <= y0:
        y1 = min(height, y0 + 1)
    return x0, y0, x1, y1


def render_pages(doc: fitz.Document, images_dir: Path, dpi: int, force: bool) -> List[Path]:
    images_dir.mkdir(parents=True, exist_ok=True)
    scale = dpi / 72.0
    matrix = fitz.Matrix(scale, scale)
    image_paths: List[Path] = []
    for index in progress_iter(range(doc.page_count), desc="Rendering pages", unit="page"):
        filename = f"page_{index + 1:03d}.png"
        out_path = images_dir / filename
        if not force and out_path.exists() and out_path.stat().st_size > 0:
            image_paths.append(out_path)
            continue
        page = doc.load_page(index)
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        pix.save(out_path)
        image_paths.append(out_path)
    return image_paths


def build_tile_image(
    page_image_paths: List[Path],
    page_numbers: List[int],
    out_path: Path,
) -> Path:
    images: List[Image.Image] = []
    for path in page_image_paths:
        images.append(Image.open(path).convert("RGB"))

    width = max(img.width for img in images)
    band_height = 40
    total_height = sum(img.height + band_height for img in images)
    tile = Image.new("RGB", (width, total_height), (255, 255, 255))
    draw = ImageDraw.Draw(tile)
    font = ImageFont.load_default()

    cursor = 0
    for img, page_no in zip(images, page_numbers):
        draw.rectangle([0, cursor, width, cursor + band_height], fill=(245, 245, 245))
        label = f"=== PAGE {page_no:03d} ==="
        draw.text((10, cursor + 12), label, fill=(0, 0, 0), font=font)
        cursor += band_height
        offset_x = (width - img.width) // 2
        tile.paste(img, (offset_x, cursor))
        cursor += img.height

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tile.save(out_path)
    for img in images:
        img.close()
    return out_path


def build_contents(client: "genai.Client", image_path: Path, prompt: str) -> List[Any]:
    mime_type = "image/png"
    if image_path.stat().st_size > INLINE_SIZE_LIMIT:
        uploaded = client.files.upload(file=str(image_path), config={"mimeType": mime_type})
        return [uploaded, prompt]
    with image_path.open("rb") as handle:
        data = handle.read()
    return [types.Part.from_bytes(data=data, mime_type=mime_type), prompt]


def call_gemini(
    client: "genai.Client",
    model: str,
    image_path: Path,
    prompt: str,
    return_raw: bool = False,
) -> Any:
    config = types.GenerateContentConfig(response_mime_type="application/json", temperature=0)
    contents = build_contents(client, image_path, prompt)
    attempts = 0
    while True:
        try:
            response = client.models.generate_content(model=model, contents=contents, config=config)
            break
        except Exception as exc:
            if genai_errors is None or not isinstance(exc, genai_errors.ClientError):
                raise
            if exc.code != 429:
                raise
            details = exc.details
            if is_daily_quota(details):
                quota_id = extract_quota_id(details) or "daily quota"
                raise GeminiRateLimitError(
                    f"Gemini quota exceeded ({quota_id}). Wait for reset or use a billed key/project."
                ) from exc
            if attempts >= RATE_LIMIT_RETRIES:
                raise GeminiRateLimitError("Gemini rate limit exceeded. Try again later.") from exc
            retry_delay = extract_retry_delay(details)
            sleep_for = max(1.0, retry_delay or (2 ** attempts))
            print(f"Rate limit hit; retrying in {sleep_for:.1f}s...", file=sys.stderr)
            time.sleep(sleep_for)
            attempts += 1
    if not response or not response.text:
        raise RuntimeError("Gemini returned an empty response.")
    parsed = parse_json_payload(response.text)
    if return_raw:
        return parsed, response.text
    return parsed


def coerce_page_response(response: Any) -> Tuple[str, List[Dict[str, Any]]]:
    if isinstance(response, dict):
        markdown = str(response.get("markdown") or response.get("content") or "").strip()
        images = response.get("images") or response.get("figures") or []
        return markdown, images
    return str(response).strip(), []


def extract_tile_pages(response: Any, chunk_numbers: List[int]) -> List[Dict[str, Any]]:
    pages: Optional[List[Any]] = None
    if isinstance(response, list):
        pages = response
    elif isinstance(response, dict):
        if isinstance(response.get("pages"), list):
            pages = response.get("pages")
        elif all(key in response for key in ("page", "markdown")):
            pages = [response]
        elif isinstance(response.get("data"), list):
            pages = response.get("data")
        elif isinstance(response.get("results"), list):
            pages = response.get("results")
        else:
            numeric_keys = []
            for key in response:
                key_str = str(key)
                if key_str.isdigit():
                    numeric_keys.append(int(key_str))
            if numeric_keys:
                pages = []
                for key in sorted(numeric_keys):
                    item = response.get(str(key)) or response.get(key)
                    if isinstance(item, dict):
                        item = dict(item)
                        item.setdefault("page", key)
                        pages.append(item)
    if not pages:
        return []
    normalized: List[Dict[str, Any]] = []
    for idx, page_item in enumerate(pages):
        if not isinstance(page_item, dict):
            continue
        page_no_raw = (
            page_item.get("page")
            or page_item.get("page_number")
            or page_item.get("pageNo")
            or page_item.get("page_index")
        )
        if page_no_raw is None:
            if idx < len(chunk_numbers):
                page_no = chunk_numbers[idx]
            else:
                continue
        else:
            try:
                page_no = int(str(page_no_raw))
            except ValueError:
                continue
        markdown, images = coerce_page_response(page_item)
        normalized.append({"page": page_no, "markdown": markdown, "images": images})
    return normalized


def insert_image_blocks(
    markdown: str,
    images: List[Dict[str, Any]],
    page_image_path: Path,
    crops_dir: Path,
    markdown_path: Path,
) -> Tuple[str, List[Dict[str, Any]]]:
    crops_dir.mkdir(parents=True, exist_ok=True)
    page_image = Image.open(page_image_path).convert("RGB")
    width, height = page_image.size
    results: List[Dict[str, Any]] = []

    for idx, item in enumerate(images, start=1):
        label = str(item.get("label") or f"img_{idx:02d}")
        bbox_norm = item.get("bbox_norm") or item.get("bbox") or []
        if len(bbox_norm) != 4:
            continue
        x0, y0, x1, y1 = normalize_bbox([float(v) for v in bbox_norm], width, height)
        crop = page_image.crop((x0, y0, x1, y1))
        crop_name = f"{page_image_path.stem}_img_{idx:02d}.png"
        crop_path = crops_dir / crop_name
        crop.save(crop_path)

        source_rel = os.path.relpath(page_image_path, markdown_path.parent)
        crop_rel = os.path.relpath(crop_path, markdown_path.parent)
        bbox_str = ",".join(str(int(v)) for v in bbox_norm)
        image_block = (
            f'<IMAGE source="{source_rel}" bbox="{bbox_str}">\n'
            f"![{label}]({crop_rel})\n"
            f"</IMAGE>"
        )

        placeholder = f"[[IMAGE:{label}]]"
        if placeholder in markdown:
            markdown = markdown.replace(placeholder, image_block)
        else:
            markdown = f"{markdown}\n\n{image_block}"
        results.append(
            {
                "label": label,
                "bbox_norm": bbox_norm,
                "bbox_order": BBOX_ORDER,
                "crop_path": str(crop_path),
            }
        )

    page_image.close()
    return markdown.strip() + "\n", results


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_config(config_path: Path) -> Dict[str, Any]:
    if not config_path.exists():
        return {}
    try:
        return json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_config(config_path: Path, config: Dict[str, Any]) -> None:
    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


IMAGE_BLOCK_RE = re.compile(
    r'<IMAGE\s+source="([^"]+)"\s+bbox="([^"]+)"\s*>\s*'
    r'!\[([^\]]*)\]\(([^)]+)\)\s*</IMAGE>',
    re.IGNORECASE,
)


def load_existing_markdown(page_md_path: Path) -> Optional[str]:
    if not page_md_path.exists():
        return None
    content = page_md_path.read_text(encoding="utf-8").strip()
    return content or None


def extract_image_records_from_markdown(markdown: str, markdown_path: Path) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for match in IMAGE_BLOCK_RE.finditer(markdown):
        bbox_raw = match.group(2)
        label = match.group(3) or "img"
        crop_rel = match.group(4)
        bbox_values: List[float] = []
        for item in bbox_raw.split(","):
            item = item.strip()
            if not item:
                continue
            try:
                bbox_values.append(float(item))
            except ValueError:
                bbox_values = []
                break
        if len(bbox_values) != 4:
            continue
        crop_path = markdown_path.parent / crop_rel
        results.append(
            {
                "label": label,
                "bbox_norm": bbox_values,
                "bbox_order": BBOX_ORDER,
                "crop_path": str(crop_path),
            }
        )
    return results

def process_pdf(
    client: "genai.Client",
    pdf_path: Path,
    out_dir: Path,
    dpi: int,
    tile_pages: int,
    model: str,
    prompt_path: Path,
    force: bool,
) -> Dict[str, Any]:
    section_name = pdf_path.stem
    images_dir = out_dir / "images" / section_name
    crops_dir = out_dir / "crops" / section_name
    markdown_dir = out_dir / "markdown"
    pages_dir = markdown_dir / "pages"
    tiles_dir = out_dir / "tiles" / section_name
    ensure_dir(markdown_dir)
    ensure_dir(pages_dir)

    doc = fitz.open(pdf_path)
    page_count = doc.page_count
    page_image_paths = render_pages(doc, images_dir, dpi, force)

    per_page_markdown: Dict[int, str] = {}
    image_records: Dict[int, List[Dict[str, Any]]] = {}
    if not force:
        for page_no in range(1, page_count + 1):
            page_md_path = pages_dir / f"{section_name}_page_{page_no:03d}.md"
            existing_markdown = load_existing_markdown(page_md_path)
            if not existing_markdown:
                continue
            per_page_markdown[page_no] = existing_markdown.strip()
            image_records[page_no] = extract_image_records_from_markdown(existing_markdown, page_md_path)

    if tile_pages > 1:
        for start in progress_iter(range(0, page_count, tile_pages), desc="Parsing tiles", unit="tile"):
            end = min(page_count, start + tile_pages)
            chunk_paths = page_image_paths[start:end]
            chunk_numbers = list(range(start + 1, end + 1))
            missing_pages = [page_no for page_no in chunk_numbers if page_no not in per_page_markdown]
            if not missing_pages and not force:
                continue
            tile_name = f"tile_{chunk_numbers[0]:03d}_{chunk_numbers[-1]:03d}.png"
            tile_path = tiles_dir / tile_name
            if force or not tile_path.exists():
                build_tile_image(chunk_paths, chunk_numbers, tile_path)
            prompt = load_prompt(
                prompt_path,
                page_numbers=",".join(f"{n:03d}" for n in chunk_numbers),
                bbox_order=BBOX_ORDER,
            )
            response, raw_text = call_gemini(client, model, tile_path, prompt, return_raw=True)
            pages = extract_tile_pages(response, chunk_numbers)
            if not pages:
                snippet = raw_text.strip().replace("\n", " ")
                if len(snippet) > 400:
                    snippet = snippet[:400] + "..."
                raise RuntimeError(f"Tile response missing 'pages' list. Raw snippet: {snippet}")
            for page_item in pages:
                page_no_raw = page_item.get("page")
                if page_no_raw is None:
                    print("Skipping tile entry without page number.", file=sys.stderr)
                    continue
                page_no = int(page_no_raw)
                if page_no < 1 or page_no > page_count:
                    print(f"Skipping out-of-range page number: {page_no}", file=sys.stderr)
                    continue
                if not force and page_no in per_page_markdown:
                    continue
                markdown, images = coerce_page_response(page_item)
                page_md_path = pages_dir / f"{section_name}_page_{page_no:03d}.md"
                markdown, crops = insert_image_blocks(
                    markdown, images, page_image_paths[page_no - 1], crops_dir, page_md_path
                )
                page_md_path.write_text(markdown, encoding="utf-8")
                per_page_markdown[page_no] = markdown
                image_records[page_no] = crops
    else:
        for page_index in progress_iter(range(page_count), desc="Parsing pages", unit="page"):
            page_no = page_index + 1
            image_path = page_image_paths[page_index]
            if not force and page_no in per_page_markdown:
                continue
            prompt = load_prompt(
                prompt_path,
                page_number=f"{page_no:03d}",
                bbox_order=BBOX_ORDER,
            )
            response = call_gemini(client, model, image_path, prompt)
            markdown, images = coerce_page_response(response)
            page_md_path = pages_dir / f"{section_name}_page_{page_no:03d}.md"
            markdown, crops = insert_image_blocks(markdown, images, image_path, crops_dir, page_md_path)
            page_md_path.write_text(markdown, encoding="utf-8")
            per_page_markdown[page_no] = markdown
            image_records[page_no] = crops

    combined_md_path = markdown_dir / f"{section_name}.md"
    combined = "\n\n".join(per_page_markdown[k].strip() for k in sorted(per_page_markdown))
    combined_md_path.write_text(combined + "\n", encoding="utf-8")

    doc.close()
    return {
        "section": section_name,
        "source_pdf": str(pdf_path),
        "pages": page_count,
        "images_dir": str(images_dir),
        "crops_dir": str(crops_dir),
        "markdown": str(combined_md_path),
        "page_markdown_dir": str(pages_dir),
        "tile_pages": tile_pages,
        "bbox_order": BBOX_ORDER,
        "image_records": image_records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse PDFs into Markdown using Gemini.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pdf", help="Path to a PDF to parse.")
    group.add_argument("--sections-dir", help="Directory containing section PDFs to parse.")
    parser.add_argument("--out-dir", help="Output directory (default: <pdf-stem>__out).")
    parser.add_argument("--dpi", type=int, default=200, help="DPI for rendering (default: 200).")
    parser.add_argument("--tile-pages", type=int, default=1, help="Number of pages per tiled image.")
    parser.add_argument("--model", default="gemini-2.5-flash", help="Gemini model name.")
    parser.add_argument("--prompt", help="Path to prompt template.")
    parser.add_argument("--api-key", help="Gemini API key override.")
    parser.add_argument("--force", action="store_true", help="Re-parse even if outputs exist.")
    args = parser.parse_args()

    if args.tile_pages < 1:
        print("--tile-pages must be >= 1", file=sys.stderr)
        return 1
    if args.dpi <= 0:
        print("--dpi must be > 0", file=sys.stderr)
        return 1

    if tqdm is None:
        print("tqdm not installed; progress bars disabled. Install with: pip install tqdm", file=sys.stderr)

    ensure_genai()
    api_key = load_api_key(args.api_key)
    if not api_key:
        print("GEMINI_API_KEY is required (set in .env or environment).", file=sys.stderr)
        return 1

    client = genai.Client(api_key=api_key)
    pdf_paths: List[Path] = []

    if args.pdf:
        pdf_path = Path(args.pdf).expanduser().resolve()
        if not pdf_path.exists():
            print(f"PDF not found: {pdf_path}", file=sys.stderr)
            return 1
        pdf_paths = [pdf_path]
        out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else pdf_path.parent / f"{pdf_path.stem}__out"
    else:
        sections_dir = Path(args.sections_dir).expanduser().resolve()
        if not sections_dir.exists():
            print(f"Sections directory not found: {sections_dir}", file=sys.stderr)
            return 1
        pdf_paths = sorted(sections_dir.glob("*.pdf"))
        if not pdf_paths:
            print(f"No PDFs found in {sections_dir}", file=sys.stderr)
            return 1
        out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else sections_dir.parent

    ensure_dir(out_dir)
    config_path = out_dir / "config.json"
    config = load_config(config_path)
    parse_runs = config.get("parse_runs", [])

    prompt_path = Path(args.prompt).expanduser().resolve() if args.prompt else None
    if prompt_path is None:
        prompt_path = (
            Path(__file__).parent / "prompts" / ("tile_prompt.txt" if args.tile_pages > 1 else "page_prompt.txt")
        )
    if not prompt_path.exists():
        print(f"Prompt file not found: {prompt_path}", file=sys.stderr)
        return 1

    run_sections = []
    try:
        for pdf_path in pdf_paths:
            print(f"Parsing {pdf_path.name} with model {args.model}...")
            run_sections.append(
                process_pdf(
                    client=client,
                    pdf_path=pdf_path,
                    out_dir=out_dir,
                    dpi=args.dpi,
                    tile_pages=args.tile_pages,
                    model=args.model,
                    prompt_path=prompt_path,
                    force=args.force,
                )
            )
    except GeminiRateLimitError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    run_info = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "model": args.model,
        "prompt": str(prompt_path),
        "dpi": args.dpi,
        "tile_pages": args.tile_pages,
        "bbox_order": BBOX_ORDER,
        "sections": run_sections,
    }
    parse_runs.append(run_info)
    config["parse_runs"] = parse_runs
    save_config(config_path, config)
    print(f"Updated config: {config_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
