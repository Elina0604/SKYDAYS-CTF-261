# Order 66 CTF - Nginx Routing Setup

This document explains the nginx reverse proxy configuration for the Order 66 CTF challenge.

## Architecture

The nginx reverse proxy provides clean routing for:

- **Frontend**: `https://order66.skydays.ctf/` → Vue.js application
- **Backend API**: `https://order66.skydays.ctf/api/` → FastAPI backend

## Local Development Setup

### 1. Add Domain to Hosts File

Add this entry to your `/etc/hosts` file (on macOS/Linux) or `C:\Windows\System32\drivers\etc\hosts` (on Windows):

```
127.0.0.1 order66.skydays.ctf
```

### 2. Start the Services

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

### 3. Access the Application

- **Frontend**: https://order66.skydays.ctf/
- **Backend API**: https://order66.skydays.ctf/api/
- **API Health Check**: https://order66.skydays.ctf/api/health
- **Nginx Health Check**: https://order66.skydays.ctf/nginx-health

## SSL Certificates

The setup uses self-signed SSL certificates for HTTPS support:

- **Certificate**: `nginx/ssl/cert.pem`
- **Private Key**: `nginx/ssl/key.pem`

### Browser Security Warning

Since we use self-signed certificates, your browser will show a security warning. This is normal for development:

1. Click **"Advanced"**
2. Click **"Proceed to order66.skydays.ctf (unsafe)"**

### Regenerate Certificates

If you need to regenerate the SSL certificates:

```bash
./nginx/scripts/generate-certs.sh
```

## Configuration Files

### Nginx Structure

```
nginx/
├── nginx.conf              # Main nginx configuration
├── conf.d/
│   └── default.conf        # Server blocks and routing rules
├── ssl/
│   ├── cert.pem           # SSL certificate
│   └── key.pem            # SSL private key
└── scripts/
    └── generate-certs.sh   # Certificate generation script
```

### Key Features

- **HTTPS Redirect**: All HTTP requests redirect to HTTPS
- **Rate Limiting**: API and general request rate limiting
- **Security Headers**: Comprehensive security headers
- **CORS Support**: Proper CORS handling for API requests
- **Static Asset Caching**: Optimized caching for frontend assets
- **Health Checks**: Built-in health monitoring endpoints

## Service Ports

| Service | Internal Port | External Access |
|---------|---------------|-----------------|
| Nginx   | 80/443        | All traffic     |
| Frontend| 80 (internal) | Via nginx only  |
| Backend | 8000 (internal) | Via nginx only |
| MySQL   | 3306 (internal) | Internal only |

## Troubleshooting

### Check Service Status

```bash
# View all service logs
docker-compose logs

# View specific service logs
docker-compose logs nginx
docker-compose logs frontend
docker-compose logs backend

# Check nginx configuration
docker-compose exec nginx nginx -t
```

### Test Endpoints

```bash
# Test HTTPS redirect
curl -I http://order66.skydays.ctf/

# Test frontend (should return HTML)
curl -k https://order66.skydays.ctf/

# Test API (should return health status)
curl -k https://order66.skydays.ctf/api/health

# Test nginx health
curl -k https://order66.skydays.ctf/nginx-health
```

### Common Issues

1. **"Connection refused"**: Ensure the domain is in your hosts file
2. **SSL warnings**: Normal for self-signed certificates - proceed anyway
3. **404 on API calls**: Check backend service is running and healthy
4. **CORS errors**: Check browser console and backend ALLOWED_ORIGINS

## Development vs Production

This setup is configured for local development with:

- Self-signed SSL certificates
- Docker internal networking
- Development-friendly CORS settings

For production deployment, consider:

- Valid SSL certificates (Let's Encrypt)
- Enhanced security headers
- Stricter CORS policies
- Load balancing configuration
- Monitoring and logging improvements

## Security Features

- **TLS 1.2/1.3 only**
- **Security headers** (HSTS, CSP, X-Frame-Options, etc.)
- **Rate limiting** (API: 10 req/s, General: 30 req/s)
- **Request size limits** (16MB max)
- **Server tokens disabled**

## CTF Challenge Integration

The nginx setup preserves all CTF challenge functionality while providing:

- Clean URLs for better user experience
- HTTPS security for realistic scenario
- Proper API routing for the SQL injection challenge
- Health monitoring for service reliability