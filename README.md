# Virtual Brain Backend

Minimal V1 backend scaffold for the Virtual Brain project.

## Current scope

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`
- `GET /health`

## Stack

- FastAPI
- SQLAlchemy
- JWT authentication
- SQLite by default for local development

## Local setup

1. Create a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and update secrets.
4. Run the API:

```bash
uvicorn app.main:app --reload
```

## Notes

- The default `DATABASE_URL` uses SQLite so you can start quickly.
- For the real V1 cloud deployment, switch to Postgres by setting `DATABASE_URL`.
- Table creation currently runs automatically on startup to keep the first iteration simple.
