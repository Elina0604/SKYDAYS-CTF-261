#!/bin/bash

echo "🚀 Testing Vader Todo Full Stack Integration"
echo "=============================================="
echo

# Test 1: Check if frontend can be built
echo "Test 1: Building Frontend..."
cd vader-todo-app
if bun run build; then
    echo "✅ Frontend build successful"
else
    echo "❌ Frontend build failed"
    exit 1
fi
echo

# Test 2: Check backend setup (without running)  
echo "Test 2: Checking Backend Setup..."
cd ../backend
if python3 -c "
try:
    import sys, os
    sys.path.insert(0, '.')
    from app.main import app
    from app.database import Base, engine
    print('✅ Backend imports successful')
    
    # Test database creation
    Base.metadata.create_all(bind=engine)
    print('✅ Database tables created')
    
    print('✅ Backend setup complete')
    print('🎉 Full stack integration ready!')
    print()
    print('Next steps:')
    print('1. Start backend: cd backend && ./start.sh')
    print('2. Start frontend: cd vader-todo-app && bun dev')
    print('3. Visit: http://localhost:5173')
    
except ImportError as e:
    print(f'❌ Backend dependencies missing: {e}')
    print('💡 Install with: pip install -r requirements.txt')
    sys.exit(1)
except Exception as e:
    print(f'❌ Backend error: {e}')
    sys.exit(1)
"; then
    echo "Backend check completed"
else
    echo "❌ Backend setup failed"
    exit 1
fi