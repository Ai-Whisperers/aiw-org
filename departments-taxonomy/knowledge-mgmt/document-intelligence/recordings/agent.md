# Recordings Agent

> DEMIURGE-078 — `document-intelligence/recordings`

```yaml
id: di-recordings
agent_id: orpheus-recordings-agent
implementation: demiurge/agents/orpheus-recordings-agent/
department: knowledge-mgmt
status: active
role: Ingest audio/video, transcribe, classify, mine, route, and archive meetings and voice notes.
```

## Role

End-to-end pipeline for recordings: receive file or stream link → transcribe → run Classifier on transcript → run Miner → route outputs → archive original + transcript + extracted assets.

Highest-value near-term win: replaces manual transcription and synthesis sessions.

## Inputs

- Audio/video file or stream URL (`storage_uri`)
- Optional metadata: title, participants, `given.audience`

## Outputs

- Transcript `DocumentEnvelope` (`document_type: transcript`, `dc_type: Text`)
- Lineage: recording envelope (`dc_type: Sound`) → transcript via `source_id` (PROV-inspired)
- Miner assets (action items, decisions, nuggets)
- Router deliveries per Classifier output

## Prior art

- **OpenAI Whisper** — ASR (speech-to-text), open source, state of the art
- **pyannote.audio** — speaker diarization
- **Otter.ai / Fireflies** — commercial pipeline pattern: transcribe → summarize → action items

## Manual analog

[`docs/CONVERSATION-NOTES-AND-LONG-DEPT-LIST.md`](../../../../docs/CONVERSATION-NOTES-AND-LONG-DEPT-LIST.md) — manually created from a meeting transcript.

## Dependencies

- **Classifier**, **Miner**, **Router**, **Archivist** — downstream pipeline stages
- **document.md** — envelope and lineage fields

## Pipeline (Phase 3)

```
recording → diarize (optional) → Whisper transcribe → Classifier → Miner → Router → Archivist
```

## Phase 3 notes

- Speaker labels improve Miner attribution for action items
- Original binary retained at `storage_uri`; transcript is searchable text envelope
