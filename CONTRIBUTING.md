# Contributing to Enclave

Thank you for your interest in contributing. This document covers how to report bugs, suggest features, set up a development environment, and submit pull requests.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Commit Message Format](#commit-message-format)

---

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold it. Report unacceptable behavior to the maintainers.

---

## Reporting Bugs

Before filing a bug report, search existing issues to avoid duplicates.

Use the **Bug Report** issue template. Include:

- Your OS, Docker version, and `docker compose version`
- The values of `LLM_PROVIDER` and `EMBEDDING_PROVIDER` in your `.env` (never paste the full file — omit secrets)
- The exact error message or unexpected behavior
- Steps to reproduce reliably
- Relevant log output: `docker compose logs backend --tail=50`

Security vulnerabilities must **not** be reported as public issues. See [SECURITY.md](SECURITY.md).

---

## Suggesting Features

Use the **Feature Request** issue template. Describe the problem you're trying to solve, not just the solution. This helps maintainers evaluate whether it fits the project's scope and constraints (16 GB RAM LAN server is the reference hardware).

---

## Development Setup

### Prerequisites

- Docker and Docker Compose v2+
- Python 3.12+ (for running scripts and backend tests outside Docker)
- Node.js 20+ (for frontend development outside Docker)

### First-time setup

```bash
git clone https://github.com/yousef-yy4u/enclave.git
cd enclave
cp .env.example .env
# Edit .env — defaults work for local dev
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

The dev compose file adds hot reload for both the backend (uvicorn `--reload`) and the frontend (Next.js dev server).

### Running tests

```bash
# Backend unit tests — no Docker needed, runs in <5 seconds
cd backend
pip install -e ".[dev]"
pytest tests/unit/ -v

# Backend integration tests — requires the full Docker stack running
pytest tests/integration/ -v

# Frontend type check + lint
cd frontend
npm ci
npm run type-check
npm run lint

# E2E tests (Playwright) — requires full stack running
npx playwright test
```

### Database migrations

```bash
# Apply all migrations
docker compose exec backend alembic upgrade head

# Create a new migration after changing a model
docker compose exec backend alembic revision --autogenerate -m "description"
```

---

## Coding Standards

### Python (backend)

- Formatter: **Ruff** (`ruff format`)
- Linter: **Ruff** (`ruff check`)
- Type hints are required on all public function signatures
- No raw SQL string concatenation — use SQLAlchemy ORM or parameterized queries
- All new services must have corresponding unit tests in `tests/unit/`

### TypeScript (frontend)

- Formatter and linter: **ESLint** + **Prettier** (configured in `frontend/.eslintrc`)
- Strict TypeScript (`strict: true` in `tsconfig.json`)
- No `any` types without a justification comment
- Component props must be typed with interfaces

### General

- Keep PRs focused — one logical change per PR
- Don't add features or abstractions beyond what the task requires
- Write no comments unless the *why* is non-obvious — well-named identifiers explain the *what*
- Don't break the error code registry (`ENC-XXXX`) — add new codes for new error conditions

---

## Submitting a Pull Request

1. Fork the repository and create a branch from `main`
2. Branch naming: `fix/short-description`, `feat/short-description`, `chore/short-description`
3. Write or update tests for your change
4. Ensure `pytest tests/unit/` and `npm run type-check` both pass locally
5. Fill out the pull request template completely
6. Request a review — PRs without a description will not be reviewed

Branch protection on `main` requires:
- At least one approving review
- All CI checks passing (lint, type check, unit tests, security audit)

---

## Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short summary>

[optional body]
```

Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `ci`

Examples:
```
feat(rag): add trigram similarity fallback when vector search returns 0 results
fix(auth): handle expired refresh token on parallel requests
docs(contributing): add database migration instructions
```
