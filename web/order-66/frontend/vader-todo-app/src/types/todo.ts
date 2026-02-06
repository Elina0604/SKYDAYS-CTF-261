export interface Todo {
  id: string
  text: string
  completed: boolean
  createdAt: Date
  completedAt?: Date
  priority: 'low' | 'medium' | 'high'
}

// Updated to allow any string for CTF challenge
export type SortField = string // 'name' | 'createdAt' | 'completedAt' | 'priority' | any custom field
export type SortOrder = 'asc' | 'desc'

export interface TodoState {
  todos: Todo[]
  filter: 'all' | 'active' | 'completed'
  sortField: SortField
  sortOrder: SortOrder
}