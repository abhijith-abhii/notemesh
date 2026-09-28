# NoteMesh

Shared meeting notes without lost edits for **study groups**.

Original topic: **Real-Time Collaborative Notes App** from [the source post](https://www.instagram.com/p/DdyMaogE4ud/).

> Local portfolio implementation developed with Codex assistance. Measured results and limitations are documented; no production adoption, revenue or hiring outcome is claimed.

![Application screenshot](reports/screenshots/app.png)

## What works

- Live saved-note synchronization with SSE
- Optimistic revision checks and preserved conflict drafts
- Persistent revision history and Markdown export

[Example output](reports/example-output.json) · [Verification notes](VERIFICATION.md) · [Learning and interview guide](LEARNING_GUIDE.md)

## Start

Python 3.12 is the validated Python runtime. Run commands from this repository directory. Windows users activate `.venv\Scripts\activate` instead of `source`.

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:8080**. Keep the process running. Set `PORT` to use another port. The Python development servers are intended for local demonstrations.

## Demonstration

Open study-room in two tabs. Save in one and observe the other update. Type drafts in both, save the first, then save the stale second draft and inspect the conflict message; its text is preserved.

## Architecture and decisions

Browser controls → validated Flask API → project analysis/workflow → results and export.

Stack: Flask · SQLite · SSE.

1. Optimistic integer revisions reject stale saves instead of overwriting another user's draft.
2. Server-sent events broadcast saved revisions; heartbeat frames and reconnection keep the client informed.
3. Append-only revision metadata records author and update time alongside the latest note.

## Verification

```sh
python -m pytest -q
```

See [VERIFICATION.md](VERIFICATION.md) for actual executed checks, setup verification, model/data results and any outstanding environment limitations. The [recorded CI runs](reports/ci-verification.json) passed for the linked source revision.

## Data and attribution

Local shared notes. See [DATA_AND_SOURCES.md](DATA_AND_SOURCES.md) for provenance and usage notes. Original project code is MIT unless a preserved source file or dependency states otherwise. Model and third-party data licenses remain separate.

## Limitations and next improvement

Whole-note optimistic editing, not character-level CRDT merging. No authentication or tenancy; anyone with local access to a room can edit. Author names are self-reported. History lists metadata; full historical bodies remain in SQLite.

Suggested extension: Add a read-only revision viewer using the existing history table, without changing the current note.

## Honest portfolio use

This implementation and documentation were developed with substantial Codex assistance. Before presenting it, run the demonstration, explain the design choices, and complete the suggested independent modification. Do not describe generated code as work experience, an accepted upstream contribution, or a deployed production service.
