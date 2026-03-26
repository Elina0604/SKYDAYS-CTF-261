# 🚀 Order 66 CTF - Deployment Guide

This guide provides step-by-step instructions for deploying the Order 66 CTF challenge application with nginx reverse proxy routing.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Architecture Overview](#architecture-overview)
- [Detailed Deployment Steps](#detailed-deployment-steps)
- [Configuration](#configuration)
- [SSL/HTTPS Setup](#ssl-https-setup)
- [Testing & Verification](#testing--verification)
- [Troubleshooting](#troubleshooting)
- [Production Considerations](#production-considerations)

## 🔧 Prerequisites

### System Requirements
- **Docker**: Version 20.10+ 
- **Docker Compose**: Version 2.0+
- **Operating System**: Linux, macOS, or Windows with WSL2
- **Memory**: Minimum 2GB RAM
- **Storage**: Minimum 5GB free space

### Network Requirements
- Access to ports 80 and 443
- Internet connection for Docker image downloads
- Domain name (for production) or hosts file modification (for development)

### Required Tools
```bash
# Check Docker installation
docker --version
docker-compose --version

# Install required tools (Ubuntu/Debian)
sudo apt update
sudo apt install curl jq openssl

# Install required tools (macOS)
brew install curl jq openssl
```

## ⚡ Quick Start

For a quick deployment with default settings:

```bash
# 1. Clone or navigate to the project directory
cd /path/to/order-66

# 2. Add domain to hosts file (for local development)
echo "127.0.0.1 order66.skydays.ctf" | sudo tee -a /etc/hosts

# 3. Create environment configuration file
cp .env.example .env

# 4. Start all services
# This uses runtime environment variables declared in .env
docker-compose up -d

# Wait for services to initialize (30-60 seconds)
sleep 60

# 5. Access the application
open https://order66.skydays.ctf/
```

## 🏗️ Architecture Overview

The application consists of 4 main services:

```
┌─────────────────┐    ┌─────────────────┐
│   Browser       │───▶│  Nginx Proxy    │ Port 80/443
│                 │    │  (SSL/Routing)  │
└─────────────────┘    └─────────────────┘
                                │
                       ┌────────┴────────┐
                       ▼                 ▼
              ┌─────────────────┐ ┌─────────────────┐
              │  Vue.js         │ │  FastAPI        │
              │  Frontend       │ │  Backend        │ Port 8000
              │                 │ │                 │ (internal)
              └─────────────────┘ └─────────────────┘
                                          │
                                          ▼
                                 ┌─────────────────┐
                                 │  MySQL 8.0      │ Port 3306
                                 │  Database       │ (internal)
                                 └─────────────────┘
```

### Service Details

| Service | Technology | Port | Purpose |
|---------|------------|------|---------|
| **nginx** | Nginx 1.24 | 80/443 | Reverse proxy, SSL termination, routing |
| **frontend** | Vue.js 3 + Nginx | 80 (internal) | Single Page Application |
| **backend** | FastAPI + Python | 8000 (internal) | REST API, CTF logic |
| **mysql** | MySQL 8.0 | 3306 (internal) | Database storage |

## 📝 Detailed Deployment Steps

### Step 1: Environment Preparation

1. **Create project directory** (if deploying fresh):
```bash
mkdir order-66-ctf
cd order-66-ctf
# Copy all project files here
```

2. **Set up environment variables**:
```bash
# Copy example environment file
cp .env.example .env

# Edit environment variables (optional)
nano .env
```

3. **Configure domain name**:

For **development/local deployment**:
```bash
# Add to /etc/hosts (Linux/macOS)
echo "127.0.0.1 order66.skydays.ctf" | sudo tee -a /etc/hosts

# On Windows, edit C:\Windows\System32\drivers\etc\hosts
# Add line: 127.0.0.1 order66.skydays.ctf
```

For **production deployment**:
- Configure DNS A record pointing to your server IP
- Update domain in `nginx/conf.d/default.conf`
- Update `VITE_API_URL` in .env file.

### Step 2: SSL Certificate Generation

The application uses self-signed certificates by default. Generate them:

```bash
# Generate SSL certificates
./nginx/scripts/generate-certs.sh

# Verify certificates were created
ls -la nginx/ssl/
```

For **production**, replace with valid certificates:
```bash
# Copy your certificates
cp /path/to/your/cert.pem nginx/ssl/cert.pem
cp /path/to/your/key.pem nginx/ssl/key.pem

# Set proper permissions
chmod 644 nginx/ssl/cert.pem
chmod 600 nginx/ssl/key.pem
```

### Step 3: Start Services

**Start all services**:
```bash
# Ensure .env is configured with your runtime variables
docker-compose up -d

# Or start with logs (for debugging)
docker-compose up
```

**Verify services are running**:
```bash
# Check service status
docker-compose ps

# Expected output should show all services as healthy
```
## ⚙️ Configuration

### Runtime Environment Variables

Key environment variables for runtime configuration are provided in the `.env` file. These variables are substituted at container startup by `entrypoint.sh` and `envsubst`.

Example `.env` file:
```shell
# Frontend Configuration
VITE_API_URL=https://order66.skydays.ctf/api  # API endpoint for frontend

# Backend Configuration
DATABASE_URL=mysql+pymysql://vader:deathstar@mysql:3306/empire_todos
FRONTEND_URL=https://order66.skydays.ctf
ALLOWED_ORIGINS=["https://order66.skydays.ctf","http://order66.skydays.ctf"]

# Security
SECRET_KEY=execute-order-66-the-empire-strikes-back
CTF_FLAG=SKYDAYS{SKYORDER_66_HAD_TO_EXECUTED}

# Database
MYSQL_ROOT_PASSWORD=emperor
MYSQL_DATABASE=empire_todos
MYSQL_USER=vader
MYSQL_PASSWORD=deathstar
```

### Nginx Configuration

Main configuration files:
- `nginx/nginx.conf` - Main nginx config
- `nginx/conf.d/default.conf` - Server blocks and routing rules

Key routing rules:
```nginx
# API Backend (all /api/* requests)
location /api/ {
    proxy_pass http://backend:8000/api/;
    # ... proxy headers and settings
}

# Frontend (everything else)
location / {
    proxy_pass http://frontend;
    # ... SPA routing support
}
```

### Custom Domain Configuration

To use a different domain:

1. **Update nginx configuration**:
```bash
# Edit nginx/conf.d/default.conf
sed -i 's/order66.skydays.ctf/your-domain.com/g' nginx/conf.d/default.conf
```

## ✅ Testing & Verification

### Automated Testing Script

Use the provided `test-runtime-config.sh` script to verify deployment:
```bash
sudo bash ./test-runtime-config.sh
```

For runtime configuration, the script ensures:
1. The `VITE_API_URL` variable is correctly substituted.
2. The application routes to the API URL successfully.
3. Health checks and API endpoints return valid responses.

### Manual Testing Steps
1. **Access the application**:
```bash
# Open in browser
open https://order66.skydays.ctf/

# Or test with curl
curl -k https://order66.skydays.ctf/
```

2. **Test API endpoints**:
```bash
# Health check
curl -k https://order66.skydays.ctf/api/health

# Get todos
curl -k https://order66.skydays.ctf/api/todos

# Get challenge info
curl -k https://order66.skydays.ctf/api/info
```

## 🔧 Troubleshooting

### Common Issues

#### "Runtime Configuration Not Applied"
If the application does not reflect environment changes:
```bash
# Ensure you restarted services
sudo docker-compose down && docker-compose up -d

# Verify entrypoint script executed
sudo docker logs <frontend_container_id>

# Check if .env variables are correct
cat .env
```

---

**Happy Hacking! May the Force be with you! 🌟**

*"Execute Order 66 - Deploy the Empire's finest CTF challenge!"*