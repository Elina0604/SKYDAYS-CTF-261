from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, Literal
from datetime import datetime

from ..database import get_db
from ..models.todo import Todo
from ..schemas.todo import TodoCreate, TodoUpdate, TodoResponse, TodoListResponse, TodoStats

router = APIRouter()


def calculate_todo_stats(db: Session) -> TodoStats:
    """Calculate todo statistics"""
    todos = db.query(Todo).all()
    active = sum(1 for todo in todos if not todo.completed)
    completed = sum(1 for todo in todos if todo.completed)
    by_priority = {"low": 0, "medium": 0, "high": 0}
    
    for todo in todos:
        if not todo.completed:  # Only count active todos in priority stats
            by_priority[todo.priority] += 1
    
    return TodoStats(
        active=active,
        completed=completed,
        total=len(todos),
        by_priority=by_priority
    )


@router.get("/todos", response_model=TodoListResponse)
async def get_todos(
    filter: Optional[Literal["all", "active", "completed"]] = Query(default="all", description="Filter todos by completion status"),
    sort: Optional[str] = Query(default="created_at", description="Sort field - try different column names!"),
    order: Optional[Literal["asc", "desc"]] = Query(default="desc", description="Sort order"),
    limit: Optional[int] = Query(default=50, ge=1, le=100, description="Number of todos to return"),
    offset: Optional[int] = Query(default=0, ge=0, description="Number of todos to skip"),
    db: Session = Depends(get_db)
):
    """Get todos with filtering and sorting - The Empire's task management system"""
    # Base query for todos
    base_query = """
    SELECT id, text, completed, priority, created_at, updated_at, completed_at 
    FROM todos
    """
    
    # Apply filter
    if filter == "active":
        base_query += " WHERE completed = 0"
    elif filter == "completed":
        base_query += " WHERE completed = 1"
    
    # Apply sorting - VULNERABLE: Direct string concatenation!
    # The Empire's developers were too confident in their security...
    try:
        # Normalize common sort field names for backwards compatibility
        if sort in ["name", "createdAt", "completedAt"]:
            if sort == "name":
                sort = "text"
            elif sort == "createdAt":
                sort = "created_at"
            elif sort == "completedAt":
                sort = "completed_at"
        
        # WARNING: This is vulnerable to SQL injection!
        # The sort parameter is directly inserted into the query
        if sort and order:
            base_query += f" ORDER BY {sort} {order.upper()}"
        
        # Add pagination
        base_query += f" LIMIT {limit} OFFSET {offset}"
        
        # Execute the raw SQL query
        result = db.execute(text(base_query))
        todos_data = result.fetchall()
        
        # Convert raw results to Todo objects
        todos = []
        for row in todos_data:
            todo = Todo()
            todo.id = row[0]
            todo.text = row[1]
            todo.completed = bool(row[2])
            todo.priority = row[3]
            todo.created_at = row[4]
            todo.updated_at = row[5]
            todo.completed_at = row[6]
            todos.append(todo)
            
    except Exception as e:
        # Helpful error messages for the CTF participants
        error_msg = str(e)
        if "no such column" in error_msg.lower():
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid sort column: {sort}. The Empire's database structure might be more complex than it appears..."
            )
        elif "syntax error" in error_msg.lower():
            raise HTTPException(
                status_code=400, 
                detail=f"SQL syntax error in sort parameter. Perhaps you're trying to execute something the Empire doesn't expect? Error: {error_msg}"
            )
        else:
            raise HTTPException(status_code=500, detail=f"Unexpected database error: {error_msg}")
    
    # Get total count (using safe query for count)
    count_query = db.query(Todo)
    if filter == "active":
        count_query = count_query.filter(Todo.completed == False)
    elif filter == "completed":
        count_query = count_query.filter(Todo.completed == True)
    total = count_query.count()
    
    # Calculate stats
    stats = calculate_todo_stats(db)
    
    return TodoListResponse(
        todos=[TodoResponse.from_orm(todo) for todo in todos],
        total=total,
        stats=stats
    )


@router.post("/todos", response_model=TodoResponse, status_code=201)
async def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db)
):
    """Create a new todo"""
    db_todo = Todo(
        text=todo.text,
        priority=todo.priority,
        completed=False
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return TodoResponse.from_orm(db_todo)


@router.delete("/todos/completed", status_code=204)
async def clear_completed_todos(
    db: Session = Depends(get_db)
):
    """Delete all completed todos"""
    completed_todos = db.query(Todo).filter(Todo.completed == True).all()
    for todo in completed_todos:
        db.delete(todo)
    db.commit()


@router.get("/todos/stats", response_model=TodoStats)
async def get_todo_stats(
    db: Session = Depends(get_db)
):
    """Get todo statistics"""
    return calculate_todo_stats(db)


@router.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific todo by ID"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return TodoResponse.from_orm(todo)


@router.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: str,
    todo_update: TodoUpdate,
    db: Session = Depends(get_db)
):
    """Update a todo"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Update fields that were provided
    update_data = todo_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)
    
    # Handle completion date logic
    if "completed" in update_data:
        if update_data["completed"] and not todo.completed_at:
            todo.completed_at = datetime.now()
        elif not update_data["completed"] and todo.completed_at:
            todo.completed_at = None
    
    db.commit()
    db.refresh(todo)
    return TodoResponse.from_orm(todo)


@router.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(
    todo_id: str,
    db: Session = Depends(get_db)
):
    """Delete a todo"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()


@router.put("/todos/{todo_id}/toggle", response_model=TodoResponse)
async def toggle_todo(
    todo_id: str,
    db: Session = Depends(get_db)
):
    """Toggle todo completion status"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    was_completed = todo.completed
    todo.completed = not todo.completed
    
    # Update completion date
    if todo.completed and not was_completed:
        todo.completed_at = datetime.now()
    elif not todo.completed and was_completed:
        todo.completed_at = None
    
    db.commit()
    db.refresh(todo)
    return TodoResponse.from_orm(todo)


@router.put("/todos/{todo_id}/priority", response_model=TodoResponse)
async def update_todo_priority(
    todo_id: str,
    priority: Literal["low", "medium", "high"],
    db: Session = Depends(get_db)
):
    """Update todo priority"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo.priority = priority
    db.commit()
    db.refresh(todo)
    return TodoResponse.from_orm(todo)