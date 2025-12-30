# Buffered PDF TTS reader with auto-advance

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must be kept up to date as work proceeds. Maintain this plan in accordance with `.agent/PLANS.md` at the repository root.

## Purpose / Big Picture

Create a simple, audiobook-like PDF TTS experience that behaves like a real media player: click “Read Page” and the reader automatically speaks paragraph-sized fragments, keeps a small buffer of fragments ready, advances the viewer page as narration crosses page boundaries, and shows a continuous playback timeline with elapsed and remaining time. The user-visible outcome is that play/pause/stop and scrubbing work like Spotify/YouTube, with no manual queue management and smooth page transitions.

## Progress

- [x] (2025-12-29 15:42Z) Updated ExecPlan scope to paragraph-based buffering with auto page switching and simplified controls.
- [x] (2025-12-29 16:04Z) Implement buffered narration session state, fragment chunking, and playback loop in `index.html`.
- [x] (2025-12-29 16:04Z) Update `viewer/viewer.html` to preserve line breaks and support narration-specific messaging (`sessionId`, `setPage`).
- [x] (2025-12-29 16:04Z) Simplify UI by removing manual queue controls and wiring play/pause/stop to the new narration flow.
- [x] (2025-12-29 18:10Z) Add continuous narration timeline with elapsed + remaining, scrub/seek across played and buffered segments, and media-style overlay controls.
- [ ] (2025-12-29 18:10Z) Validate auto-advance, buffering behavior, pause/resume, and continuous timeline scrubbing across multiple PDFs (completed: README update; remaining: manual validation).

## Surprises & Discoveries

- Observation: Skipping or seeking while playback was in-flight would allow the original playback promise to resolve and double-count segments.
  Evidence: Playback uses a race with `playbackAbortResolver`, so aborting does not stop `playNextNarrationFragment` from continuing unless guarded.

## Decision Log

- Decision: Use paragraph-based fragments with a hard cap of 150 words; oversized paragraphs are split on periods, then by word count if still too long.
  Rationale: Keeps narration natural while preventing long, blocking audio segments.
  Date/Author: 2025-12-29 / Codex
- Decision: Keep a small buffer of three fragments and prefetch next-page text early to avoid gaps at page boundaries.
  Rationale: Limits memory/time spent generating audio while maintaining seamless playback.
  Date/Author: 2025-12-29 / Codex
- Decision: Remove the manual page queue UI and auto-continue toggle, replacing them with a single narration controller and overlay controls (play/pause/stop/next).
  Rationale: User requested an ebook-like single interface without ad-hoc queueing.
  Date/Author: 2025-12-29 / Codex
- Decision: Use a continuous timeline based on played + current + buffered segment estimates, and display elapsed + remaining time while allowing scrubbing within that buffered window.
  Rationale: Provides an ebook-like, media-player experience without generating unbounded audio in advance.
  Date/Author: 2025-12-29 / Codex
- Decision: Guard narration completion updates when the current fragment changes mid-play (skip/seek), and rebuild session state on seek instead of chaining ad-hoc offsets.
  Rationale: Prevents double-counting segments and keeps the timeline consistent when jumping across history and buffer.
  Date/Author: 2025-12-29 / Codex

## Outcomes & Retrospective

Implemented continuous timeline, elapsed + remaining display, scrub/seek across buffered history, and media-style overlay controls. Manual validation across PDFs is still pending.

## Context and Orientation

The TTS and reader UI live in `index.html`. It uses `requestPageText`/`requestSelectionText` messages to `viewer/viewer.html`, which extracts page text via PDF.js (preserving line breaks) and returns it. The current flow uses a narration session that buffers paragraph fragments (max 150 words), prefetches upcoming pages, and auto-advances the viewer page via a `setPage` message. Page changes are broadcast from the viewer (`pageChanged`), and a PDF open request is still sent via `openFile`. The PDF viewer is local and same-origin, so direct page-setting via messaging is safe and consistent with the existing event bus.

Definitions used in this plan:
- “Fragment”: a text chunk produced from a paragraph (or sentence) of at most 150 words.
- “Buffer”: a small list (target size 3) of fragments ready to be spoken next.
- “Narration session”: a single, continuous reading run that owns fragment state, playback, and auto page switching.

## Plan of Work

Extend the narration controller in `index.html` so playback is tracked on a continuous timeline rather than per-fragment resets. Keep the buffer size small but recompute total buffered duration as fragments are queued, then display elapsed and remaining time in the overlay. Replace the static progress bar with a scrubber that maps a dragged time position to the correct fragment and offset, rewinds or fast-forwards across both history and buffered segments, and resumes playback from the selected point. Update overlay controls and metadata to reflect the current page, segment, and buffer count while remaining consistent with the existing auto-advance flow.

## Concrete Steps

- Work in `/Users/natkite/Documents/2025/netsi25/PhD/phd-dev/SelfStudy`.
- In `viewer/viewer.html`, update `extractPageText` to insert `\n` for line breaks and normalize whitespace; include `sessionId` from request payload in the response. Add a message handler for `{ type: 'setPage', payload: { pageNumber } }` that sets `PDFViewerApplication.page`.
- In `index.html`, remove manual queue data structures, queue UI updates, and auto-continue toggle wiring. Replace with narration session state including `sessionId`, `fragmentQueue`, `pageFragmentCache`, `pendingPageRequests`, and `paused` flags.
- Add helper functions to split page text into paragraphs and fragments (max 150 words; split on periods; fallback to word slicing). Ensure normalization removes soft hyphens and joins hyphenation at line breaks but preserves paragraph breaks.
- Implement `startNarrationFromPage`, `ensureNarrationBuffer`, `playNextFragment`, `pauseNarration`, `resumeNarration`, `stopNarration`, and `skipFragment` functions. Make `Read Page` start a session at the current page number. Ensure the overlay play/pause button toggles the narration state, and stop clears the session.
- Auto-advance the viewer page whenever narration moves to a fragment from a new page (use `setPage` message). Suppress “manual page change” handling for these auto-advances.
- Update overlay metadata to show `Page N` and fragment position (e.g., `Fragment 2/5`) plus the narration speed; display “Buffering…” status when waiting on text.
- Add a continuous narration timeline that sums played + current + buffered durations and exposes a scrubber in the overlay. Implement seek logic that maps a scrubbed time to the correct fragment and offset across history and buffered segments, then restarts playback from that position while preserving paused/playing state.
- Update the overlay time display to show elapsed + remaining side by side, and keep the total duration rolling as buffer estimates change.
- Update `README.md` to describe the new audiobook-like TTS behavior and how to use play/pause/stop.

## Validation and Acceptance

Start a local server (`python3 -m http.server 8000`) and open `index.html`. Load a multi-page PDF and click “Read Page.” Acceptance criteria:
- Narration begins within one page and continues automatically across pages without manual queueing.
- The viewer page visibly changes as narration crosses pages.
- The overlay play/pause button pauses and resumes playback reliably; Stop clears the session.
- Buffering behavior shows a short “Buffering…” status when waiting for page text, without crashing or duplicating fragments.
- The overlay time display shows elapsed + remaining for the buffered timeline and does not reset between fragments.
- Scrubbing moves playback to the selected position across both played and buffered segments, and playback resumes from that point.
- No console errors during page transitions or pauses.

## Idempotence and Recovery

Changes are limited to `index.html`, `viewer/viewer.html`, and `README.md`. Reloading the page resets narration state. If playback stalls, pressing Stop or reloading restores a clean state. Edits are additive and can be re-applied safely.

## Artifacts and Notes

Capture short console logs showing fragment generation (page number, fragment count) and an example of an auto-advance page change to confirm smooth transitions.

## Interfaces and Dependencies

The parent/iframe messaging contract remains same-origin. Use `requestPageText` with payload `{ pageNumber, context: 'narration', sessionId }` and expect `{ text, pageNumber, url, context, sessionId, error? }` from `viewer/viewer.html`. Add a new `setPage` message type to set `PDFViewerApplication.page`. Continue using tts.rocks for audio (`TTS.kokoroTTS`/`TTS.speak`). Preserve existing storage keys for bookmarks and speed; no queue persistence is required.

Plan change note: Replaced the earlier queue-focused ExecPlan with a paragraph-buffered narration plan because the user requested an ebook-like, automatic reader without manual page queue controls.
Plan update note (2025-12-29 16:04Z): Marked implementation steps complete, refreshed context to match the new buffered narration architecture, and noted manual validation remaining.
Plan update note (2025-12-29 17:20Z): Expanded scope to include continuous playback timeline, elapsed + remaining display, and scrub/seek across played and buffered segments per the latest user request.
Plan update note (2025-12-29 18:10Z): Recorded implementation of the continuous timeline + scrubber work and noted remaining manual validation.
