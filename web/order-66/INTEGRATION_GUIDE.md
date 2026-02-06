# 🌟 Vader Todo - Full Stack Setup Guide

Your **Star Wars-themed todo application** is now fully integrated with a FastAPI backend!

## 🚀 Quick Start

### 1. Start the Backend API

```bash
cd backend
./start.sh
```

The backend will be available at:
- **API**: http://localhost:8000/api  
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/api/health

### 2. Start the Frontend  

```bash
cd vader-todo-app
bun dev
```

The frontend will be available at:
- **App**: http://localhost:5173

## ✨ Features Now Available

### 🔄 **Smart API Integration**
- **Automatic failover** - Works offline with localStorage if API is unavailable
- **Real-time status** - Shows online/offline status in top-right corner
- **Seamless sync** - Local todos automatically sync when API comes online

### ⚡ **Enhanced User Experience**
- **Loading states** for all operations (add, edit, delete, toggle)
- **Visual feedback** with spinners and disabled states
- **Error handling** with Vader-themed error messages
- **Connection status** indicator

### 🛠 **Backend Features**
- **FastAPI** with automatic documentation
- **SQLite database** (perfect for single-user or development)
- **PostgreSQL ready** (just change DATABASE_URL)
- **Comprehensive API** with filtering, sorting, pagination
- **Vader-themed error messages** ("I find your lack of faith disturbing")

## 🔧 Configuration

### Frontend (.env in vader-todo-app/)
```bash
# API Configuration
VITE_API_URL=http://localhost:8000/api

# Development settings  
VITE_DEV_MODE=true
```

### Backend (.env in backend/)
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

## 🎯 How It Works

### 1. **Intelligent Mode Detection**
On startup, the frontend checks if the API is available:
- ✅ **API Available**: Uses backend for all operations
- ❌ **API Unavailable**: Falls back to localStorage  
- 🔄 **Auto-sync**: When API comes back online, local data syncs automatically

### 2. **API-First with Offline Fallback**
```javascript
// All operations try API first, fallback to localStorage
await todoStore.addTodo("Complete Death Star plans", "high")
```

### 3. **Seamless User Experience**
- Loading spinners on all async operations
- API status indicator (online/offline)
- Error messages with Star Wars quotes
- No disruption when switching between modes

## 📊 API Endpoints

### **Todos**
- `GET /api/todos` - List with filtering & sorting
- `POST /api/todos` - Create new todo
- `PUT /api/todos/{id}` - Update todo  
- `DELETE /api/todos/{id}` - Delete todo
- `PUT /api/todos/{id}/toggle` - Toggle completion
- `DELETE /api/todos/completed` - Clear completed

### **Statistics**  
- `GET /api/todos/stats` - Get counts and analytics

### **Health & Info**
- `GET /api/health` - API health check
- `GET /api/info` - API information

## 🧪 Testing

### Run Backend Tests
```bash  
cd backend
pytest -v
```

### Test API Integration
```bash
# With backend running, test the API
curl http://localhost:8000/api/health
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"text": "Test the Death Star", "priority": "high"}'
```

## 🌐 Deployment Ready

### Backend Deployment
```bash
# Using Gunicorn (production)
cd backend
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Using Docker
docker build -t vader-todo-api .
docker run -p 8000:8000 vader-todo-api
```

### Frontend Deployment  
```bash  
cd vader-todo-app
bun run build
# Deploy dist/ folder to any static hosting (Vercel, Netlify, etc.)
```

## 🛡️ What Changed

### ✅ **Preserved All Original Features**
- Star Wars theming and sound effects
- All existing UI components and styling
- Local storage functionality (as fallback)
- Filtering, sorting, and search
- Responsive design and animations

### ➕ **Added New Capabilities**
- REST API with full CRUD operations
- Database persistence (SQLite/PostgreSQL)
- Loading states and error handling
- Online/offline mode switching
- Automatic data synchronization
- Professional API documentation

### 🔄 **Enhanced Components**
- **TodoStore**: Now handles both API and localStorage
- **TodoView**: Added loading states and API status
- **TodoItem**: Async operations with visual feedback
- **New Services**: API client, error handling, loading management

---

## 🎭 Experience the Power of the Dark Side

Your todo app now has the power of both frontend AND backend. Whether the API is online or offline, your tasks will be preserved. 

**"The Force is strong with this application."**

Start both servers and experience the seamless integration! 🌟