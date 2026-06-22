#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
    # Local-dev convenience: manage.py is the developer entrypoint (production
    # serves via gunicorn/wsgi, not manage.py). If no production SECRET_KEY is
    # provided, assume a dev run and enable DEBUG so the app starts with the
    # dev fallback key. On a real server DJANGO_SECRET_KEY is set, so this is a
    # no-op and the strict production defaults apply.
    if not os.environ.get('DJANGO_SECRET_KEY'):
        os.environ.setdefault('DJANGO_DEBUG', '1')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
