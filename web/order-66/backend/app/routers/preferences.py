from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.preferences import GlobalPreferences
from ..schemas.preferences import PreferencesUpdate, PreferencesResponse, PreferencesBase

router = APIRouter()


def get_or_create_preferences(db: Session) -> GlobalPreferences:
    """Get global preferences, create if they don't exist"""
    preferences = db.query(GlobalPreferences).filter(GlobalPreferences.id == 1).first()
    if not preferences:
        # Create default preferences
        preferences = GlobalPreferences(id=1)
        db.add(preferences)
        db.commit()
        db.refresh(preferences)
    return preferences


@router.get("/preferences", response_model=PreferencesResponse)
async def get_preferences(
    db: Session = Depends(get_db)
):
    """Get global preferences"""
    preferences = get_or_create_preferences(db)
    return PreferencesResponse.from_orm(preferences)


@router.put("/preferences", response_model=PreferencesResponse)
async def update_preferences(
    preferences_update: PreferencesUpdate,
    db: Session = Depends(get_db)
):
    """Update global preferences"""
    preferences = get_or_create_preferences(db)
    
    # Update fields that were provided
    update_data = preferences_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(preferences, field, value)
    
    db.commit()
    db.refresh(preferences)
    return PreferencesResponse.from_orm(preferences)


@router.post("/preferences/reset", response_model=PreferencesResponse)
async def reset_preferences(
    db: Session = Depends(get_db)
):
    """Reset preferences to defaults"""
    preferences = get_or_create_preferences(db)
    
    # Reset to defaults
    preferences.sort_field = "createdAt"
    preferences.sort_order = "desc"
    preferences.sound_effects_enabled = True
    preferences.theme = "dark"
    preferences.items_per_page = 50
    
    db.commit()
    db.refresh(preferences)
    return PreferencesResponse.from_orm(preferences)