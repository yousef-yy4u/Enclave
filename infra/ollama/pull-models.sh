#!/usr/bin/env bash
# Pull default Ollama models on first boot.
# Run inside the ollama container:
#   docker compose exec ollama /bin/bash /infra/ollama/pull-models.sh
# Or mount and call from a one-shot container on first deploy.

set -euo pipefail

OLLAMA_HOST="${OLLAMA_HOST:-http://localhost:11434}"

echo "Waiting for Ollama to be ready..."
until curl -sf "${OLLAMA_HOST}/api/tags" > /dev/null; do
  sleep 2
done
echo "Ollama is ready."

EMBED_MODEL="${OLLAMA_EMBED_MODEL:-nomic-embed-text}"
GEN_MODEL="${OLLAMA_GEN_MODEL:-llama3.2:3b}"

echo "Pulling embedding model: ${EMBED_MODEL}"
ollama pull "${EMBED_MODEL}"

echo "Pulling generation model: ${GEN_MODEL}"
ollama pull "${GEN_MODEL}"

echo "Done. Models available:"
ollama list
