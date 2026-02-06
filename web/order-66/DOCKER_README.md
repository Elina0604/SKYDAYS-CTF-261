# 🏴 Order 66: Execute the Query - Docker Setup

**A Star Wars-themed CTF challenge featuring intentional SQL injection vulnerabilities**

## 🚀 Quick Start

```bash
# 1. Quick setup (recommended)
./setup-docker.sh

# 2. Manual setup
cp .env.docker .env
docker-compose up --build
```

## 🎯 Access Your CTF Challenge

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main application interface |
| **Backend API** | http://localhost:8000 | REST API and documentation |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |
| **MySQL** | localhost:3306 | Direct database access |

## 🗄️ Database Access

### CTF Participants

```bash
# Main application user (full access)
mysql -h localhost -u vader -p
# Password: deathstar

# Limited access user  
mysql -h localhost -u empire_user -p
# Password: darkside

# Read-only reconnaissance
mysql -h localhost -u rebel_spy -p
# Password: hope
```

## 🔧 Configuration

### Environment Variables

The application uses **43 environment variables** organized into 6 categories:

- 🗄️ **MySQL Database** (8 variables)
- 🔧 **Backend API** (12 variables)  
- 🎨 **Frontend** (5 variables)
- 🔐 **Security** (6 variables)
- ⚡ **Performance** (8 variables)
- 🏴 **CTF Challenge** (4 variables)

**📖 Complete Documentation**: See [`DOCKER_ENV_GUIDE.md`](./DOCKER_ENV_GUIDE.md)

### Key Settings to Customize

```env
# Security (Change in production!)
MYSQL_ROOT_PASSWORD=emperor
MYSQL_PASSWORD=deathstar
SECRET_KEY=execute-order-66-the-empire-strikes-back

# Challenge Configuration
CTF_FLAG=SKYDAYS{SKYORDER_66_HAD_TO_EXECUTED}
CTF_FLAG_DESCRIPTION=Execute Order 66 - The hidden Imperial intelligence

# Access Ports
FRONTEND_PORT=3000
BACKEND_PORT=8000
MYSQL_EXTERNAL_PORT=3306
```

## 🏴 CTF Challenge Information

| Field | Value |
|-------|-------|
| **Name** | Order 66: Execute the Query |
| **Category** | Web Application Security |
| **Type** | SQL Injection |
| **Difficulty** | Intermediate |
| **Objective** | Extract the hidden Imperial flag from the database |
| **Vulnerability** | Boolean-based blind SQL injection in sort parameter |

### 🎯 Challenge Hints

1. **Entry Point**: Explore the todo application functionality
2. **Vulnerability Location**: The sorting feature seems suspicious...
3. **Technique**: Boolean-based blind SQL injection
4. **Target**: Extract the hidden flag from the `flags` table
5. **Flag Format**: `SKYDAYS{...}`

## 🐳 Docker Services

### Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │     MySQL       │
│   (Vue3+nginx)  │◄───┤   (FastAPI)     │◄───┤   (Database)    │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 3306    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Service Details

| Service | Technology | Purpose |
|---------|------------|---------|
| `frontend` | Vue 3 + Vite + nginx | Web interface for the todo application |
| `backend` | FastAPI + Python | REST API with intentional vulnerabilities |
| `mysql` | MySQL 8.0 | Database containing the hidden flag |

## 📁 File Structure

```
order-66/
├── docker-compose.yml          # 🐳 Main orchestration
├── setup-docker.sh             # 🚀 Quick setup script
├── .env                        # 🔧 Your configuration
├── .env.docker                 # 📋 Configuration template
├── DOCKER_ENV_GUIDE.md         # 📖 Detailed documentation
├── backend/
│   ├── Dockerfile              # 🏗️ Backend container
│   ├── .dockerignore           
│   ├── requirements.txt        # 📦 Updated with MySQL driver
│   └── app/
│       ├── config.py           # ⚙️ Enhanced configuration
│       └── database.py         # 🔄 Updated for MySQL
├── frontend/
│   ├── Dockerfile              # 🎨 Frontend container
│   └── .dockerignore           
└── docker/
    └── mysql/
        └── init.sql            # 🗄️ Database initialization
```

## 🔨 Development Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mysql

# Execute commands in containers
docker-compose exec backend bash
docker-compose exec mysql mysql -u root -p

# Rebuild specific service
docker-compose up --build backend

# Stop services
docker-compose down

# Complete cleanup
docker-compose down -v --rmi all
```

## 🔍 Monitoring & Health Checks

All services include health checks:

```bash
# Check service status
docker-compose ps

# Service health endpoints
curl http://localhost:8000/api/health  # Backend
curl http://localhost:3000/health      # Frontend
```

## 🛠️ Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Port conflicts** | Change `*_PORT` variables in `.env` |
| **Database connection failed** | Wait for MySQL startup, check logs |
| **CORS errors** | Verify `ALLOWED_ORIGINS` in `.env` |
| **Build failures** | Clean Docker cache: `docker system prune` |

### Debug Commands

```bash
# Validate configuration
docker-compose config

# Check Docker resources
docker system df

# Remove unused resources
docker system prune

# View service details
docker-compose ps -a
docker inspect order66_backend
```

## 🔐 Security Considerations

### For CTF Deployment

- ✅ **Intentionally vulnerable** (part of the challenge)
- ✅ **Database exposed** (allows direct access for flag extraction)
- ✅ **Default credentials** (documented for participants)

### For Production Use

If adapting this code for production:

- 🚨 **Remove SQL injection vulnerabilities**
- 🚨 **Change all default passwords**
- 🚨 **Restrict database access**
- 🚨 **Use proper secret management**
- 🚨 **Enable HTTPS with SSL certificates**

## 📊 Resource Requirements

| Service | CPU | Memory | Storage |
|---------|-----|--------|---------|
| Frontend | 0.1 CPU | 128MB | 50MB |
| Backend | 0.2 CPU | 256MB | 100MB |
| MySQL | 0.2 CPU | 512MB | 1GB |
| **Total** | **0.5 CPU** | **896MB** | **1.15GB** |

## 🎓 Educational Value

This setup demonstrates:

- **Containerization** with Docker and Docker Compose
- **Multi-service architecture** with proper networking
- **Environment-based configuration** with 43 variables
- **Security vulnerabilities** in web applications
- **Database security** and access controls
- **Modern web development** with Vue 3 and FastAPI

## 🤝 Contributing

To modify or enhance the challenge:

1. **Environment Variables**: Edit `.env` or update `backend/app/config.py`
2. **Database Schema**: Modify `docker/mysql/init.sql`
3. **Application Logic**: Update `backend/app/` or `frontend/src/`
4. **Container Configuration**: Edit Dockerfiles or `docker-compose.yml`

## 📚 References

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [MySQL Docker Image](https://hub.docker.com/_/mysql)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vue.js Documentation](https://vuejs.org/)

---

**🏴 May the Force be with you in this challenge!**

*Execute Order 66... and extract the hidden intelligence from the Empire's database.*