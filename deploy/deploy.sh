#!/usr/bin/env bash
#
# Деплой / обновление attestation.by на сервере CWP.
# Запускать от пользователя django:
#   cd /home/django/webapps/attestation && bash deploy/deploy.sh

set -euo pipefail

APP_DIR="/home/django/webapps/attestation"
VENV="$APP_DIR/venv"
ENV_FILE="$APP_DIR/.env"
DJANGO_DIR="$APP_DIR/web"

cd "$APP_DIR"

echo "==> Загружаем переменные окружения..."
if [[ -f "$ENV_FILE" ]]; then
  set -a; source "$ENV_FILE"; set +a
fi

echo "==> Устанавливаем/обновляем зависимости..."
"$VENV/bin/pip" install -q --upgrade pip
"$VENV/bin/pip" install -q -r requirements.txt

cd "$DJANGO_DIR"

echo "==> Применяем миграции..."
"$VENV/bin/python" manage.py migrate --noinput

echo "==> Собираем статику..."
"$VENV/bin/python" manage.py collectstatic --noinput --clear

echo "==> Очищаем кэш Django..."
"$VENV/bin/python" manage.py shell -c \
  "from django.core.cache import cache; cache.clear(); print('Cache cleared')"

echo "==> Перезапускаем gunicorn..."
systemctl restart gunicorn-attestation

echo "==> Готово."
