# 🚀 Order 66 CTF Challenge - Setup Guide

## Quick Setup (Recommended)

### Step 1: Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### Step 2: Frontend Setup (New Terminal)
```bash
cd vader-todo-app
bun install
bun dev --port 3000
```

### Step 3: Verify Setup
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs
- Challenge Info: http://localhost:8000/api/info

## Docker Setup (Alternative)

*Note: Docker configuration can be added if needed*

## Environment Details

### Backend Requirements
- Python 3.8+
- FastAPI
- SQLAlchemy 
- SQLite (automatically created)

### Frontend Requirements  
- Bun (recommended) or Node.js 18+
- Vue 3
- TypeScript

## Database Initialization

The application automatically:
1. Creates SQLite database (`database.db`)
2. Initializes `todos` and `flags` tables
3. Plants the CTF flag: `SKYDAYS{SKYORDER_66_HAD_TO_EXECUTED}`
4. Adds sample Imperial todos for realism

## Verification Checklist

✅ **Backend Running:** Visit http://localhost:8000/docs  
✅ **Frontend Running:** Visit http://localhost:3000  
✅ **Database Initialized:** See Imperial todos in the interface  
✅ **Vulnerability Active:** Try `?sort=invalid_column` in browser at http://localhost:8000/api/todos?sort=invalid_column  
✅ **Challenge Ready:** Challenge info shows at http://localhost:8000/

## Troubleshooting

### "Module not found" errors
```bash
cd backend
pip install fastapi uvicorn sqlalchemy
```

### Port conflicts
- Backend: Change `--port 8000` to different port
- Frontend: Change `--port 3000` to different port
- Update frontend API base URL if changing backend port

### Database issues
Delete `database.db` and restart backend to reinitialize

### Frontend build issues
```bash
rm -rf node_modules
bun install  # or npm install
```

## Expected Output

### Backend Startup
```
INFO: Uvicorn running on http://127.0.0.1:8000
🏴 CTF Challenge initialized! Flag planted in the Empire's database...
```

### Frontend Startup  
```
  Local:   http://localhost:3000/
  Network: http://192.168.1.x:3000/
```

## Security Notes

- **SQLite database** is created in backend directory
- **No authentication** required (single-user challenge)
- **Intentional vulnerability** - DO NOT use in production
- **Educational purposes only**

---

The Empire's systems are now operational. Begin your mission, rebel! 🏴