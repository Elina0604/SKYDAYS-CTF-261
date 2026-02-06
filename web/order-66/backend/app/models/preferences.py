from sqlalchemy import Column, String, Boolean, DateTime, Integer, CheckConstraint
from sqlalchemy.sql import func
from ..database import Base


class GlobalPreferences(Base):
    __tablename__ = "global_preferences"
    
    id = Column(Integer, primary_key=True, default=1)
    sort_field = Column(String(20), default="createdAt", nullable=False)
    sort_order = Column(String(10), default="desc", nullable=False)
    sound_effects_enabled = Column(Boolean, default=True, nullable=False)
    theme = Column(String(20), default="dark", nullable=False)
    items_per_page = Column(Integer, default=50, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    __table_args__ = (
        CheckConstraint("id = 1", name='single_row_check'),
        CheckConstraint("sort_field IN ('name', 'createdAt', 'completedAt', 'priority')", name='sort_field_check'),
        CheckConstraint("sort_order IN ('asc', 'desc')", name='sort_order_check'),
        CheckConstraint("theme IN ('dark', 'light')", name='theme_check'),
        CheckConstraint("items_per_page BETWEEN 10 AND 100", name='items_per_page_check'),
    )