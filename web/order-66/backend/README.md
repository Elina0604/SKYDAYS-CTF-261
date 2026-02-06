# Vader Todo API

A Star Wars themed todo API built with FastAPI. May the Force be with your productivity!

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
cd backend

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Run the server
uvicorn app.main:app --reload

# The API will be available at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_todos.py -v
```

## 📚 API Endpoints

### Health & Info

- **GET** `/` - Welcome message
- **GET** `/api/health` - Health check
- **GET** `/api/info` - API information

### Todos

- **GET** `/api/todos` - List todos with filtering and sorting
- **POST** `/api/todos` - Create new todo
- **GET** `/api/todos/{id}` - Get specific todo
- **PUT** `/api/todos/{id}` - Update todo
- **DELETE** `/api/todos/{id}` - Delete todo
- **PUT** `/api/todos/{id}/toggle` - Toggle completion status
- **PUT** `/api/todos/{id}/priority` - Update priority
- **DELETE** `/api/todos/completed` - Clear all completed todos
- **GET** `/api/todos/stats` - Get todo statistics

### Preferences

- **GET** `/api/preferences` - Get global preferences
- **PUT** `/api/preferences` - Update preferences
- **POST** `/api/preferences/reset` - Reset to defaults

## 🔧 Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=sqlite:///./vader_todos.db
# For PostgreSQL: postgresql://user:pass@localhost/vader_todos

# CORS
FRONTEND_URL=http://localhost:5173
ALLOWED_ORIGINS=["http://localhost:5173"]

# Optional
DEBUG=true
LOG_LEVEL=info
```

### Database Support

- **SQLite** - Perfect for development and single-user deployments
- **PostgreSQL** - Recommended for production

## 📖 API Examples

### Create a Todo

```bash
curl -X POST "http://localhost:8000/api/todos" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Complete the Death Star plans",
       "priority": "high"
     }'
```

### Get Todos with Filtering

```bash
# Get active todos, sorted by priority
curl "http://localhost:8000/api/todos?filter=active&sort=priority&order=desc"

# Get completed todos
curl "http://localhost:8000/api/todos?filter=completed"

# Paginated results
curl "http://localhost:8000/api/todos?limit=10&offset=0"
```

### Update Todo

```bash
curl -X PUT "http://localhost:8000/api/todos/{todo-id}" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Updated: Find the rebel base",
       "completed": true,
       "priority": "medium"
     }'
```

### Toggle Completion

```bash
curl -X PUT "http://localhost:8000/api/todos/{todo-id}/toggle"
```

### Update Preferences

```bash
curl -X PUT "http://localhost:8000/api/preferences" \
     -H "Content-Type: application/json" \
     -d '{
       "sort_field": "priority",
       "sort_order": "asc",
       "sound_effects_enabled": false,
       "theme": "light"
     }'
```

## 🎯 Features

### Core Features
- ✅ **Complete CRUD operations** for todos
- ✅ **Advanced filtering** (all, active, completed)  
- ✅ **Flexible sorting** (name, date, priority)
- ✅ **Priority levels** (low, medium, high)
- ✅ **Completion tracking** with timestamps
- ✅ **Global preferences** persistence
- ✅ **Statistics and analytics**

### Technical Features
- ✅ **Automatic API documentation** with Swagger/ReDoc
- ✅ **Type-safe** with Pydantic models
- ✅ **Comprehensive error handling** with Star Wars themed messages
- ✅ **Input validation** and sanitization
- ✅ **CORS support** for frontend integration
- ✅ **Comprehensive test suite** with pytest
- ✅ **Database migrations** ready (Alembic)

### Star Wars Features
- ⭐ **Vader-themed error messages** ("I find your lack of faith disturbing")
- ⭐ **Star Wars API descriptions** and documentation
- ⭐ **Force-powered health checks** 
- ⭐ **Imperial efficiency** in code organization

## 🚀 Deployment

### Local Development
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
# Using Gunicorn + Uvicorn workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Using Docker
docker build -t vader-todo-api .
docker run -p 8000:8000 vader-todo-api
```

### Database Setup

For PostgreSQL:
```bash
# Create database
createdb vader_todos

# Set DATABASE_URL in .env
DATABASE_URL=postgresql://user:pass@localhost/vader_todos

# Run migrations (if using Alembic)
alembic upgrade head
```

## 📊 API Response Examples

### Todo Response
```json
{
  "id": "uuid-v4",
  "text": "Complete the Death Star plans",
  "completed": false,
  "priority": "high", 
  "created_at": "2026-02-01T10:30:00.000Z",
  "updated_at": "2026-02-01T10:30:00.000Z",
  "completed_at": null
}
```

### Todo List Response
```json
{
  "todos": [...],
  "total": 25,
  "stats": {
    "active": 15,
    "completed": 10,
    "total": 25,
    "by_priority": {
      "high": 5,
      "medium": 8,
      "low": 2
    }
  }
}
```

### Error Response  
```json
{
  "detail": "Todo not found",
  "vader_quote": "I find your search... lacking."
}
```

## 🧪 Testing

The API includes comprehensive tests covering:

- **Unit tests** for all endpoints
- **Integration tests** for database operations
- **Error handling tests** with edge cases
- **Validation tests** for input sanitization
- **Performance tests** for pagination and filtering

Run tests with:
```bash
pytest -v --cov=app tests/
```

## 📈 Performance

- **Fast responses** with proper indexing
- **Efficient pagination** for large datasets
- **Optimized queries** with SQLAlchemy
- **Async support** for concurrent requests
- **Memory efficient** with proper connection pooling

## 🔒 Security

- **Input validation** with Pydantic schemas
- **SQL injection protection** via ORM
- **CORS configuration** for frontend security  
- **Error handling** that doesn't leak sensitive info
- **Type safety** preventing runtime errors

---

**"The Force is strong with this API."** 

For more details, visit the interactive documentation at `/docs` when running the server.