import pytest
from tests.conftest import client, setup_database


class TestPreferencesEndpoints:
    """Test suite for preferences endpoints"""

    def test_get_default_preferences(self, setup_database):
        """Test getting default preferences when none exist"""
        response = client.get("/api/preferences")
        assert response.status_code == 200
        
        data = response.json()
        assert data["sort_field"] == "createdAt"
        assert data["sort_order"] == "desc"
        assert data["sound_effects_enabled"] == True
        assert data["theme"] == "dark"
        assert data["items_per_page"] == 50

    def test_update_preferences(self, setup_database):
        """Test updating preferences"""
        update_data = {
            "sort_field": "priority",
            "sort_order": "asc",
            "sound_effects_enabled": False,
            "theme": "light",
            "items_per_page": 25
        }
        
        response = client.put("/api/preferences", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["sort_field"] == "priority"
        assert data["sort_order"] == "asc"
        assert data["sound_effects_enabled"] == False
        assert data["theme"] == "light"
        assert data["items_per_page"] == 25

    def test_partial_update_preferences(self, setup_database):
        """Test partially updating preferences"""
        # First, set initial preferences
        initial_data = {"sort_field": "name", "theme": "light"}
        client.put("/api/preferences", json=initial_data)
        
        # Then update only some fields
        partial_update = {"sound_effects_enabled": False}
        response = client.put("/api/preferences", json=partial_update)
        assert response.status_code == 200
        
        data = response.json()
        # Should keep previous values and update only specified ones
        assert data["sort_field"] == "name"  # Kept from before
        assert data["theme"] == "light"  # Kept from before  
        assert data["sound_effects_enabled"] == False  # Updated
        assert data["sort_order"] == "desc"  # Default unchanged

    def test_reset_preferences(self, setup_database):
        """Test resetting preferences to defaults"""
        # First, change some preferences
        update_data = {
            "sort_field": "priority",
            "theme": "light",
            "sound_effects_enabled": False
        }
        client.put("/api/preferences", json=update_data)
        
        # Reset to defaults
        response = client.post("/api/preferences/reset")
        assert response.status_code == 200
        
        data = response.json()
        assert data["sort_field"] == "createdAt"  # Back to default
        assert data["sort_order"] == "desc"  # Back to default
        assert data["sound_effects_enabled"] == True  # Back to default
        assert data["theme"] == "dark"  # Back to default
        assert data["items_per_page"] == 50  # Back to default

    def test_preferences_validation_error(self, setup_database):
        """Test validation error with invalid preferences data"""
        invalid_data = {
            "sort_field": "invalid_field",  # Invalid sort field
            "items_per_page": 5  # Too small
        }
        
        response = client.put("/api/preferences", json=invalid_data)
        assert response.status_code == 422
        assert "vader_quote" in response.json()

    def test_preferences_persistence(self, setup_database):
        """Test that preferences persist across requests"""
        # Set preferences
        update_data = {"sort_field": "name", "theme": "light"}
        response = client.put("/api/preferences", json=update_data)
        assert response.status_code == 200
        
        # Get preferences again - should be persisted
        response = client.get("/api/preferences")
        assert response.status_code == 200
        
        data = response.json()
        assert data["sort_field"] == "name"
        assert data["theme"] == "light"