#!/bin/bash

# Vader Todo API Startup Script
echo "🌟 Starting Vader Todo API..."
echo "May the Force be with your productivity!"

# Start the server
echo ""
echo "🎯 Starting Vader Todo API server..."
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🌐 API Base URL: http://localhost:8000/api"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
