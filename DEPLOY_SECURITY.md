# Деплой и безопасность — attestation.by

## Обязательные переменные окружения (production)

Без `DJANGO_SECRET_KEY` приложение **намеренно не запустится** при `DEBUG=False`.

```bash
# --- Обязательно ---
DJANGO_SECRET_KEY="<длинный случайный ключ, см. ниже>"
DJANGO_ALLOWED_HOSTS="attestation.by,www.attestation.by"

# --- Почта (Yandex SMTP) ---
EMAIL_HOST_USER="ваш@yandex.ru"
EMAIL_HOST_PASSWORD="пароль-приложения-яндекс"
CONTACT_EMAIL="куда-получать-заявки@example.com"   # по умолчанию = EMAIL_HOST_USER

# --- Telegram (опционально) ---
TELEGRAM_BOT_TOKEN="123456:ABC..."
TELEGRAM_CHAT_ID="-100123456789"

# --- Необязательно (есть разумные значения по умолчанию) ---
DJANGO_DEBUG=0                 # 0/пусто = продакшен (по умолчанию)
DJANGO_SSL_REDIRECT=1          # редирект http->https
DJANGO_HSTS_SECONDS=31536000   # 1 год
CONTACT_RATE_LIMIT=5           # заявок с одного IP за окно
CONTACT_RATE_WINDOW=3600       # окно в секундах (1 час)
```

### Генерация SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Что включено в защиту

| Механизм | Где | Эффект |
|---|---|---|
| `DEBUG=False` по умолчанию | settings.py | Нет утечки traceback/кода |
| SECRET_KEY из env (обязателен) | settings.py | Нельзя подделать сессии |
| `ALLOWED_HOSTS` без `*` | settings.py | Защита от Host Header Injection |
| SSL-редирект + HSTS | settings.py (prod) | Принудительный HTTPS |
| Secure / HttpOnly / SameSite cookies | settings.py (prod) | Защита cookies сессии и CSRF |
| **CSP** + защитные заголовки | core/middleware.py | Блок инъекции внешних скриптов, кликджекинга, угона форм |
| Rate-limit на форму (per-IP) | core/views.py | Защита от спама/флуда (429) |
| Honeypot-поле | форма + views.py | Отсев ботов |
| Лимит длины полей | core/views.py | Защита от оversized-payload |

## Запуск в production

**Не использовать `runserver`** (однопоточный, для разработки). Нужен gunicorn + Nginx:

```bash
# пример
gunicorn web.wsgi:application --bind 127.0.0.1:8000 --workers 3
```

Nginx должен передавать `X-Forwarded-Proto` (для корректного SSL-редиректа)
и `X-Forwarded-For` (для rate-limit по реальному IP).

## Проверка перед деплоем

```bash
python manage.py check --deploy
```

Должно быть 0 критических замечаний (только опциональные W-предупреждения,
если SECRET_KEY короткий).

## Локальная разработка

`manage.py` автоматически включает `DJANGO_DEBUG=1`, если `DJANGO_SECRET_KEY`
не задан — то есть локально `python manage.py runserver` просто работает,
а на сервере (где задан SECRET_KEY) действуют строгие production-настройки.
