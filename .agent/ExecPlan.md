# Three-pane reader layout with unified tools and responsive drawers

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must be kept up to date as work proceeds. Maintain this plan in accordance with .agent/PLANS.md at the repository root.

## Purpose / Big Picture

Restructure the main reading experience into a clean three-pane layout on desktop (library list, PDF reader, unified reading tools) with a coherent light/dark theme that matches the viewer. On mobile, collapse into a PDF-first single pane with drawers/sheets for library and tools. The user-visible outcome: clear navigation, a tidy reader with page/zoom/search controls, and a consolidated tools panel (bookmarks, highlights/notes placeholder, narration) that feels intentional and minimal.

## Progress

- [x] (2025-12-03 17:55Z) Captured requirements for 3-pane layout, tool consolidation, and responsive behavior; reset plan scope to this redesign.
- [x] (2025-12-03 18:35Z) Inventoried existing structure (theme sync, TTS, bookmarks, iframe messaging) and extracted file tree/bookmark/TTS blocks for reuse.
- [x] (2025-12-03 18:45Z) Implemented desktop three-pane layout: library-only left pane, reader center with top toolbar shell, right tools pane with bookmark card, narration card (read selection/page, speed), and notes placeholder using shared tokens.
- [x] (2025-12-03 18:55Z) Added responsive behavior: library drawer <1024px with backdrop; tools pane stays at medium; bottom quick toolbar + expandable sheet for tools on mobile (<768px); dual theme toggles synced to viewer.
- [ ] (2025-12-03 18:55Z) Validate bookmarks, PDF load, TTS selection/page reads, and responsive behavior across breakpoints; adjust UI polish (spacing, icons, shadows, contrast).

## Surprises & Discoveries

- Observation: None yet for this scope.  
  Evidence: Plan creation only.

## Decision Log

- Decision: Use a CSS grid/flex three-pane shell at ≥1024px; collapse left pane at <1024px and convert tools to a bottom toolbar+sheet at ≤767px.  
  Rationale: Matches the requested breakpoints and keeps the reader central on smaller viewports.  
  Date/Author: 2025-12-03 / Codex
- Decision: Keep the existing PDF viewer iframe (`viewer/viewer.html`) and messaging contract (`openFile`, `requestSelectionText`, `requestPageText`, `requestCurrentPage`), reusing the shared `pdfjs-theme` toggle for consistency.  
  Rationale: Avoids reworking PDF.js internals while aligning visuals.  
  Date/Author: 2025-12-03 / Codex
- Decision: Consolidate tools into a right pane card stack (bookmarks, narration controls, notes/highlights placeholder) with light elevation using the existing token palette (shared with viewer).  
  Rationale: Delivers the requested merged tools without new dependencies.  
  Date/Author: 2025-12-03 / Codex

## Outcomes & Retrospective

Pending implementation; will summarize layout results, responsive behavior, and any accessibility gaps.

## Context and Orientation

Current main UI is in `index.html` with inline CSS/JS. It embeds `viewer/viewer.html` in an iframe, exchanges messages for opening files and retrieving selection/page text, and manages bookmarks/TTS locally with `localStorage` keys (`pdfBookmarks`, `pdfLastDocument`, `ttsNarrationSpeed`, `pdfjs-theme`). The library tree and TTS controls live in the sidebar; floating controls sit over the reader. The viewer already has dual-theme tokens and a toggle in `viewer/viewer.html`/`viewer.css`/`viewer.mjs`. We will:
- Reorganize `index.html` into a three-area layout: left library list, center reader (placeholder + iframe + top mini-toolbar), right tools panel for bookmarks + narration + notes placeholder.
- Reuse the shared token palette defined in `index.html` (aligned to viewer) for consistent light/dark styling.
- Adjust JS for new DOM structure (moving controls, drawers/sheets) while preserving messaging and bookmark/TTS logic.

## Plan of Work

Describe, in prose, the sequence of edits and additions. For each edit, name the file and location and what to insert or change.

1) Orient and inventory: read `index.html` CSS/JS blocks to map current sidebar, floating TTS controls, bookmark buttons, and theme sync; note iframe messaging and storage keys. Note viewer-side theme toggle already exists.  
2) Desktop layout (≥1024px): convert body into a three-column grid/flex: left library (header + file tree only), center reader container (placeholder + iframe + top toolbar for page/zoom/search hooks), right tools column (~260px) with stacked cards:  
   - Bookmarks card: set/resume/clear buttons, status text.  
   - Narration card: read selection, read page, speed slider, playback overlay/summary.  
   - Notes/highlights placeholder card (structure only).  
   Apply tokens for surfaces, borders, soft shadows, rounded corners; use thin icons (can reuse emoji/inline SVG).  
3) Responsive behavior:  
   - 768–1023px: left pane collapsible via hamburger; right pane remains but may overlay; ensure main reader width stays primary.  
   - ≤767px: PDF full screen; left pane becomes slide-in drawer with backdrop; right tools become bottom pill toolbar with buttons (bookmark, notes/highlights placeholder, read selection, read page, TTS speed/playback). Provide expandable sheet/modal for detailed controls (speed slider, status).  
   Ensure drawers/sheets use CSS transitions and respect `prefers-reduced-motion`.  
4) Theme and visuals: keep shared token palette; ensure new components consume tokens (panel bg, border, text, accent, focus). Keep gradients minimal (or remove) in favor of flat tinted surfaces.  
5) JS wiring:  
   - Update selectors and event bindings to new DOM structure (buttons moved to right pane and bottom toolbar).  
   - Ensure theme toggle still updates `data-theme` on root and syncs to iframe on load/ready.  
   - Adjust show/hide logic for drawers and bottom sheet; ensure accessibility (aria labels, focus trapping where appropriate, Escape to close).  
   - Preserve existing bookmark/TTS logic and messaging; only relocate UI controls.  
6) Testing/validation: manual in browser: load PDFs, expand library, trigger drawers, switch breakpoints, set/resume bookmarks, read selection/page, adjust speed, toggle theme. Capture notes for any accessibility or interaction issues.

## Concrete Steps

- Work in `/Users/natkite/Documents/2025/netsi25/PhD/phd-dev/SelfStudy`.
- Review current structure: `sed -n '1,260p' index.html` (layout/styles), `rg -n "bookmark|tts|theme|viewer" index.html`.  
- Implement layout/CSS and move controls in `index.html`:  
  - Define three-pane grid for ≥1024px; style panels with tokens; add top reader toolbar container.  
  - Build right tools panel cards; add bottom toolbar + sheet for mobile; add left drawer markup for library.  
  - Update media queries for 1024/768/767 breakpoints.  
- Update JS in `index.html`:  
  - Rebind bookmark/TTS buttons to new elements; manage drawer/bottom-sheet toggles; keep theme sync to iframe.  
  - Ensure `viewerReady` handler calls theme sync; keep existing postMessage handling.  
- Validate manually (browser):  
  - Desktop: verify three panes, scrolling lists, theme toggle affects all panes and iframe; bookmarks/TTS work.  
  - Tablet width (~900px): library collapsible; tools visible; interactions OK.  
  - Mobile (~390px): library drawer, bottom toolbar + sheet; TTS and bookmarks usable; theme toggle present (location TBD).  
- Adjust spacing/contrast/focus as needed; document outcomes.

## Validation and Acceptance

- Desktop (≥1024px): three visible panes; library scrolls independently; tools panel houses bookmark set/resume/clear, TTS controls (read selection/page, speed), notes placeholder; theme toggle applies to page + iframe; PDF loads and bookmarks/TTS operate normally.  
- Medium (768–1023px): library collapsible drawer with backdrop; tools pane still accessible; reader prioritized.  
- Mobile (≤767px): reader full screen; library via left drawer; tools via bottom toolbar and expandable sheet; TTS and bookmark actions work; overlays/drawers close via tap/Escape; no layout shifts or clipped controls.  
- No console errors; focus outlines visible; `pdfjs-theme` persists and syncs.

## Idempotence and Recovery

Edits confined to `index.html` (markup/CSS/JS). Re-running steps is safe. If layout regresses, use `git diff` to revert specific sections. LocalStorage keys (`pdfBookmarks`, `pdfLastDocument`, `ttsNarrationSpeed`, `pdfjs-theme`) can be cleared for clean testing without affecting code.

## Artifacts and Notes

Note before/after layout sketches and any accessibility considerations (focus traps for drawers/sheets, `aria-expanded`/`aria-controls`). Capture any CSS decisions (grid vs flex) and token tweaks needed for contrast.

## Interfaces and Dependencies

Preserve existing contracts: `window.loadPDF` → `openDocument` → iframe postMessage `{ type: 'openFile', payload: { url, pageNumber? } }`; bookmark save/resume via `requestCurrentPage`/`currentPage` message; TTS via `requestSelectionText`/`requestPageText` responses. Reuse `pdfjs-theme` storage key and `data-theme`/`.is-dark|.is-light` application on both documents. No new external dependencies.
