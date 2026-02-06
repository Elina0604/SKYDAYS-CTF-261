import pytest
from tests.conftest import client, setup_database, sample_todo_data, create_sample_todos


class TestTodoEndpoints:
    """Test suite for todo endpoints"""

    def test_create_todo(self, setup_database, sample_todo_data):
        """Test creating a new todo"""
        response = client.post("/api/todos", json=sample_todo_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["text"] == sample_todo_data["text"]
        assert data["priority"] == sample_todo_data["priority"]
        assert data["completed"] == False
        assert "id" in data
        assert "created_at" in data

    def test_get_todos_empty(self, setup_database):
        """Test getting todos when database is empty"""
        response = client.get("/api/todos")
        assert response.status_code == 200
        
        data = response.json()
        assert data["todos"] == []
        assert data["total"] == 0
        assert data["stats"]["active"] == 0
        assert data["stats"]["completed"] == 0

    def test_get_todos_with_data(self, create_sample_todos):
        """Test getting todos with sample data"""
        response = client.get("/api/todos")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["todos"]) == 3
        assert data["total"] == 3
        assert data["stats"]["active"] == 2  # 2 incomplete todos
        assert data["stats"]["completed"] == 1  # 1 completed todo

    def test_get_todos_filtered_active(self, create_sample_todos):
        """Test getting only active todos"""
        response = client.get("/api/todos?filter=active")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["todos"]) == 2  # Only active todos
        for todo in data["todos"]:
            assert todo["completed"] == False

    def test_get_todos_filtered_completed(self, create_sample_todos):
        """Test getting only completed todos"""
        response = client.get("/api/todos?filter=completed")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["todos"]) == 1  # Only completed todos
        for todo in data["todos"]:
            assert todo["completed"] == True

    def test_get_todos_sorted_by_priority(self, create_sample_todos):
        """Test sorting todos by priority"""
        response = client.get("/api/todos?sort=priority&order=desc")
        assert response.status_code == 200
        
        data = response.json()
        priorities = [todo["priority"] for todo in data["todos"]]
        assert priorities == ["high", "medium", "low"]  # Descending priority

    def test_get_todo_by_id(self, create_sample_todos):
        """Test getting a specific todo by ID"""
        todos = create_sample_todos
        todo_id = todos[0].id
        
        response = client.get(f"/api/todos/{todo_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == todo_id
        assert data["text"] == todos[0].text

    def test_get_todo_not_found(self, setup_database):
        """Test getting a non-existent todo"""
        response = client.get("/api/todos/nonexistent-id")
        assert response.status_code == 404
        assert "vader_quote" in response.json()

    def test_update_todo(self, create_sample_todos):
        """Test updating a todo"""
        todos = create_sample_todos
        todo_id = todos[0].id
        
        update_data = {
            "text": "Updated: Find rebel base",
            "priority": "medium"
        }
        
        response = client.put(f"/api/todos/{todo_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["text"] == update_data["text"]
        assert data["priority"] == update_data["priority"]

    def test_toggle_todo_completion(self, create_sample_todos):
        """Test toggling todo completion status"""
        todos = create_sample_todos
        todo_id = todos[0].id  # This todo is initially incomplete
        
        response = client.put(f"/api/todos/{todo_id}/toggle")
        assert response.status_code == 200
        
        data = response.json()
        assert data["completed"] == True
        assert data["completed_at"] is not None

    def test_update_todo_priority(self, create_sample_todos):
        """Test updating todo priority"""
        todos = create_sample_todos
        todo_id = todos[0].id
        
        response = client.put(f"/api/todos/{todo_id}/priority?priority=low")
        assert response.status_code == 200
        
        data = response.json()
        assert data["priority"] == "low"

    def test_delete_todo(self, create_sample_todos):
        """Test deleting a todo"""
        todos = create_sample_todos
        todo_id = todos[0].id
        
        response = client.delete(f"/api/todos/{todo_id}")
        assert response.status_code == 204
        
        # Verify todo is deleted
        response = client.get(f"/api/todos/{todo_id}")
        assert response.status_code == 404

    def test_clear_completed_todos(self, create_sample_todos):
        """Test clearing all completed todos"""
        response = client.delete("/api/todos/completed")
        assert response.status_code == 204
        
        # Verify completed todos are gone
        response = client.get("/api/todos")
        data = response.json()
        assert data["stats"]["completed"] == 0
        assert data["stats"]["active"] == 2  # Only active todos remain

    def test_get_todo_stats(self, create_sample_todos):
        """Test getting todo statistics"""
        response = client.get("/api/todos/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert data["active"] == 2
        assert data["completed"] == 1
        assert data["total"] == 3
        assert "by_priority" in data

    def test_create_todo_validation_error(self, setup_database):
        """Test validation error when creating todo with invalid data"""
        invalid_data = {"priority": "high"}  # Missing required 'text' field
        
        response = client.post("/api/todos", json=invalid_data)
        assert response.status_code == 422
        assert "vader_quote" in response.json()

    def test_pagination(self, setup_database):
        """Test todo pagination"""
        # Create multiple todos
        for i in range(5):
            client.post("/api/todos", json={"text": f"Todo {i}", "priority": "medium"})
        
        # Test pagination with limit
        response = client.get("/api/todos?limit=3&offset=0")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["todos"]) == 3
        assert data["total"] == 5