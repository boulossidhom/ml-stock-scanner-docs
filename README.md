# ML Stock Scanner

Production-grade ML platform for stock market prediction.

## Architecture

Multi-server infrastructure on Hetzner Cloud:
- **app-server**: FastAPI Backend + Web UI (Next.js)
- **db-server**: PostgreSQL 16 + TimescaleDB
- **ml-server**: ML Training + Inference
- **cache-server**: Redis + Celery Queue

## Getting Started

See documentation in `docs/` directory.
