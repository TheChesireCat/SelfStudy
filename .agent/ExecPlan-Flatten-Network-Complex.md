# Flatten 02-Network-Science and 03-Complex-Systems

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must be kept up to date as work proceeds.

This document follows `.agent/PLANS.md` from the repository root and must be maintained in accordance with that file.

## Purpose / Big Picture

After this change, the `02-Network-Science/` and `03-Complex-Systems/` shelves will be easier to browse on disk because the main books will live directly in those top-level category folders instead of being split across several one-book or few-book subdirectories. The sidebar in `index.html` will also become flatter so that the library view matches the new on-disk organization.

The visible proof is straightforward: run a file listing in the repository root and observe that the PDFs for network science and complex systems now sit directly inside `02-Network-Science/` and `03-Complex-Systems/`, while `index.html` points at those flatter paths and renders those two library sections with a single list each.

## Progress

- [x] (2026-04-14 18:25Z) Read `.agent/PLANS.md`, inspected the current `02-Network-Science/` and `03-Complex-Systems/` layouts, and identified all nested files that participate in the flattening.
- [x] (2026-04-14 18:27Z) Identified secondary references that also need updates: `README.md`, `index.html`, and `.agent/ExecPlan-PDF-Gemini.md`.
- [x] (2026-04-14 18:32Z) Moved the network science PDFs and support artifacts into the flatter `02-Network-Science/` layout and removed the obsolete topic directories.
- [x] (2026-04-14 18:33Z) Moved the complex systems PDFs and support artifacts into the flatter `03-Complex-Systems/` layout and removed the obsolete topic directories.
- [x] (2026-04-14 18:35Z) Rewrote the `index.html` sidebar sections for `02-Network-Science` and `03-Complex-Systems` as flat file lists that point at the new root-level paths.
- [x] (2026-04-14 18:36Z) Updated `README.md` and `.agent/ExecPlan-PDF-Gemini.md` so they no longer point at the removed topic directories.
- [x] (2026-04-14 18:38Z) Validated the final directory layout and confirmed that the user-facing paths now use the flattened structure.

## Surprises & Discoveries

- Observation: the repo had historical and support artifacts inside the folders being flattened, not just top-level PDFs, so those artifacts also needed top-level homes.
  Evidence: the preserved support paths are now `02-Network-Science/Dynamical-Processes-on-Complex-Networks-Barrat-et-al-2008__out/` and `03-Complex-Systems/Nonlinear-Dynamics-Chaos-notes/`.

- Observation: path references are duplicated outside `index.html`, so only moving files would leave stale links behind.
  Evidence: `README.md` and `.agent/ExecPlan-PDF-Gemini.md` both mention the old nested paths.

## Decision Log

- Decision: flatten the book PDFs all the way to the roots of `02-Network-Science/` and `03-Complex-Systems/`, but keep support directories that contain derived materials or notes, renaming them only if needed to avoid collisions.
  Rationale: the user asked to flatten the directory structure for those two category folders, and the simplest consistent interpretation is to eliminate the topical subfolders while preserving non-book artifacts that still belong with those shelves.
  Date/Author: 2026-04-14 / Codex

- Decision: simplify the sidebar structure for these two categories to one flat list per top-level category instead of preserving the old topic subgroup nesting.
  Rationale: this keeps the UI aligned with the flatter disk layout rather than pretending the old subdirectory hierarchy still exists.
  Date/Author: 2026-04-14 / Codex

- Decision: update `README.md` and `.agent/ExecPlan-PDF-Gemini.md` alongside `index.html`.
  Rationale: both files currently embed the old paths and would become misleading after the move.
  Date/Author: 2026-04-14 / Codex

## Outcomes & Retrospective

The refactor landed as intended. `02-Network-Science/` and `03-Complex-Systems/` now keep their main PDFs directly at the category root, the old topical book subdirectories are gone, and the sidebar in `index.html` mirrors that flatter shape with one flat list per category.

The main lesson is that path refactors in this repo are never only filesystem work. Because the library view and repo notes use hard-coded paths, `index.html`, `README.md`, and any checked-in ExecPlans that mention those books all need to move in lockstep.

## Context and Orientation

This repository is a PDF library and reader. The main browsing interface is `index.html`, whose sidebar is hard-coded as nested `<div class="category">`, `<div class="subcategory">`, and `<div class="file">` elements. The file paths inside each `loadPDF(...)` call must match real repository paths because the browser loads them from GitHub’s raw media endpoint.

The two folders in scope are:

- `02-Network-Science/`, which now stores its main PDFs directly at the category root alongside a promoted course README and the Barrat `__out` support directory.
- `03-Complex-Systems/`, which now stores its main PDFs directly at the category root alongside promoted README files and the renamed nonlinear-dynamics notes directory.

The current flattened state keeps the PDFs at the top-level category folders. There are also support artifacts that remain available:

- `02-Network-Science/Dynamical-Processes-on-Complex-Networks-Barrat-et-al-2008__out/`, which contains derived split sections and metadata for one textbook.
- `03-Complex-Systems/Nonlinear-Dynamics-Chaos-notes/`, which contains notebook-based study notes.
- Topic-specific README files promoted to the category root: `02-Network-Science/Machine-Learning-on-Graphs-README.md`, `03-Complex-Systems/Nonlinear-Dynamics-Chaos-README.md`, and `03-Complex-Systems/Urban-Science-README.md`.

The implemented layout eliminates the book subfolders, moves the human-facing book files to the category roots, and preserves support content under the same top-level category with names that remain understandable.

## Plan of Work

First, move all network science PDFs from their topical subfolders into `02-Network-Science/`. Move the Barrat split-output directory out of `Network-Dynamics/` and into the same top-level folder so it stays colocated with the corresponding textbook. Move the machine learning course README to the top-level folder with a specific filename so it no longer requires the old subdirectory. Remove the now-empty topical subdirectories.

Second, move all complex systems PDFs from their topical subfolders into `03-Complex-Systems/`. Move the nonlinear dynamics notes directory and the two topical README files to the top-level folder with descriptive names. Remove the old topic subdirectories once they become empty.

Third, rewrite the `02-Network-Science` and `03-Complex-Systems` sections in `index.html` so each category contains one flat list of file entries pointing at the new top-level paths. Keep the displayed book titles readable and preserve the current labels where they already make sense.

Fourth, update `README.md` and `.agent/ExecPlan-PDF-Gemini.md` so their references point to the new flattened paths. The PDF Gemini plan should continue to refer to the Barrat textbook and its derived `__out` directory using the new locations.

## Concrete Steps

Run all commands from the repository root: `/Users/natkite/Documents/2025/netsi25/PhD/phd-dev/SelfStudy`.

List the current files before moving anything:

    find '02-Network-Science' -maxdepth 3 \( -type d -o -type f \) | sort
    find '03-Complex-Systems' -maxdepth 3 \( -type d -o -type f \) | sort

Move the network science files up one level, then move the complex systems files up one level. After each move, list the top-level category folder to confirm the new shape:

    find '02-Network-Science' -maxdepth 2 \( -type d -o -type f \) | sort
    find '03-Complex-Systems' -maxdepth 2 \( -type d -o -type f \) | sort

Patch `index.html`, `README.md`, and `.agent/ExecPlan-PDF-Gemini.md` so every path matches the new location.

Validate that no old topic-folder references remain in the user-facing files:

    rg -n "02-Network-Science/(Graph-Theory|Complex-Networks|Machine-Learning-on-Graphs|NETS2|Network-Dynamics)/|03-Complex-Systems/(General-Complexity|Nonlinear-Dynamics-Chaos|Urban-Science)/" README.md index.html .agent/ExecPlan-PDF-Gemini.md -g '!**/*.pdf'

## Validation and Acceptance

Acceptance is satisfied when all of the following are true:

1. `find '02-Network-Science' -maxdepth 1 -type f | sort` shows the main network science PDFs directly in `02-Network-Science/`.
2. `find '03-Complex-Systems' -maxdepth 1 -type f | sort` shows the main complex systems PDFs directly in `03-Complex-Systems/`.
3. `index.html` contains no `loadPDF(...)` entries pointing into the old topic subfolders for these two categories.
4. `README.md` and `.agent/ExecPlan-PDF-Gemini.md` contain no stale references to the removed topic directories.
5. `git status --short` shows only the intended moves and file edits.

## Idempotence and Recovery

The move steps are safe to retry if interrupted because each file has one intended destination and the repository is under git. If a move lands in the wrong place, the recovery path is to move the file back before deleting any old directory. Old topic directories should only be removed after a `find` command confirms they are empty.

## Artifacts and Notes

Important reference snippet after the refactor:

    README.md:66-93
    index.html:1528-1614

These ranges show the flattened links and are the quickest visual proof that the reorganization is complete.

## Interfaces and Dependencies

No new libraries or external services are required. The refactor changes filesystem paths plus hard-coded HTML links. The relevant interfaces are the `loadPDF(url, this)` calls inside `index.html`; each URL must continue to resolve to a real repository file after the moves.

Revision note: updated this ExecPlan after implementation to record the completed moves, the flattened sidebar structure, and the final support-file locations.
