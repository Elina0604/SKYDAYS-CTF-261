# Backend Dockerfile for Order 66 CTF Challenge
# Optimized build for PyMySQL compatibility

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH="/app"

# Install minimal system dependencies for PyMySQL and runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create app user for security
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Create app directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
# Use pure Python MySQL driver (no C extensions needed)
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

# Verify PyMySQL installation
RUN python -c "import pymysql; print(f'✅ PyMySQL {pymysql.__version__} installed successfully')"

# Copy application code
COPY . .

# Set ownership to app user
RUN chown -R appuser:appgroup /app

# Create startup script with enhanced debugging
RUN cat > /app/start.sh << 'EOF'
#!/bin/bash
set -e

echo "🏴 Order 66: Preparing the Empire's systems..."

# Debug information
echo "🔍 Python version: $(python --version)"
echo "🔍 Python path: $PYTHONPATH"
echo "🔍 Working directory: $(pwd)"

# Test PyMySQL import
echo "🔍 Testing PyMySQL import..."
python -c "
try:
    import pymysql
    print(f'✅ PyMySQL version: {pymysql.__version__}')
    print(f'✅ PyMySQL location: {pymysql.__file__}')
except ImportError as e:
    print(f'❌ PyMySQL import failed: {e}')
    exit(1)
"

# Test application imports
echo "🔍 Testing application imports..."
python -c "
try:
    from app.config import settings
    print(f'✅ Config loaded successfully')
    print(f'✅ Database URL: {settings.get_database_url()}')
except Exception as e:
    print(f'❌ Config import failed: {e}')
    import traceback
    traceback.print_exc()
    exit(1)
"

# Wait for database to be ready
echo "⏳ Waiting for database connection..."
while ! nc -z ${MYSQL_HOST:-mysql} ${MYSQL_PORT:-3306}; do
    echo "⏳ Database not ready yet. Waiting..."
    sleep 2
done
echo "✅ Database is ready!"

# Start the application
echo "🚀 Starting Order 66 CTF Challenge..."
exec uvicorn app.main:app \
    --host ${API_HOST:-0.0.0.0} \
    --port ${API_PORT:-8000} \
    --workers ${WORKER_PROCESSES:-1} \
    --log-level ${LOG_LEVEL:-info} \
    --access-log \
    --no-use-colors
EOF

# Make startup script executable
RUN chmod +x /app/start.sh

# Switch to app user
USER appuser

# Expose port
EXPOSE 8000

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Default command
CMD ["/app/start.sh"]