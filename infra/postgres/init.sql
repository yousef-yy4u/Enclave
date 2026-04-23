-- Run once by PostgreSQL on first container start (docker-entrypoint-initdb.d)
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
