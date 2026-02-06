#!/bin/bash
# Order 66 Docker Setup Script
# Quick setup and deployment for the CTF challenge

set -e

echo "🏴 Order 66: Execute the Query - Docker Setup"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    print_warning ".env file not found. Creating from template..."
    cp .env.docker .env
    print_success ".env file created from template"
    print_warning "Please review and modify .env file with your desired settings"
    echo ""
    echo "Key settings to review:"
    echo "  - MYSQL_ROOT_PASSWORD (default: emperor)"
    echo "  - MYSQL_PASSWORD (default: deathstar)"  
    echo "  - SECRET_KEY (default: execute-order-66-the-empire-strikes-back)"
    echo "  - CTF_FLAG (default: SKYDAYS{SKYORDER_66_HAD_TO_EXECUTED})"
    echo ""
    read -p "Press Enter to continue with default settings or Ctrl+C to exit and modify .env..."
fi

print_status "Building and starting Order 66 CTF Challenge..."

# Build and start services
if docker-compose up --build -d; then
    print_success "All services started successfully!"
    
    echo ""
    echo "🎯 CTF Challenge is now running!"
    echo "================================"
    echo ""
    echo "📱 Frontend Application:"
    echo "   http://localhost:3000"
    echo ""
    echo "🔧 Backend API:"
    echo "   http://localhost:8000"
    echo "   Documentation: http://localhost:8000/docs"
    echo ""
    echo "🗄️ MySQL Database:"
    echo "   Host: localhost"
    echo "   Port: 3306"
    echo "   Database: empire_todos"
    echo "   User: vader"
    echo "   Password: deathstar"
    echo ""
    echo "🏴 CTF Challenge Info:"
    echo "   Challenge: Order 66: Execute the Query"
    echo "   Category: SQL Injection"
    echo "   Difficulty: Intermediate"
    echo "   Objective: Extract the hidden flag from the database"
    echo "   Hint: Try the sorting functionality..."
    echo ""
    echo "🔍 Database Access Examples:"
    echo "   mysql -h localhost -u vader -p"
    echo "   mysql -h localhost -u empire_user -p"
    echo "   mysql -h localhost -u rebel_spy -p"
    echo ""
    
    # Wait for services to be ready
    print_status "Waiting for services to be ready..."
    sleep 10
    
    # Check service health
    if docker-compose ps | grep -q "Up"; then
        print_success "Services are running!"
        
        # Test API endpoint
        if curl -f -s http://localhost:8000/api/health > /dev/null; then
            print_success "Backend API is responding"
        else
            print_warning "Backend API might still be starting up..."
        fi
        
        # Test frontend
        if curl -f -s http://localhost:3000 > /dev/null; then
            print_success "Frontend is responding"
        else
            print_warning "Frontend might still be starting up..."
        fi
        
    else
        print_warning "Some services might be starting up..."
    fi
    
    echo ""
    print_success "Order 66 CTF Challenge deployment complete!"
    echo ""
    echo "🚀 Next Steps:"
    echo "  1. Open http://localhost:3000 in your browser"
    echo "  2. Explore the application and find the vulnerability"
    echo "  3. Use SQL injection to extract the hidden flag"
    echo "  4. Check logs with: docker-compose logs -f"
    echo ""
    echo "🛑 To stop the challenge:"
    echo "  docker-compose down"
    echo ""
    echo "🧹 To clean up completely:"
    echo "  docker-compose down -v --rmi all"
    
else
    print_error "Failed to start services. Check the logs:"
    echo "docker-compose logs"
    exit 1
fi