#!/bin/sh
set -e

python - <<'PY'
import os, time
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from django.db import connection
for attempt in range(30):
    try:
        connection.ensure_connection()
        break
    except Exception:
        time.sleep(1)
else:
    raise SystemExit("database is not ready")
PY

python manage.py migrate --noinput
python manage.py seed_jobs
exec "$@"
