from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal


class TodoBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, description="Todo text content")
    priority: Literal["low", "medium", "high"] = Field(default="medium", description="Todo priority level")


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    text: Optional[str] = Field(None, min_length=1, max_length=1000, description="Updated todo text")
    completed: Optional[bool] = Field(None, description="Completion status")
    priority: Optional[Literal["low", "medium", "high"]] = Field(None, description="Updated priority level")


class TodoResponse(TodoBase):
    id: str
    completed: bool
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TodoStats(BaseModel):
    active: int
    completed: int
    total: int
    by_priority: dict[str, int]


class TodoListResponse(BaseModel):
    todos: list[TodoResponse]
    total: int
    stats: TodoStats