#!/usr/bin/env bash
# PostgreSQL backup wrapper. Keeps last 7 daily dumps.
# Recommended cron: 0 3 * * * /path/to/backup-db.sh
# Requires: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB set in environment.

set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-./backups}"
RETAIN_DAYS="${RETAIN_DAYS:-7}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME="${BACKUP_DIR}/enclave_${TIMESTAMP}.sql.gz"

mkdir -p "${BACKUP_DIR}"

echo "Backing up ${POSTGRES_DB:-enclave} → ${FILENAME}"

PGPASSWORD="${POSTGRES_PASSWORD:-CHANGE_ME}" pg_dump \
  -h "${POSTGRES_HOST:-localhost}" \
  -p "${POSTGRES_PORT:-5432}" \
  -U "${POSTGRES_USER:-enclave}" \
  "${POSTGRES_DB:-enclave}" \
  | gzip > "${FILENAME}"

echo "Backup complete: ${FILENAME}"

# Remove dumps older than RETAIN_DAYS
find "${BACKUP_DIR}" -name "enclave_*.sql.gz" -mtime "+${RETAIN_DAYS}" -delete
echo "Pruned backups older than ${RETAIN_DAYS} days."
