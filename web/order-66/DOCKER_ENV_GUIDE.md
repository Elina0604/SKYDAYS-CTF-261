# 🏴 Order 66: Docker Environment Variables Guide

Complete documentation for configuring your dockerized Star Wars CTF challenge application.

## 📋 Quick Start

```bash
# 1. Copy the environment template
cp .env.docker .env

# 2. Build and start all services
docker-compose up --build

# 3. Access your application
Frontend: http://localhost:3000
Backend API: http://localhost:8000
MySQL Database: localhost:3306
```

## 🎯 CTF Challenge Access

- **Frontend Application**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Database Access**: `mysql -h localhost -u vader -p` (password: `deathstar`)
- **Challenge Flag**: Hidden in the database (extractable via SQL injection)

---

## 📊 Environment Variables Overview

**Total Variables**: 43 organized into 6 categories

| Category | Variables | Purpose |
|----------|-----------|---------|
| 🗄️ MySQL Database | 8 | Database connection and configuration |
| 🔧 Backend API | 12 | FastAPI server and API settings |
| 🎨 Frontend | 5 | Vue.js application and nginx serving |
| 🔐 Security | 6 | Authentication, encryption, and secrets |
| ⚡ Performance | 8 | Scaling, timeouts, and resource limits |
| 🏴 CTF Challenge | 4 | Challenge-specific configuration |

---

## 🗄️ MySQL Database Configuration

### Core Database Settings

| Variable | Default | Description | Required |
|----------|---------|-------------|----------|
| `MYSQL_ROOT_PASSWORD` | `emperor` | MySQL root user password | ✅ **YES** |
| `MYSQL_DATABASE` | `empire_todos` | Database name for the application | ✅ **YES** |
| `MYSQL_USER` | `vader` | MySQL user for the application | ✅ **YES** |
| `MYSQL_PASSWORD` | `deathstar` | Password for the application user | ✅ **YES** |

### Access Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `MYSQL_EXTERNAL_PORT` | `3306` | External port for database access (CTF participants) |

### 🔒 Security Recommendations

**🚨 PRODUCTION WARNING**: Change default passwords!

```env
# Use strong, unique passwords in production
MYSQL_ROOT_PASSWORD=your-super-secure-root-password-here
MYSQL_PASSWORD=your-secure-app-password-here
```

### 💡 CTF Optimization

The database is configured for **easy CTF access**:
- **Multiple users** with different permission levels
- **Exposed port** (3306) for direct database connections
- **Additional users**: `empire_user` (read/write), `rebel_spy` (read-only)

---

## 🔧 Backend API Configuration

### Server Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `API_HOST` | `0.0.0.0` | Backend server bind address |
| `API_PORT` | `8000` | Backend server port |
| `API_PREFIX` | `/api` | API path prefix |
| `BACKEND_PORT` | `8000` | External port for backend service |

### Framework Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `PYTHON_VERSION` | `3.11` | Python version for Docker build |
| `FRONTEND_URL` | `http://localhost:3000` | Frontend URL for CORS |
| `ALLOWED_ORIGINS` | `["http://localhost:3000","http://frontend:3000"]` | CORS allowed origins (JSON array) |

### Environment Detection

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `production` | Environment type (development/staging/production) |
| `DEBUG` | `false` | Enable debug mode |
| `LOG_LEVEL` | `info` | Logging level (debug/info/warning/error/critical) |

---

## 🎨 Frontend Configuration

### Build Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_URL` | `http://localhost:8000/api` | Backend API URL for frontend |
| `VITE_DEV_MODE` | `false` | Enable development mode features |

### Container Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `FRONTEND_PORT` | `3000` | External port for frontend service |
| `NODE_VERSION` | `20` | Node.js version for Docker build |
| `NGINX_VERSION` | `1.24` | Nginx version for serving |

---

## 🔐 Security & Authentication

### JWT Configuration

| Variable | Default | Description | Required |
|----------|---------|-------------|----------|
| `SECRET_KEY` | `execute-order-66-the-empire-strikes-back` | JWT signing key | ✅ **YES** |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | JWT token expiration time | No |
| `ALGORITHM` | `HS256` | JWT signing algorithm | No |

### 🔒 Security Best Practices

**🚨 PRODUCTION CRITICAL**: Generate a secure secret key!

```bash
# Generate a secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

```env
# Use the generated key
SECRET_KEY=your-generated-secure-secret-key-here
```

---

## ⚡ Performance & Scaling Configuration

### Worker Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `WORKER_PROCESSES` | `1` | Number of uvicorn worker processes |
| `WORKER_CONNECTIONS` | `1000` | Maximum connections per worker |

### Timeout Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `KEEPALIVE_TIMEOUT` | `2` | Keep-alive timeout (seconds) |
| `REQUEST_TIMEOUT` | `30` | Request timeout (seconds) |
| `MAX_REQUEST_SIZE` | `16777216` | Maximum request size (bytes, 16MB) |

### Health Checks

| Variable | Default | Description |
|----------|---------|-------------|
| `HEALTH_CHECK_INTERVAL` | `30` | Health check interval (seconds) |
| `HEALTH_CHECK_TIMEOUT` | `5` | Health check timeout (seconds) |
| `HEALTH_CHECK_RETRIES` | `3` | Health check retry attempts |

---

## 🏴 CTF Challenge Configuration

### Challenge Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `CTF_FLAG` | `SKYDAYS{SKYORDER_66_HAD_TO_EXECUTED}` | The hidden flag in the database |
| `CTF_FLAG_DESCRIPTION` | `Execute Order 66 - The hidden Imperial intelligence` | Flag description |

### Challenge Features

| Variable | Default | Description |
|----------|---------|-------------|
| `ENABLE_SAMPLE_DATA` | `true` | Insert sample todos and CTF data |
| `ENABLE_CTF_ENDPOINTS` | `true` | Enable CTF-specific API endpoints |

### 🎯 Customizing Your CTF

```env
# Change the flag for your specific CTF event
CTF_FLAG=YOURCTF{YOUR_CUSTOM_FLAG_HERE}
CTF_FLAG_DESCRIPTION=Your custom challenge description
```

---

## 📁 File Structure

```
order-66/
├── docker-compose.yml          # Main orchestration file
├── .env                        # Your environment configuration
├── .env.docker                 # Environment template (this file)
├── backend/
│   ├── Dockerfile              # Backend container definition
│   ├── .dockerignore           # Backend build exclusions
│   └── requirements.txt        # Python dependencies (updated)
├── frontend/
│   ├── Dockerfile              # Frontend container definition
│   └── .dockerignore           # Frontend build exclusions
└── docker/
    └── mysql/
        └── init.sql            # Database initialization script
```

---

## 🚀 Common Deployment Scenarios

### 1. Local CTF Development

```env
DEBUG=true
LOG_LEVEL=debug
VITE_DEV_MODE=true
ENVIRONMENT=development
```

### 2. CTF Competition Production

```env
DEBUG=false
LOG_LEVEL=info
ENVIRONMENT=production
# Change all default passwords!
MYSQL_ROOT_PASSWORD=your-secure-password
MYSQL_PASSWORD=your-secure-password
SECRET_KEY=your-generated-secret-key
```

### 3. Multi-Instance Scaling

```env
WORKER_PROCESSES=4
WORKER_CONNECTIONS=2000
MAX_REQUEST_SIZE=33554432  # 32MB
```

---

## 🔧 Advanced Configuration

### Database Connection Override

Use a custom database connection string:

```env
# This takes precedence over individual MySQL settings
DATABASE_URL=mysql+pymysql://user:pass@host:port/database?charset=utf8mb4
```

### CORS Customization

```env
ALLOWED_ORIGINS=["https://yourctf.com","https://ctf-platform.com"]
ALLOW_METHODS=["GET","POST","PUT","DELETE"]
ALLOW_HEADERS=["Content-Type","Authorization","X-Custom-Header"]
```

### Custom Application Settings

```env
APP_NAME=Your Custom CTF Challenge Name
APP_VERSION=2.0.0-CUSTOM
```

---

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```bash
   # Check if MySQL is ready
   docker-compose logs mysql
   
   # Verify environment variables
   docker-compose config
   ```

2. **Frontend Can't Connect to Backend**
   ```env
   # Ensure API URL is correct
   VITE_API_URL=http://localhost:8000/api
   ```

3. **CORS Errors**
   ```env
   # Add your frontend URL to allowed origins
   ALLOWED_ORIGINS=["http://localhost:3000","https://yourdomain.com"]
   ```

### Logs and Monitoring

```bash
# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mysql

# Check service health
docker-compose ps
```

---

## 📚 Additional Resources

- **Docker Compose Documentation**: https://docs.docker.com/compose/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Vue.js Documentation**: https://vuejs.org/
- **MySQL Documentation**: https://dev.mysql.com/doc/

---

## 🏴 CTF Challenge Information

**Challenge Name**: Order 66: Execute the Query  
**Category**: Web Application Security / SQL Injection  
**Difficulty**: Intermediate  
**Flag Location**: Hidden in the MySQL database  
**Vulnerability**: SQL injection in the sorting parameter  

**Objective**: Extract the hidden Imperial intelligence (flag) from the Empire's task management database using SQL injection techniques.

---

*May the Source be with you! 🌟*