# PDF TOC splitting and Gemini Markdown parsing

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must be kept up to date as work proceeds. Maintain this plan in accordance with `.agent/PLANS.md` at the repository root.

## Purpose / Big Picture

Enable two Python tools in this repository so PDFs can be split into chapter PDFs based on the PDF table of contents (TOC), and then converted into high-quality Markdown using Gemini with bilingual pairing, LaTeX equations, and image crops with bounding box references. The user-visible outcome is: run a splitter on the Barrat network dynamics PDF to produce chapter PDFs, then run a parser on each chapter (and on the Tamil textbook) to generate Markdown plus cropped images, all stored in an output folder adjacent to the source PDF with a config/manifest file describing the run.

## Progress

- [x] (2026-01-09 02:28Z) Captured requirements and created this ExecPlan for the PDF splitting and Gemini parsing pipeline.
- [x] (2026-01-09 02:35Z) Implemented `tools/pdf_split.py` with TOC-based section output and config manifest writing.
- [x] (2026-01-09 02:35Z) Implemented `tools/pdf_parse.py` plus prompt templates for page and tiled parsing.
- [ ] Validate on the Barrat network dynamics PDF and the Tamil textbook, iterating prompts as needed.

## Surprises & Discoveries

No discoveries yet; implementation has not started.

## Decision Log

- Decision: Output folders will live in the same directory as the input PDF using a stable suffix (`<pdf-stem>__out`), and include a `config.json` manifest at the root.  
  Rationale: Keeps outputs colocated with inputs without name collisions, and makes it easy to track provenance.  
  Date/Author: 2026-01-09 / Codex
- Decision: Multi-language text will be emitted in a tagged pair format with a start tag, end tag, and a clear separator line.  
  Rationale: The user requested tags and a separator, and a fixed format makes downstream parsing reliable.  
  Date/Author: 2026-01-09 / Codex
- Decision: Image crops will be derived from Gemini-provided bounding boxes on the rendered page images, and Markdown will reference the crop while also storing the source image path and bbox in a tag.  
  Rationale: Meets the requirement to use Gemini for image understanding and to include bbox references to the original image.  
  Date/Author: 2026-01-09 / Codex
- Decision: Normalize bounding boxes in `[ymin, xmin, ymax, xmax]` order with 0-1000 coordinates, and store that order in `bbox_order` metadata.  
  Rationale: Matches Gemini object detection conventions and supports deterministic conversion to pixel crops.  
  Date/Author: 2026-01-09 / Codex
- Decision: Insert image placeholders `[[IMAGE:label]]` in Gemini Markdown outputs and replace them with `<IMAGE ...>` blocks during post-processing.  
  Rationale: Keeps image placement anchored to the page text while ensuring consistent metadata injection.  
  Date/Author: 2026-01-09 / Codex

## Outcomes & Retrospective

Pending implementation.

## Context and Orientation

The repository is a PDF library. The target PDFs for initial validation are:
1) `0X-lobia-texts/Learn Tamil in 30 Days.pdf` (bilingual Tamil/English textbook for parsing).
2) `02-Network-Science/Network-Dynamics/Dynamical-Processes-on-Complex-Networks-Barrat-et-al-2008.pdf` (network dynamics textbook for TOC splitting and per-chapter parsing).

Definitions used in this plan:
- TOC (table of contents): The PDF outline entries returned by PyMuPDF `doc.get_toc()`, each entry being `[level, title, page]` with page numbers starting at 1.
- Bounding box (bbox): A rectangle in pixel coordinates on a rendered page image, represented as `[x0, y0, x1, y1]` where `(x0, y0)` is the top-left and `(x1, y1)` is the bottom-right.
- Tiled image: A single composite image created by stacking multiple rendered pages vertically, with a separator line and page labels between pages to help Gemini split output by page.

No dedicated tools exist yet for this pipeline. New Python scripts and prompt templates will be added under a `tools/` directory at the repository root.

## Plan of Work

Create two CLI tools:

1) `tools/pdf_split.py` for TOC-based splitting. It must:
   - Load a PDF via PyMuPDF (`fitz`), inspect `doc.get_toc()`, and report whether a TOC exists.
   - Select TOC entries for a requested level (default `1`, chapter level). If no entries exist at that level, fall back to the smallest level present in the TOC.
   - Compute page ranges so each section starts at a TOC entry page and ends at the page before the next entry at the same or higher hierarchy level.
   - Write each section as a new PDF in `sections/`, with a stable index prefix and a slug of the title.
   - Emit `config.json` at the output root containing the source PDF name/path, page count, TOC entries, and a `sections` array with title, start/end pages, and output file names.
   - If no TOC exists, emit a single `sections/00_full.pdf` and note the fallback in `config.json`.

2) `tools/pdf_parse.py` for Gemini-based parsing. It must:
   - Accept either a PDF file or a directory of section PDFs.
   - Render each page to PNG using PyMuPDF at a configurable DPI (default 200). Store full-page images in `images/`.
   - Optionally combine multiple page images into a tiled image (`--tile-pages N`), inserting a horizontal separator line and a page label between pages to enforce a parse boundary.
   - Call the Gemini API (using `google-genai`) with the appropriate prompt template for page or tiled mode.
   - Parse the model output into Markdown, converting equations to Jupyter-friendly LaTeX: inline `$...$` and block `$$...$$`.
   - When bilingual content appears, wrap each paired segment using the required tag format:
     - Start tag: `<PAIR lang1="xx" lang2="yy">`
     - Separator line: `--||--`
     - End tag: `</PAIR>`
     - Example layout (lines are literal):
       `<PAIR lang1="ta" lang2="en">`
       `Tamil text line(s)...`
       `--||--`
       `English text line(s)...`
       `</PAIR>`
   - When images appear on a page, request Gemini to return bounding boxes (normalized 0-1000 or pixel-based, but choose one and document it) and labels. Convert bboxes to pixel coordinates, crop the rendered page image using Pillow, and save crops in `crops/`.
   - In the Markdown output, insert an image block that references the crop and preserves the original source and bbox:
     - `<IMAGE source="images/page_003.png" bbox="120,88,450,300">`
     - `![page_003_img_02](crops/page_003_img_02.png)`
     - `</IMAGE>`
   - Write a per-page Markdown file and an aggregated Markdown file for the PDF/section. Update `config.json` with parse outputs, model, prompts, and run settings.

Prompt templates should be stored in `tools/prompts/` with separate files for page mode and tiled mode. Prompts must explicitly instruct Gemini to:
   - Preserve reading order.
   - Output equations as LaTeX (`$...$` and `$$...$$`).
   - Detect bilingual content and label languages using ISO 639-1 codes.
   - Provide image bounding boxes and labels in the agreed format.

## Concrete Steps

Work from `/Users/natkite/Documents/2025/netsi25/PhD/phd-dev/SelfStudy`.

1) Inventory PDFs and confirm target paths:
   - `ls "0X-lobia-texts"`
   - `ls "02-Network-Science/Network-Dynamics"`

2) Create the tooling layout:
   - `mkdir -p tools/prompts`
   - `touch tools/pdf_split.py tools/pdf_parse.py tools/prompts/page_prompt.txt tools/prompts/tile_prompt.txt`

3) Implement `tools/pdf_split.py`:
   - Add CLI args: `--pdf`, `--toc-level`, `--out-dir`, `--dry-run`.
   - Build a `config.json` manifest and emit section PDFs.
   - Log TOC detection and each section range to stdout.

4) Implement `tools/pdf_parse.py`:
   - Add CLI args: `--pdf`, `--sections-dir`, `--out-dir`, `--dpi`, `--tile-pages`, `--model`, `--prompt`.
   - Render pages to PNG and (optionally) create tiles with separators.
   - Call Gemini, parse output, crop images, and write Markdown outputs + manifest updates.
   - Load `GEMINI_API_KEY` from `.env` using `python-dotenv` if available; fall back to environment variables if not.

5) Define prompt templates:
   - `tools/prompts/page_prompt.txt` for single-page parse.
   - `tools/prompts/tile_prompt.txt` for multi-page tiled parse with required page separators.

6) Validate splitting on Barrat PDF:
   - `python tools/pdf_split.py --pdf "02-Network-Science/Network-Dynamics/Dynamical-Processes-on-Complex-Networks-Barrat-et-al-2008.pdf"`
   - Inspect `.../__out/config.json` and `.../__out/sections/*.pdf` to confirm chapter boundaries.

7) Validate parsing:
   - Tamil textbook:
     - `python tools/pdf_parse.py --pdf "0X-lobia-texts/Learn Tamil in 30 Days.pdf" --dpi 200`
   - Barrat chapters:
     - `python tools/pdf_parse.py --sections-dir "02-Network-Science/Network-Dynamics/Dynamical-Processes-on-Complex-Networks-Barrat-et-al-2008__out/sections" --dpi 200`

8) Iterate prompts based on output quality, update `config.json` with prompt version, and rerun until the Markdown, equations, bilingual pairs, and image crops look correct.

## Validation and Acceptance

The work is accepted when:
- Running the splitter on the Barrat PDF produces a `__out` folder next to the PDF with `config.json` and individual chapter PDFs in `sections/`.
- Running the parser on the Tamil PDF produces Markdown with bilingual pairs in the specified `<PAIR ...>` format and proper LaTeX equations.
- Images in the Markdown have corresponding crop files in `crops/` and an `<IMAGE ...>` tag containing the source image path and bbox.
- The parser logs and config show the Gemini model used and the prompt file name for traceability.
- Manual spot checks confirm that the extracted text is in reading order and equations are formatted for Jupyter Markdown.

## Idempotence and Recovery

Both tools should overwrite only their own output folders. Re-running them on the same PDF should recreate the same directory and refresh `config.json` and derived artifacts. If a run fails midway, rerun the command after fixing prompts or parameters; the scripts should safely overwrite their own outputs without modifying the source PDFs.

## Artifacts and Notes

Capture small snippets of:
- The TOC detection log for the Barrat PDF.
- One bilingual Markdown sample from the Tamil PDF.
- One `<IMAGE ...>` block showing a cropped figure with bbox.

Store these snippets in the `config.json` notes field or a short `run.log` file in the output folder so future runs can compare quality.

## Interfaces and Dependencies

Dependencies (Python):
- PyMuPDF (`fitz`) for PDF parsing and rendering.
- Pillow (`PIL`) for image tiling and cropping.
- google-genai for Gemini API calls.
- python-dotenv for loading `.env`.

Tool interfaces:
- `tools/pdf_split.py`:
  - Inputs: `--pdf` path; optional `--toc-level`, `--out-dir`.
  - Output: `<pdf-dir>/<pdf-stem>__out/config.json`, `<pdf-dir>/<pdf-stem>__out/sections/*.pdf`.
- `tools/pdf_parse.py`:
  - Inputs: `--pdf` or `--sections-dir`, optional `--dpi`, `--tile-pages`, `--model`, `--prompt`.
  - Output: `<pdf-dir>/<pdf-stem>__out/images/*.png`, `<pdf-dir>/<pdf-stem>__out/crops/*.png`, `<pdf-dir>/<pdf-stem>__out/markdown/*.md`, and updates to `config.json`.

Gemini API usage requires network access. When running the parser, request approval for network access if the sandbox blocks outbound requests. The API key should be provided via `.env` as `GEMINI_API_KEY` or via the environment.
