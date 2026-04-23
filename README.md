# Enclave

**Local-first enterprise knowledge agent. Your documents, your server, your data.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/yousef-yy4u/enclave/actions/workflows/ci.yml/badge.svg)](https://github.com/yousef-yy4u/enclave/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/badge/docker-compose-ready-2496ED)](docker-compose.yml)

Enclave is an open-source RAG (Retrieval-Augmented Generation) search engine built for organizations that cannot send their data to the cloud. Ingest your documents, ask questions in plain language, and get cited answers — with source highlighting down to the exact passage. Everything runs on your own hardware via Docker.

---

## Features

- **100% on-premises** — no data leaves your server; works fully air-gapped on a LAN
- **Provider-agnostic AI** — swap between Ollama (local), OpenAI, or Anthropic by changing two lines in `.env`; mix and match (e.g. Anthropic for generation, Ollama for embeddings)
- **Source citations with passage highlighting** — every answer links back to the exact chunk in the original document, highlighted in the viewer
- **Module-based RBAC** — assign staff to modules (e.g. "Front Desk", "Curatorial"); documents are restricted to the modules that need them
- **Invitation-only onboarding** — admin generates invite codes; no public self-signup
- **Streaming responses** — token-by-token SSE streaming; no waiting for the full answer
- **Document editor integration** — optional ONLYOFFICE integration for in-browser DOCX editing; edits trigger automatic re-ingestion
- **Conversation memory** — sliding window context with automatic summarization; full history persisted in PostgreSQL
- **Runs on modest hardware** — designed for a 16 GB RAM, CPU-only server (i5 / no GPU)

---

## Architecture

```
┌──────────────┐     SSE stream      ┌──────────────────────┐
│  Next.js 15  │ ◄────────────────── │  FastAPI (Python)    │
│  (App Router)│ ────── REST ──────► │  + pgvector search   │
└──────────────┘                     └──────────┬───────────┘
                                                │
                          ┌─────────────────────┼─────────────────────┐
                          │                     │                     │
                   ┌──────▼──────┐    ┌─────────▼──────┐   ┌─────────▼──────┐
                   │ PostgreSQL  │    │ Ollama / OpenAI │   │   ONLYOFFICE   │
                   │ + pgvector  │    │ / Anthropic     │   │  (optional)    │
                   └─────────────┘    └─────────────────┘   └────────────────┘
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation.

---

## Quick Start

**Requirements:** Docker and Docker Compose (v2+)

```bash
git clone https://github.com/yousef-yy4u/enclave.git
cd enclave

# 1. Copy the environment template
cp .env.example .env

# 2. Edit .env — at minimum, set strong passwords for POSTGRES_PASSWORD and SECRET_KEY
#    (the defaults work for local dev but must be changed for any real deployment)

# 3. Start the stack
docker compose up -d

# 4. Pull Ollama models (first boot only — takes a few minutes)
docker compose exec ollama bash /scripts/pull-models.sh

# 5. Create the first admin account
python scripts/seed-admin.py

# 6. Verify everything is healthy
python scripts/health-check.py
```

Open [http://localhost:3000](http://localhost:3000) and log in with the admin credentials from your `.env`.

---

## Configuration

All configuration is via `.env`. Copy `.env.example` to get started — every variable is documented inline.

Key settings:

| Variable                   | Default    | Description                                                                                        |
| -------------------------- | ---------- | -------------------------------------------------------------------------------------------------- |
| `LLM_PROVIDER`           | `ollama` | Generation engine:`ollama` \| `openai` \| `anthropic`                                        |
| `EMBEDDING_PROVIDER`     | `ollama` | Embedding engine:`ollama` \| `openai`                                                          |
| `EMBEDDING_DIMENSION`    | `768`    | Must match your embedding model.**Changing this after ingestion requires a full re-ingest.** |
| `ENABLE_DOCUMENT_EDITOR` | `false`  | Set `true` to enable ONLYOFFICE (~4 GB additional RAM)                                           |
| `SESSION_TTL_DAYS`       | `30`     | Conversations older than this are purged automatically                                             |

---

## Supported File Types

| Format | Ingestion | Viewer                  | Editor           |
| ------ | --------- | ----------------------- | ---------------- |
| PDF    | Yes       | PDF.js (read-only)      | No               |
| DOCX   | Yes       | Plain text + highlights | Yes (ONLYOFFICE) |
| TXT    | Yes       | Plain text + highlights | Yes (ONLYOFFICE) |
| MD     | Yes       | Plain text + highlights | No               |
| CSV    | Yes       | Plain text + highlights | Yes (ONLYOFFICE) |

---

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide. Quick summary:

```bash
# Start dev stack with hot reload
docker compose -f docker-compose.yml -f docker-compose.dev.yml up

# Run backend unit tests (no Docker needed)
cd backend && pytest tests/unit/ -v

# Run frontend type check
cd frontend && npm run type-check
```

---

## Deployment

Enclave is designed for LAN deployment on a single server. See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for the full production checklist, including static IP setup, firewall rules, and backup configuration.

Rough RAM requirements:

| Configuration                        | RAM Used |
| ------------------------------------ | -------- |
| Ollama (3B model) + PostgreSQL + App | ~5 GB    |
| + ONLYOFFICE enabled                 | ~9 GB    |

---

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

Found a security issue? See [SECURITY.md](SECURITY.md) for the responsible disclosure process — do not open a public issue.

---

## License

[MIT](LICENSE) — free to use, modify, and distribute.
