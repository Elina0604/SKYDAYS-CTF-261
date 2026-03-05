# Order 66 Setup Guide

## Quick Start (Development)

```bash
# Clone repository
git clone <repository>
cd order-66

# Start all services (uses docker-compose.override.yml automatically)
docker-compose up -d

# Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Database: localhost:3306
```

## Production Deployment

```bash
# Clone repository
git clone <repository>
cd order-66

# Create production environment file
cp .env.example .env
# Edit .env with production values

# Start services (production defaults, no override)
docker-compose up -d

# Access application via nginx
# Frontend: http://your-domain.com
# Backend: http://your-domain.com/api
```

## Environment Variables

See `.env.example` for all available environment variables.

### Key Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CTF_FLAG` | The CTF flag to discover | `SKYDAYS{SKYORDER_66_HAD_TO_EXECUTED}` |
| `MYSQL_ROOT_PASSWORD` | Database root password | `emperor` |
| `SECRET_KEY` | JWT secret key | (insecure default) |
| `DEBUG` | Enable debug mode | `false` |
| `LOG_LEVEL` | Logging level | `info` |

## Development vs Production

- **Development**: Uses `docker-compose.override.yml` which exposes ports and enables debug mode
- **Production**: Uses defaults from `docker-compose.yml` with no exposed ports except nginx

## Troubleshooting

```bash
# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild containers
docker-compose build --no-cache
docker-compose up -d

# Access database directly
docker-compose exec mysql mysql -u vader -p empire_todos
```
