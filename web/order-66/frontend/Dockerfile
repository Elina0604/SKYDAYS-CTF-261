# Frontend Dockerfile for Order 66 CTF Challenge
# Multi-stage build: Build with Bun, Serve with Nginx

# Build stage
FROM oven/bun:1-alpine as builder

# Set build arguments
ARG NODE_VERSION=20
ARG VITE_DEV_MODE=false

# Set environment variables for build
ENV VITE_DEV_MODE=${VITE_DEV_MODE}
ENV NODE_ENV=production

# Set work directory
WORKDIR /build

# Copy package files first for better layer caching
COPY package.json bun.lockb* ./

# Install dependencies (no --production flag for build stage)
RUN bun install --frozen-lockfile

# Copy source code
COPY . .

# Build the application
RUN bun run build

# Production stage with Nginx
FROM nginx:1.24-alpine as production

# Set build arguments
ARG NGINX_VERSION=1.24

# Copy built application from builder stage
COPY --from=builder /build/dist /usr/share/nginx/html

# Copy custom nginx configuration
COPY <<EOF /etc/nginx/conf.d/default.conf
server {
    listen 80;
    listen [::]:80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
    
    # Handle Vue.js routing (SPA)
    location / {
        try_files \$uri \$uri/ /index.html;
        
        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
            add_header X-Content-Type-Options "nosniff";
        }
        
        # No cache for HTML files
        location ~* \.html$ {
            expires -1;
            add_header Cache-Control "no-cache, no-store, must-revalidate";
            add_header Pragma "no-cache";
        }
    }
    
    # API proxy (optional, for development)
    location /api/ {
        proxy_pass http://backend:8000/api/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
    
    # Health check endpoint
    location /health {
        access_log off;
        return 200 "Order 66 Frontend Operational\n";
        add_header Content-Type text/plain;
    }
    
    # Security: Hide nginx version
    server_tokens off;
    
    # Error pages
    error_page 404 /index.html;
    error_page 500 502 503 504 /index.html;
}
EOF

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:80/health || exit 1

# Start nginx (as root, which is the default and expected)
CMD ["nginx", "-g", "daemon off;"]