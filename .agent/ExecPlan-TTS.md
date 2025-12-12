# TTS auto-advance and audiobook-grade UX

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must be kept up to date as work proceeds. Maintain this plan in accordance with .agent/PLANS.md at the repository root.

## Purpose / Big Picture

Enable an audiobook-like reading flow: start narration and have pages advance automatically with clear controls to pause/resume, skip, and view what is up next. The user-visible outcome is that clicking “Read Page” (or starting a queue) continuously reads forward through the document without manual re-triggering, and the overlay/badge reflects current page, queue length, and allows pausing/resuming.

## Progress

- [x] (2026-03-03 18:20Z) Captured current TTS flow, issues (instant finish due to missing audio events, manual queueing only), and defined audiobook UX goals; created this ExecPlan.
- [x] (2026-03-03 19:05Z) Hardened playback completion handling with minimum fallback duration when no/zero-length audio is present.
- [x] (2026-03-03 19:30Z) Added auto-continue toggle (default on), seeding current+next page into the queue from “Read Page”, and auto-enqueue of subsequent pages after each completion.
- [x] (2026-03-03 19:40Z) Added skip controls (overlay + queue panel), queue status in overlay metadata, and queue action buttons; stored auto-continue preference.
- [ ] Validate manual and auto modes across breakpoints; adjust pause/resume/skip ergonomics if needed; update README/UX notes after hands-on testing.

## Surprises & Discoveries

- Observation: None yet for this scope.  
  Evidence: Plan creation only.

## Decision Log

- Decision: Treat “auto mode” as default when reading a page—seed queue with current page, then prefetch next pages up to a small cap, and advance automatically until stopped or text is unavailable.  
  Rationale: Matches audiobook expectations without extra clicks while keeping queue bounded.  
  Date/Author: 2026-03-03 / Codex
- Decision: Keep queue stored in JS state only (no persistence) and reuse existing overlay/status surfaces; add a compact queue badge in tools pane and overlay metadata showing “Page N (k remaining)”.  
  Rationale: Minimizes new UI while surfacing progress.  
  Date/Author: 2026-03-03 / Codex
- Decision: Pause/resume should halt current audio and timer but keep queue intact; resume continues from same page if mid-playback, otherwise continues to next queued item.  
  Rationale: Aligns with audiobook controls and avoids re-fetching text unless needed.  
  Date/Author: 2026-03-03 / Codex

## Outcomes & Retrospective

Pending implementation; will summarize auto-advance behavior, control ergonomics, and any reliability gaps after testing.

## Context and Orientation

Main TTS logic is in `index.html`: buttons trigger `requestSelectionPlayback`/`requestPagePlayback`, which post messages to `viewer/viewer.html` for selection/page text. Responses land in `handleSelectionText`/`handlePageText`; playback uses `ensureTTSReady` (Kokoro via tts.rocks), `speakText`, and overlay/progress helpers. We recently added a manual queue (`narrationQueue`, `processQueue`, `requestPageText` with `context: 'queue'` and `queueId`). `viewer/viewer.html` extracts page text via PDF.js and echoes `context`/`queueId`. Overlay and status are driven by `startPlaybackProgress`/`stopPlaybackProgress`, which currently assume audio end events; a fallback wait exists but needs tuning. The queue UI lives in the tools pane; Quick controls in the bottom bar are for bookmarks/TTS. No persistence exists for the queue.

## Plan of Work

1. Playback robustness: tighten `waitForPlaybackCompletion` to detect zero-duration players and apply a reasonable fallback delay; ensure overlay progress handles fallback mode smoothly. Verify Kokoro/piper players attach correctly; log when no audio element is found and fallback kicks in.
2. Auto-advance mode: introduce an “Auto Continue” toggle (default on) near the narration controls. When enabled, “Read Page” seeds the queue with the current page and the next N pages (bounded). After each page completes, fetch the next page and continue until queue empties; stop gracefully at doc end or on error. Keep manual queue actions available.
3. Controls: add Pause/Resume and Skip to the overlay or tools pane. Pause should freeze current audio and queue; Resume should continue. Skip should stop current audio and advance to next queued page. Stop should clear queue and overlay as today.
4. Status UI: show “Page X (Y queued)” in overlay metadata and update the tools-pane queue badge; optionally list first few upcoming pages. Indicate when auto-mode is on/off.
5. Acceptance polish: ensure state resets on document change, external link, or ebook mode; protect against viewer not ready; guard requests when no page number is known.
6. Docs: update README to mention auto-advance, pause/resume/skip controls, and queue behavior/limits.

## Concrete Steps

- Work in `/Users/natkite/Documents/2025/netsi25/PhD/phd-dev/SelfStudy`.
- Playback robustness: refine `waitForPlaybackCompletion` in `index.html`; handle `player.duration` <= 0, and set a minimum fallback based on word count; keep overlay progress in sync.
- Auto-advance: add `autoContinue` state and toggle UI near narration controls; modify `requestPagePlayback` and queue seeding to add current+next pages when auto mode is on; add `runNextQueueItem` logic to auto-enqueue the subsequent page until exhausted or stopped; detect end-of-doc by empty text or repeated failures and surface a user message.
- Controls: add Pause/Resume and Skip buttons (overlay and/or tools pane) wired to pause current audio (retain position if possible) and to advance the queue; keep Stop clearing queue; ensure buttons disable appropriately.
- Status UI: update overlay meta and queue badge to include current page and queued count; ensure accessibility labels update.
- Docs: extend `README.md` “Reader features” to include auto-advance and controls; add a short usage note in “Using the reader” or equivalent.
- Manual validation: run `python3 -m http.server 8000`, open `index.html`, load a multi-page PDF, test: single-page read, auto-continue through at least 3 pages, pause/resume mid-page, skip to next, stop clears queue; verify state reset after changing documents and on mobile layout.

## Validation and Acceptance

Auto-continue on: clicking “Read Page” reads current page, then automatically continues to subsequent pages until Stop or document end, with overlay showing “Page N (k queued)” and a badge reflecting the queue. Pause/Resume halts and continues playback without losing the queue; Skip advances to the next queued page. Stop clears queue and overlay. Manual mode (auto-continue off) behaves like current single-page reads. No console errors across desktop/tablet/mobile. README documents the behavior.

## Idempotence and Recovery

Edits are confined to `index.html`, `viewer/viewer.html`, and `README.md`. Reloading the page clears transient queue state. If playback gets stuck, Stop or reload resets the queue. The plan’s steps can be re-applied; no migrations or persistent schema changes exist.

## Artifacts and Notes

Capture short notes on playback timing fallback (e.g., minimum wait = max(estimateMs, 2s) if no audio element) and any Kokoro/piper quirks. Log snippets may be useful to confirm queue advancement.

## Interfaces and Dependencies

Reuse existing messaging: `requestPageText` optionally includes `pageNumber`, `context`, `queueId`; `viewer/viewer.html` returns `{ text, pageNumber, url, context, queueId, error? }`. Keep TTS via tts.rocks (`TTS.kokoroTTS`/`TTS.speak`). Add pause/skip controls on top of current overlay; maintain `localStorage` keys (`pdfBookmarks`, `pdfLastDocument`, `ttsNarrationSpeed`, `pdfjs-theme`) unchanged. Ensure new auto-mode toggle defaults to on and is stored in memory only (no persistence) unless a simple `localStorage` flag is warranted. 
