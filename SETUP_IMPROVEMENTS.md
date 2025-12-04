# Setup Improvements

Summary of infrastructure and configuration upgrades made to the project template.

---

## Docker Compose Split

The project now uses a multi-file Docker Compose setup:

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Base configuration (shared) |
| `docker-compose.dev.yml` | Development overrides |
| `docker-compose.prod.yml` | Production overrides |

**Development:**
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

**Production:**
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## Key Changes

### Build Optimization
- Added `.dockerignore` files to backend and frontend
- Excludes `node_modules`, `__pycache__`, `.git`, logs from build context
- Results in faster builds and smaller images

### Container Management
- All services now have explicit `container_name` (e.g., `project1-backend`)
- Health checks added to all services
- Resource limits set (memory + CPU)

### Nginx Improvements
- Gzip compression enabled
- Security headers added (X-Frame-Options, X-Content-Type-Options, etc.)
- Removed duplicate config entries
- Separate `nginx.prod.conf` with static file caching

### Migrations
- `makemigrations` removed from container startup
- Run manually when needed:
  ```bash
  docker exec -it project1-backend python manage.py makemigrations
  ```

### Git Tracking
- `__init__.py` files now tracked (Python packages)
- `package-lock.json` now tracked (npm reproducibility)

---

## Container Names

| Service | Container Name |
|---------|----------------|
| Nginx | `project1-nginx` |
| Backend | `project1-backend` |
| Frontend | `project1-frontend` |
| PostgreSQL | `project1-postgres` |

---

## Resource Limits

| Service | Memory | CPU |
|---------|--------|-----|
| nginx | 128M | 0.25 |
| backend | 512M | 0.5 |
| frontend | 1G | 1 |
| postgres | 256M | 0.25 |

