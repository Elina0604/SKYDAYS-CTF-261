from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal


class PreferencesBase(BaseModel):
    sort_field: Literal["name", "createdAt", "completedAt", "priority"] = Field(default="createdAt", description="Default sort field")
    sort_order: Literal["asc", "desc"] = Field(default="desc", description="Default sort order")
    sound_effects_enabled: bool = Field(default=True, description="Whether sound effects are enabled")
    theme: Literal["dark", "light"] = Field(default="dark", description="UI theme")
    items_per_page: int = Field(default=50, ge=10, le=100, description="Number of items per page")


class PreferencesUpdate(BaseModel):
    sort_field: Optional[Literal["name", "createdAt", "completedAt", "priority"]] = Field(None, description="Updated sort field")
    sort_order: Optional[Literal["asc", "desc"]] = Field(None, description="Updated sort order")
    sound_effects_enabled: Optional[bool] = Field(None, description="Updated sound effects setting")
    theme: Optional[Literal["dark", "light"]] = Field(None, description="Updated theme")
    items_per_page: Optional[int] = Field(None, ge=10, le=100, description="Updated items per page")


class PreferencesResponse(PreferencesBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True