# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ML Stock Scanner is a machine learning-based stock analysis platform designed for high-accuracy stock scanning and prediction. The system uses a multi-server infrastructure deployed on Hetzner cloud with a hybrid architecture.

## Infrastructure Architecture

The application runs on a 4-server architecture:

| Server | Private IP | Type | Primary Role |
|--------|-----------|------|--------------|
| app-server | 10.0.1.1 | CPX31 | Web UI (Next.js), API, Nginx |
| db-server | 10.0.1.2 | CPX41 | PostgreSQL 16 Database |
| ml-server | 10.0.1.3 | CPX51 | ML Training & Inference |
| cache-server | 10.0.1.4 | CPX21 | Redis Cache & Celery Worker |

All servers communicate via private network (10.0.1.0/24) for security and performance.

## Technology Stack

### Backend
- **Python 3.12**: Core ML pipeline and API backend
- **PostgreSQL 16**: Primary database (db-server)
- **Redis**: Caching and message queue (cache-server)
- **Celery**: Distributed task queue for async processing
- **MLflow**: ML experiment tracking and model registry

### Frontend
- **Next.js**: Web UI framework (app-server)
- **Node.js 20 LTS**: JavaScript runtime

### Infrastructure
- **Nginx**: Reverse proxy and static file serving
- **Docker**: Containerization
- **Kubernetes**: Container orchestration
- **PM2**: Node.js process management
- **Prometheus**: Metrics collection (node-exporter on all servers)

## Project Structure

```
ml-stock-scanner/
├── src/
│   ├── api/          # FastAPI/Flask backend endpoints
│   ├── data/         # Data ingestion and preprocessing
│   ├── features/     # Feature engineering modules
│   ├── models/       # ML model definitions
│   ├── pipeline/     # ML training/inference pipelines
│   └── web/          # Next.js frontend application
├── config/           # Configuration files
├── deploy/
│   ├── docker/       # Dockerfiles
│   ├── kubernetes/   # K8s manifests
│   └── scripts/      # Deployment automation scripts
├── scripts/          # Utility and maintenance scripts
├── tests/            # Test suite
├── notebooks/        # Jupyter notebooks for experimentation
├── data/             # Data storage (not committed to git)
├── logs/             # Application logs
└── docs/             # Project documentation
```

## GitHub Repository

**Repository**: https://github.com/boulossidhom/ml-stock-scanner
**Owner**: boulossidhom

### GitHub Setup Scripts

All GitHub configuration scripts are in `scripts/`:

| Script | Purpose | Run On |
|--------|---------|--------|
| `setup_ssh_key.sh` | Generate SSH key for GitHub | All 4 servers |
| `configure_git.sh` | Configure Git identity | All 4 servers |
| `init_repository.sh` | Initialize and push repository | app-server only |
| `clone_repository.sh` | Clone repository | db/ml/cache servers |
| `deploy.sh` | Deploy to all servers | app-server |

See `scripts/README_GITHUB_SETUP.md` for detailed setup instructions.

### Quick GitHub Workflow

```bash
# On app-server: Make changes and deploy
cd ~/ml-stock-scanner
git add -A
git commit -m "feat: Your change description"
git push origin main
./scripts/deploy.sh  # Deploys to all other servers
```

## Development Environment Setup

### Prerequisites
All development servers must have:
- Python 3.12
- Node.js 20 LTS
- Git
- Docker (for containerized development)

### Python Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies (when requirements.txt is available)
pip install -r requirements.txt

# For ML development specifically
pip install -r requirements-ml.txt
```

### Node.js Environment
```bash
# Install dependencies (when package.json is available)
cd src/web
npm install

# Or using yarn
yarn install
```

## Server-Specific Roles

### app-server (10.0.1.1)
- Hosts Next.js frontend
- API gateway via Nginx
- Serves static assets
- Rate limiting and security

### db-server (10.0.1.2)
- PostgreSQL 16 database
- Stores stock data, model results, user data
- Configured for high-performance queries
- UTC timezone for consistent timestamps

### ml-server (10.0.1.3)
- ML model training
- Inference/prediction serving
- MLflow tracking server
- Heavy computational workloads

### cache-server (10.0.1.4)
- Redis for caching
- Celery workers for async tasks
- Message broker for distributed processing
- Session storage

## Key Design Principles

### Timezone Management
All servers are configured to UTC timezone. This ensures:
- Consistent timestamps across distributed systems
- Simplified market data handling across timezones
- Accurate log correlation

### Security
- Private network (10.0.1.0/24) for inter-server communication
- Only app-server exposed to public internet
- Database and cache servers isolated on private network
- Floating IP for high availability

### Monitoring
All servers run:
- `prometheus-node-exporter` on port 9100 for metrics
- `vnstat` for network monitoring
- System monitoring tools (htop, glances, iotop)

## Important File Locations

### Configuration Files
- Database config: `config/database.yaml` (expected)
- Redis config: `config/redis.yaml` (expected)
- ML config: `config/ml_config.yaml` (expected)
- API config: `config/api.yaml` (expected)

### Environment Variables
Expected environment variables (when code is developed):
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `ANTHROPIC_API_KEY`: For Claude Code integration
- `MLFLOW_TRACKING_URI`: MLflow server URL

## Development Workflow

### Working with Multiple Servers
When developing features that span multiple servers:
1. Develop locally first with containerized dependencies
2. Test on staging environment
3. Deploy to production servers sequentially
4. Always test db-server and cache-server before app-server
5. ml-server can be updated independently for model improvements

### Data Pipeline
1. Data ingestion (src/data/) fetches stock data
2. Feature engineering (src/features/) processes raw data
3. ML pipeline (src/pipeline/) trains/updates models
4. Models deployed via MLflow for inference
5. Results cached in Redis for fast API responses

## Documentation

Key documentation files in `docs/`:
- `Base_Software_Installation_Guide.md`: Server setup instructions
- `ML_Stock_Scanner_Phase1_Checklist.docx`: Phase 1 implementation checklist
- `ML_Stock_Scanner_Technology_Guide.docx`: Technology decisions
- `ML_Stock_Scanner_Infrastructure_Documentation.docx`: Infrastructure details
- `Git_Integration_Guide.docx`: Version control workflow
- `Hetzner_Private_Network_Setup_Guide.docx`: Network configuration
- `Hetzner_Floating_IP_HA_Setup_Guide.docx`: High availability setup

## Notes for Future Development

### When Adding New Features
- Consider which server(s) the feature affects
- Update relevant configuration files
- Ensure timezone-aware datetime handling
- Add appropriate monitoring/logging
- Document in relevant docs/ files

### Performance Considerations
- Use Redis caching for frequently accessed data
- Offload heavy computations to ml-server via Celery
- Keep API responses fast by pre-computing on ml-server
- Monitor node-exporter metrics for resource usage

### ML Model Development
- Use notebooks/ for experimentation
- Track experiments in MLflow
- Version models appropriately
- Test inference latency before deployment
- Consider model size for memory constraints
