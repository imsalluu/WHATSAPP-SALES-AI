# Deployment & Docker Architecture

## 1. Multi-Container Orchestration

The application is fully containerized using Docker and Docker Compose:

- **`postgres`**: PostgreSQL 16 with `pgvector` extension for transactional data and vector search.
- **`redis`**: High-performance in-memory caching and message rate limiting.
- **`backend`**: FastAPI asynchronous web server running Uvicorn.
- **`frontend`**: Next.js 14+ production container with optimized standalone output.

---

## 2. Quickstart with Docker Compose

```bash
# 1. Clone the repository
git clone https://github.com/imsalluu/WHATSAPP-SALES-AI.git
cd WHATSAPP-SALES-AI

# 2. Copy environment template
cp .env.example .env

# 3. Spin up all services
docker compose up --build -d
```

Frontend will be accessible at `http://localhost:3000` and FastAPI Backend at `http://localhost:8000/docs`.
