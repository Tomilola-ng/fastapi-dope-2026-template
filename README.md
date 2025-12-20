# 🚀 FastAPI Dope 2026 Template

![Python](https://img.shields.io/badge/Python-3.13+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.125%2B-009688?logo=fastapi&logoColor=white)
![Tortoise ORM](https://img.shields.io/badge/Tortoise%20ORM-Ready-3D9970)
![Aerich](https://img.shields.io/badge/Aerich-Migrations-555)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Ready-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)
![uv](https://img.shields.io/badge/uv-Python%20packager-000000)

Production-ready FastAPI starter featuring:

- 🧠 Tortoise ORM and 🐢 Aerich migrations
- 🐘 PostgreSQL with `asyncpg`
- ☁️ Cloudflare R2 file storage via `boto3`
- 🔐 Token-based API protection
- 📦 `uv` for dependency management and running apps
- 🩺 Health check and 📄 file upload endpoints

Built and maintained by [Tomilola-ng](https://github.com/Tomilola-ng) 💚

## ✨ Features

- FastAPI app with hot-reload dev CLI
- Database setup with Tortoise ORM
- Aerich schema migrations
- R2 file uploads with presigned URL generation
- Paginated listing in local environments
- Docker image using `fastapi run` on port 80

## 📁 Project Structure

```
.
├─ main.py
├─ pyproject.toml
├─ .env.sample
├─ app/
│  ├─ config/
│  │  ├─ settings.py        # Env + Tortoise config
│  │  ├─ database.py        # Tortoise init + alias for Aerich
│  │  ├─ routes.py          # /health + routers
│  │  ├─ storage.py         # R2 client + helpers
│  └─ base/
│     ├─ models.py          # FileAsset model
│     ├─ routes.py          # /base endpoints
│     └─ schemas.py         # Pydantic schemas
└─ migrations/
   └─ models/               # Aerich-generated migrations
```

## ⚙️ Prerequisites

- Python `3.13+`
- `uv` installed (see: https://github.com/astral-sh/uv)
- PostgreSQL instance and connection string
- Cloudflare R2 credentials (optional if you don’t use files)

## 🚦 Quick Start

1. Install dependencies

```
uv sync
```

2. Configure environment

```
copy .env.sample .env
# then edit .env with your DATABASE_URL, R2 keys, etc.
```

3. Initialize Aerich (first time only)

```
uv run aerich init -t app.config.database.TORTOISE_ORM
uv run aerich init-db
```

4. Run development server (hot reload)

```
uv run fastapi dev main.py
# or
uv run uvicorn main:app --reload --port 8000
```

## 🔑 Configuration

Environment variables are loaded from `.env` via `pydantic-settings`:

- `DATABASE_URL` — PostgreSQL connection string
- `ENVIRONMENT` — `local` | `staging` | `production`
- `API_AUTHORIZATION_TOKEN` — token to protect sensitive endpoints
- `CORS_ORIGINS` — CSV or list of allowed origins
- R2: `R2_ENDPOINT_URL`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET_NAME`, `R2_PUBLIC_URL`

See examples in `.env.sample`.

## 🗄️ Database & Migrations

Tortoise config is defined in `settings.py` and exposed to Aerich via an alias:

- `app/config/database.py` exports `TORTOISE_ORM` for Aerich to import.

Common commands:

```
uv run aerich init -t app.config.database.TORTOISE_ORM
uv run aerich init-db
uv run aerich migrate
uv run aerich upgrade
uv run aerich heads
uv run aerich history
```

If you see “Failed to load tortoise config…”, ensure you ran the `init` step with `-t app.config.database.TORTOISE_ORM`.

## 📡 API Endpoints

- `GET /api/v1/health` — Health check
- `POST /api/v1/base/files` — Upload a file (multipart form) to R2, returns metadata + presigned preview URL
- `GET /api/v1/base/files` — Paginated list of files (available when `ENVIRONMENT=local`)

Example file upload:

```
curl -X POST http://localhost:8000/api/v1/base/files \
  -F "file=@./path/to/file.png" \
  -F "alt_text=Optional alt" \
  -F "folder=files"
```

## 🐳 Docker

Build:

```
docker build -t fastapi-dope-2026-template .
```

Run:

```
docker run --env-file .env -p 8000:80 fastapi-dope-2026-template
```

The container runs `fastapi run main.py` on port `80`.

## 🧰 Tech Stack

- FastAPI `fastapi[standard]`
- Tortoise ORM `tortoise-orm`
- Aerich migrations `aerich`
- Async PostgreSQL driver `asyncpg`
- Cloudflare R2 via `boto3`
- `uv` packager and runner

## 🙌 Attribution

Created by [Tomilola-ng](https://github.com/Tomilola-ng) — if this template helps you, please ⭐ the repo and share!
