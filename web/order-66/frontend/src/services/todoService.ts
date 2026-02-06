import type { Todo } from '../types/todo'
import { apiClient, isApiAvailable } from './api'

export interface TodoCreateRequest {
  text: string
  priority: Todo['priority']
}

export interface TodoUpdateRequest {
  text?: string
  completed?: boolean
  priority?: Todo['priority']
}

export interface TodoListResponse {
  todos: Todo[]
  total: number
  stats: {
    active: number
    completed: number
    total: number
    by_priority: Record<string, number>
  }
}

export interface TodoFilters {
  filter?: 'all' | 'active' | 'completed'
  sort?: string // Allow any string for CTF challenge - was: 'name' | 'createdAt' | 'completedAt' | 'priority'
  order?: 'asc' | 'desc'
  limit?: number
  offset?: number
}

class TodoService {
  /**
   * Get all todos with optional filtering and sorting
   */
  async getTodos(filters: TodoFilters = {}): Promise<TodoListResponse> {
    const params = new URLSearchParams()
    
    if (filters.filter) params.append('filter', filters.filter)
    if (filters.sort) params.append('sort', filters.sort)
    if (filters.order) params.append('order', filters.order)
    if (filters.limit) params.append('limit', filters.limit.toString())
    if (filters.offset) params.append('offset', filters.offset.toString())
    
    const response = await apiClient.get<TodoListResponse>(`/todos?${params}`)
    return response.data
  }

  /**
   * Get a specific todo by ID
   */
  async getTodoById(id: string): Promise<Todo> {
    const response = await apiClient.get<Todo>(`/todos/${id}`)
    return response.data
  }

  /**
   * Create a new todo
   */
  async createTodo(todo: TodoCreateRequest): Promise<Todo> {
    const response = await apiClient.post<Todo>('/todos', todo)
    return response.data
  }

  /**
   * Update a todo
   */
  async updateTodo(id: string, updates: TodoUpdateRequest): Promise<Todo> {
    const response = await apiClient.put<Todo>(`/todos/${id}`, updates)
    return response.data
  }

  /**
   * Delete a todo
   */
  async deleteTodo(id: string): Promise<void> {
    await apiClient.delete(`/todos/${id}`)
  }

  /**
   * Toggle todo completion status
   */
  async toggleTodo(id: string): Promise<Todo> {
    const response = await apiClient.put<Todo>(`/todos/${id}/toggle`)
    return response.data
  }

  /**
   * Update todo priority
   */
  async updateTodoPriority(id: string, priority: Todo['priority']): Promise<Todo> {
    const response = await apiClient.put<Todo>(`/todos/${id}/priority?priority=${priority}`)
    return response.data
  }

  /**
   * Clear all completed todos
   */
  async clearCompletedTodos(): Promise<void> {
    await apiClient.delete('/todos/completed')
  }

  /**
   * Get todo statistics
   */
  async getTodoStats(): Promise<TodoListResponse['stats']> {
    const response = await apiClient.get<TodoListResponse['stats']>('/todos/stats')
    return response.data
  }
}

// Export singleton instance
export const todoService = new TodoService()
export default todoService