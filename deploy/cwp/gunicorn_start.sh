#!/usr/bin/env bash
#
# Запуск attestation.by через Gunicorn (CWP).

set -euo pipefail

APP_DIR="/home/django/webapps/attestation"
VENV_DIR="$APP_DIR/venv"
LOG_DIR="$APP_DIR/logs"
RUN_DIR="$APP_DIR/run"
ENV_FILE="$APP_DIR/.env"

mkdir -p "$LOG_DIR" "$RUN_DIR"

if [[ -f "$ENV_FILE" ]]; then
  set -a
  source "$ENV_FILE"
  set +a
fi

cd "$APP_DIR"

exec "$VENV_DIR/bin/gunicorn" \
  --name attestation \
  --workers "${GUNICORN_WORKERS:-3}" \
  --bind "${GUNICORN_BIND:-127.0.0.1:8022}" \
  --timeout "${GUNICORN_TIMEOUT:-120}" \
  --log-level "${GUNICORN_LOG_LEVEL:-info}" \
  --access-logfile "$LOG_DIR/gunicorn.access.log" \
  --error-logfile "$LOG_DIR/gunicorn.error.log" \
  --pid "$RUN_DIR/gunicorn.pid" \
  web.wsgi:application
