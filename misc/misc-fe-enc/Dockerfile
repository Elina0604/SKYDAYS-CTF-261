# Multi-stage build for minimal production image
# Build stage using Bun (lighter than Node.js)
FROM oven/bun:1.3-slim AS builder

WORKDIR /app

    # Copy package files and install dependencies
    COPY package.json bun.lock ./
    RUN bun install

# Copy source code and build
COPY . .
RUN bun run build

# Production stage using minimal nginx alpine
FROM nginx:alpine AS production

# Remove default nginx content
RUN rm -rf /usr/share/nginx/html/*

# Copy built application from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Create custom nginx config for SPA (React Router support)
RUN echo 'server {' > /etc/nginx/conf.d/default.conf && \
    echo '    listen 80;' >> /etc/nginx/conf.d/default.conf && \
    echo '    server_name localhost;' >> /etc/nginx/conf.d/default.conf && \
    echo '    root /usr/share/nginx/html;' >> /etc/nginx/conf.d/default.conf && \
    echo '    index index.html;' >> /etc/nginx/conf.d/default.conf && \
    echo '    location / {' >> /etc/nginx/conf.d/default.conf && \
    echo '        try_files $uri $uri/ /index.html;' >> /etc/nginx/conf.d/default.conf && \
    echo '    }' >> /etc/nginx/conf.d/default.conf && \
    echo '    # Disable access logs for CTF (reduces container size)' >> /etc/nginx/conf.d/default.conf && \
    echo '    access_log off;' >> /etc/nginx/conf.d/default.conf && \
    echo '    error_log /var/log/nginx/error.log error;' >> /etc/nginx/conf.d/default.conf && \
    echo '}' >> /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]

# Alternative development stage (uncomment to use)
# FROM oven/bun:1.3-slim AS development
# WORKDIR /app
# COPY package.json bun.lock* ./
# RUN bun install
# COPY . .
# EXPOSE 3000
# CMD ["bun", "run", "dev", "--host", "0.0.0.0"]