# NoteMesh — learning guide

## What it does

Shared meeting notes without lost edits. The intended user is study groups. Browser controls → validated Flask API → project analysis/workflow → results and export.

## Run and demonstrate

Follow the README installation block, then: Open study-room in two tabs. Save in one and observe the other update. Type drafts in both, save the first, then save the stale second draft and inspect the conflict message; its text is preserved.

## Important files

- `app.py` — local HTTP interface and request/error handling.
- `core.py` — project-specific logic.
- `tests/` — regression and correctness checks.
- `reports/` — recorded outputs and verification evidence.

## Three engineering decisions

1. Optimistic integer revisions reject stale saves instead of overwriting another user's draft.
2. Server-sent events broadcast saved revisions; heartbeat frames and reconnection keep the client informed.
3. Append-only revision metadata records author and update time alongside the latest note.

## Five interview questions

1. **Is this simultaneous character-level collaboration?** No. Clients edit a local draft and save the whole note. Server-sent events distribute saved revisions. This provides live saved-note synchronization, not a CRDT or operational transformation editor.

2. **How is a lost update prevented?** Each save includes the revision the editor read. A stale revision is rejected instead of overwriting newer content. The browser retains the rejected draft so the user can reconcile it.

3. **Why choose SSE?** Updates travel from server to clients, while saves use ordinary HTTP requests. SSE fits that one-way notification flow without a bidirectional socket protocol.

4. **How did you test the conflict behavior?** Two actual browser tabs shared a room. One saved a newer revision; the other attempted a stale save. The first edit remained authoritative and the second draft stayed visible.

5. **What is the main security boundary?** Room names and author labels are not identities or access control. A public multi-user deployment needs authentication, room authorization and retention controls.

## Independent exercise

Add a read-only revision viewer using the existing history table, without changing the current note.

Write down the expected behavior before editing. Add a meaningful regression check, run the existing suite, and describe what changed in your own words.

## Contribution and resume guidance

The implementation was developed with substantial AI assistance under Abhijith Viswanathan's direction. The verified contribution is the working artifact and the learning work actually completed, not invented employment or adoption.

Suggested factual bullet after personally validating the demo:

- Implemented SSE synchronization and revision-based conflict detection for shared notes; verified two-tab synchronization and preservation of rejected drafts.

Use [VERIFICATION.md](VERIFICATION.md) to add only measured numbers. Do not claim production traffic, users, savings, upstream acceptance or cloud deployment without corresponding evidence.
