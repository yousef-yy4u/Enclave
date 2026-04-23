FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for psycopg2/asyncpg and file extraction
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir -e ".[prod]"

# Copy application source
COPY src/ ./src/
COPY alembic.ini .
COPY alembic/ ./alembic/

# Ensure document storage directory exists
RUN mkdir -p /app/data/documents

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
