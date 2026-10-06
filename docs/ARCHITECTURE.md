# JobFlow architecture

```mermaid
flowchart LR
  Browser[Next.js UI] -->|cookie JWT /api/v1| API[Django REST]
  API --> PG[(PostgreSQL)]
  API --> Redis[(Redis)]
  API --> Mail[SMTP or console email]
  Beat[Celery beat] --> Redis
  Worker[Celery worker] --> Redis
  Worker --> PG
  Worker --> Mail
  CI[GitHub Actions] --> API
  CI --> Playwright
```

Browser calls same-origin `/api/v1`, which Next.js rewrites to Django. Access and refresh tokens are HttpOnly cookies. Celery sends deadline emails. Swagger lives at `/api/v1/docs/`.
