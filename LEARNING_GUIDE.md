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

1. **What problem does this project solve, and what is its unit of work?** Explain shared meeting notes without lost edits, identify study groups as the audience, and trace one concrete example through the files above. Use the demonstration output rather than hypothetical impact.
2. **Why did you choose the first design decision?** Optimistic integer revisions reject stale saves instead of overwriting another user's draft. Show the corresponding implementation and a test that would fail if that property were removed.
3. **How do you protect correctness when inputs or execution change?** Server-sent events broadcast saved revisions; heartbeat frames and reconnection keep the client informed. Explain the relevant invalid-input or edge-case test and distinguish a checked property from an untested assumption.
4. **How do you make results inspectable and reproducible?** Append-only revision metadata records author and update time alongside the latest note. Point to actual outputs and recorded commands. Explain why a successful example is weaker evidence than a tested boundary or independently reconciled total.
5. **What would you improve before real deployment or real-data use?** Whole-note optimistic editing, not character-level CRDT merging. No authentication or tenancy; anyone with local access to a room can edit. Author names are self-reported. History lists metadata; full historical bodies remain in SQLite. Choose one limitation, describe the missing evidence, and propose a measurable acceptance check rather than promising production readiness.

## Independent exercise

Add a read-only revision viewer using the existing history table, without changing the current note.

Write down the expected behavior before editing. Add a meaningful regression check, run the existing suite, and describe what changed in your own words.

## Contribution and resume guidance

The implementation was developed with substantial AI assistance under Abhijith Viswanathan's direction. The verified contribution is the working artifact and the learning work actually completed, not invented employment or adoption.

Suggested factual bullet after personally validating the demo:

- Implemented and validated shared meeting notes without lost edits using Flask · SQLite · SSE, with live saved-note synchronization with sse and documented correctness checks and limitations.

Use [VERIFICATION.md](VERIFICATION.md) to add only measured numbers. Do not claim production traffic, users, savings, upstream acceptance or cloud deployment without corresponding evidence.
