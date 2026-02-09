# devops-fastapi-postgres-demo
FastAPI + PostgreSQL notes API, fully containerized with Docker Compose. Includes healthchecks, service dependencies and a persistent volume. Built as a small DevOps learning/demo project to show Docker, API and database working together


# FastAPI + Postgres Docker Compose Project

Simple REST API with PostgreSQL database using Docker Compose. Made for DevOps learning / CV demo.

## What it does

- FastAPI app with `/health` and `/notes` endpoints (GET/POST)
- Postgres 16 database with persistent storage (Docker volume)
- Docker Compose with healthchecks so the API waits for the database to be ready

## How to run

```bash
git clone https://github.com/empahub/devops-fastapi-postgres-demo.git
cd devops-fastapi-postgres-demo
sudo docker compose up -d --build

- Test it

# Check if healthy
curl http://localhost:8000/health

# Get notes (empty at first)
curl http://localhost:8000/notes

# Add note
curl -X POST http://localhost:8000/notes \
  -H "Content-Type: application/json" \
  -d '{"text":"test note"}'

# See all notes
curl http://localhost:8000/notes

- You should see:

{"status":"ok"}
[]
{"id":1,"text":"test note"}
[{"id":1,"text":"test note"}]

API docs: http://localhost:8000/docs


- Stop

sudo docker compose down
sudo docker compose down -v  # deletes database too

- Files

  docker-compose.yml – Postgres + FastAPI services, healthcheck, volume
  Dockerfile – builds the Python FastAPI app
  main.py – FastAPI code + database connection + endpoints
  requirements.txt – fastapi, uvicorn, asyncpg

