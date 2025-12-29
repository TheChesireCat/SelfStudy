# Add MiniSearch-powered library filtering and fix mobile sidebar scrolling

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must be kept up to date as work proceeds. Maintain this plan in accordance with `.agent/PLANS.md` at the repository root.

## Purpose / Big Picture

Users should be able to search the library by title, category, or subcategory and see the existing tree filtered in place, while the mobile sidebar should scroll all the way to the bottom without truncation. The visible outcome is a search input in the sidebar that narrows the tree and a mobile drawer that scrolls reliably to the last entry.

## Progress

- [x] (2025-12-29 17:27Z) Reviewed `index.html` sidebar markup/CSS/JS and identified the hook points for search indexing and scroll behavior.
- [x] (2025-12-29 17:42Z) Added MiniSearch loader, sidebar search UI, and filtering logic that keeps the existing tree but hides non-matching nodes.
- [x] (2025-12-29 17:46Z) Fixed mobile sidebar scrolling by keeping the sidebar as a flex column and moving scrolling to the file tree.
- [ ] (2025-12-29 17:05Z) Validate locally via `python3 -m http.server 8000` and test desktop + mobile emulation behaviors.

## Surprises & Discoveries

No discoveries yet; work has not started.

## Decision Log

- Decision: Use MiniSearch from the CDN and build the index from existing `.file` elements (including external links).  
  Rationale: The library is already hard-coded in the DOM and this avoids rewriting the data model.  
  Date/Author: 2025-12-29 / Codex
- Decision: Filter by hiding non-matching DOM nodes and revealing matched files with their ancestor headers instead of rendering a separate search results list.  
  Rationale: The requirement is to keep the regular tree structure but filtered.  
  Date/Author: 2025-12-29 / Codex
- Decision: Initialize search after the window `load` event so MiniSearch is available, and fall back to a simple text search if the CDN script is unavailable.  
  Rationale: Deferred CDN scripts execute after parsing, and the fallback keeps search usable offline.  
  Date/Author: 2025-12-29 / Codex

## Outcomes & Retrospective

Implementation complete for search UI/filtering and the mobile scroll fix; local validation is still pending to confirm behavior across breakpoints.

## Context and Orientation

The primary UI lives in `index.html` and uses inline CSS/JS. The left sidebar is a flex column with a header (`#header`) followed by the library tree (`#file-tree`). Each category is a `.category` element containing a `.category-header` and `.category-content`; nested subcategories use `.subcategory-header` followed by `.file-list`. Individual library entries are `.file` elements with inline `onclick` handlers for `loadPDF(...)` or `loadExternal(...)`. The JS already provides helpers to open PDFs, EPUBs, MOBIs, and external links; it also expands ancestors for selected files.

The mobile sidebar uses a media query at `max-width: 1023px` to switch into a fixed-position drawer. Right now the open state sets `display: block`, which breaks the flex layout and can interfere with scrolling.

## Plan of Work

Work happens only in `index.html`. Add a MiniSearch script tag in the `<head>` (CDN). Insert a search UI element between `#header` and `#file-tree` so it stays fixed while the tree scrolls. Add CSS for the search input, a clear button, and a small status line, plus helper classes (for example, `.search-hidden`) to hide non-matching nodes.

Add JS functions that build search documents from the existing `.file` DOM nodes. For each file, collect its title text plus its category and subcategory labels (derived from ancestor headers). Index these fields with MiniSearch so queries match titles, categories, and subcategories. Implement a filter pass that hides all non-matching nodes, reveals the matching files and their ancestor headers, and forces the relevant `.file-list` and `.category-content` containers open while search is active. When the search query is cleared, restore the previous open/closed state and show the full tree again.

Fix the mobile scroll issue by keeping `#sidebar` as a flex column in the open state and moving the scrollable region to `#file-tree`. Apply `overflow: hidden` to the sidebar container and `overflow-y: auto` plus safe-area padding to the file tree. This prevents nested scroll containers and ensures the final entries are reachable on mobile.

## Concrete Steps

Run commands from `/Users/natkite/Documents/2025/netsi25/PhD/phd-dev/SelfStudy`.

1) Inspect current sidebar structure and mobile CSS:
   - `rg -n "#sidebar|#file-tree|subcategory-header|category-content" index.html`
   - `sed -n '200,420p' index.html`
   - `sed -n '940,1040p' index.html`

2) Add the MiniSearch CDN script in `index.html` and insert the search UI markup between `#header` and `#file-tree`.

3) Update the CSS block in `index.html` to style the search input and define `.search-hidden` plus `.search-active` behavior. Adjust the mobile `@media (max-width: 1023px)` rules so the sidebar uses `display: flex` when open and only `#file-tree` scrolls. Add safe-area padding to `#file-tree` on mobile.

4) Update the JS block in `index.html` to:
   - Build a search index from `.file` elements using MiniSearch.
   - Listen for input changes, run searches, and apply DOM filtering.
   - Snapshot and restore open states when entering/leaving search.

5) Validate manually by running `python3 -m http.server 8000` and visiting `http://localhost:8000/index.html`. Confirm that search filters the tree, categories/subcategories remain visible for matches, external links appear in results, and the mobile sidebar scrolls to the bottom.

## Validation and Acceptance

- Typing a query in the sidebar search filters the existing tree in place, showing matching file titles with their category/subcategory headers still visible.
- Searching for a category or subcategory name returns the expected files under those headings, including external links.
- Clearing the search restores the tree and its previous open/closed state.
- On mobile widths (<=1023px), the sidebar drawer opens with a fully scrollable file tree that reaches the last entry.
- No console errors are introduced by the search logic or MiniSearch loading.

## Idempotence and Recovery

Changes are confined to `index.html`. Re-applying the steps is safe because the search UI and CSS selectors are stable. If something goes wrong, use `git diff` to identify the changes and revert the affected sections. No data migrations are required.

## Artifacts and Notes

Record any console errors or unexpected scroll behavior discovered during validation, and note the exact queries or viewport sizes that reproduce issues.

## Interfaces and Dependencies

MiniSearch is loaded from `https://cdn.jsdelivr.net/npm/minisearch@7.2.0/dist/umd/index.min.js` and provides the `MiniSearch` global. The existing `loadResource`, `openDocument`, and `openExternalResource` functions remain unchanged; search only filters the DOM and uses existing click handlers on `.file` elements.

Plan update (2025-12-29): Marked progress for the completed search UI and mobile scroll adjustments, added the decision to initialize search after `load` with a fallback when MiniSearch is unavailable, and noted that validation remains pending.
