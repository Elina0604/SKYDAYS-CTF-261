import { defineStore } from 'pinia'
import type { Todo, TodoState, SortField, SortOrder } from '../types/todo'
import { soundEffects } from '../utils/soundEffects'
import { todoService } from '../services/todoService'
import { checkApiAvailability, isApiAvailable } from '../services/api'
import { useApi } from '../composables/useApi'

const vaderQuotes = [
  "You have failed me for the last time.",
  "The power of the Dark Side compels you.",
  "Your lack of faith is disturbing.",
  "Impressive. Most impressive.",
  "You underestimate the power of the Dark Side.",
  "The circle is now complete.",
  "I find your lack of progress disturbing.",
  "You have much to learn.",
  "The Force is strong with this one.",
  "Your destiny lies with me.",
  "Don't make me destroy you.",
  "You cannot escape your destiny.",
  "I sense something... a presence I've not felt since...",
  "The Emperor is not as forgiving as I am.",
  "You are beaten. It is useless to resist.",
  "Your powers are weak, old man.",
  "I have you now.",
  "You may fire when ready.",
  "All too easy.",
  "Perhaps you refer to the imminent attack of your rebel fleet?"
]

export const useTodoStore = defineStore('todos', {
  state: (): TodoState & { 
    isLoading: boolean
    isInitialized: boolean
    isApiMode: boolean
    lastSyncTime: Date | null
  } => {
    const savedTodos = localStorage.getItem('vader-todos')
    const savedSortField = (localStorage.getItem('vader-sort-field') as SortField) || 'createdAt'
    const savedSortOrder = (localStorage.getItem('vader-sort-order') as SortOrder) || 'desc'
    
    return {
      todos: JSON.parse(savedTodos || '[]').map((todo: any) => ({
        ...todo,
        createdAt: new Date(todo.created_at || todo.createdAt),
        completedAt: todo.completed_at || todo.completedAt ? new Date(todo.completed_at || todo.completedAt) : undefined
      })),
      filter: 'all',
      sortField: savedSortField,
      sortOrder: savedSortOrder,
      isLoading: false,
      isInitialized: false,
      isApiMode: false,
      lastSyncTime: null
    }
  },

  getters: {
    sortedTodos(): Todo[] {
      // If API is available, let the backend handle sorting
      if (this.isApiMode) {
        return this.todos
      }
      
      // Otherwise, sort locally (existing logic)
      const priorityOrder = { high: 3, medium: 2, low: 1 }
      
      return [...this.todos].sort((a, b) => {
        let comparison = 0
        
        switch (this.sortField) {
          case 'name':
            comparison = a.text.toLowerCase().localeCompare(b.text.toLowerCase())
            break
          case 'createdAt':
            comparison = a.createdAt.getTime() - b.createdAt.getTime()
            break
          case 'completedAt':
            // Handle undefined completedAt values
            if (!a.completedAt && !b.completedAt) comparison = 0
            else if (!a.completedAt) comparison = 1  // Put incomplete tasks at end when sorting by completion
            else if (!b.completedAt) comparison = -1
            else comparison = a.completedAt.getTime() - b.completedAt.getTime()
            break
          case 'priority':
            comparison = priorityOrder[a.priority] - priorityOrder[b.priority]
            break
          default:
            comparison = 0
        }
        
        return this.sortOrder === 'asc' ? comparison : -comparison
      })
    },

    filteredTodos(): Todo[] {
      // If API is available, let the backend handle filtering  
      if (this.isApiMode) {
        return this.todos
      }
      
      // Otherwise, filter locally (existing logic)
      const sorted = this.sortedTodos
      
      switch (this.filter) {
        case 'active':
          return sorted.filter(todo => !todo.completed)
        case 'completed':
          return sorted.filter(todo => todo.completed)
        default:
          return sorted
      }
    },

    activeTodosCount(): number {
      return this.todos.filter(todo => !todo.completed).length
    },

    completedTodosCount(): number {
      return this.todos.filter(todo => todo.completed).length
    },

    randomVaderQuote(): string {
      return vaderQuotes[Math.floor(Math.random() * vaderQuotes.length)]
    },

    statusMessage(): string {
      if (!this.isInitialized) return 'Initializing...'
      if (this.isLoading) return 'Loading...'
      if (this.isApiMode) return 'Connected to API'
      return 'Offline Mode'
    }
  },

  actions: {
    /**
     * Initialize the store - check API availability and load data
     */
    async initialize() {
      const { withLoading } = useApi()
      
      await withLoading('initialize', async () => {
        console.log('🚀 Initializing Vader Todo Store...')
        
        // Check if API is available
        const apiAvailable = await checkApiAvailability()
        this.isApiMode = apiAvailable
        
        if (apiAvailable) {
          console.log('✅ API available - switching to API mode')
          await this.loadTodosFromApi()
          // Sync any local todos that might exist
          await this.syncLocalTodos()
        } else {
          console.log('📱 API unavailable - using localStorage mode')
          // Already loaded from localStorage in state initialization
        }
        
        this.isInitialized = true
        this.lastSyncTime = new Date()
      })
    },

    /**
     * Load todos from API
     */
    async loadTodosFromApi() {
      try {
        const response = await todoService.getTodos({
          filter: this.filter !== 'all' ? this.filter : undefined,
          sort: this.sortField,
          order: this.sortOrder
        })
        
        // Convert API response dates to Date objects and fix field mapping
        this.todos = response.todos.map((todo: any) => ({
          ...todo,
          createdAt: new Date(todo.created_at || todo.createdAt),
          completedAt: todo.completed_at || todo.completedAt ? new Date(todo.completed_at || todo.completedAt) : undefined
        }))
        
        console.log(`✅ Loaded ${this.todos.length} todos from API`)
      } catch (error) {
        console.error('Failed to load todos from API:', error)
        throw error
      }
    },

    /**
     * Sync any local todos that don't exist in API
     */
    async syncLocalTodos() {
      const localTodos = JSON.parse(localStorage.getItem('vader-todos') || '[]')
      if (localTodos.length === 0) return

      console.log(`🔄 Syncing ${localTodos.length} local todos to API...`)
      
      for (const localTodo of localTodos) {
        try {
          await todoService.createTodo({
            text: localTodo.text,
            priority: localTodo.priority
          })
        } catch (error) {
          console.warn('Failed to sync local todo:', localTodo, error)
        }
      }
      
      // Clear local storage after sync
      localStorage.removeItem('vader-todos')
      
      // Reload from API to get proper IDs
      await this.loadTodosFromApi()
    },

    /**
     * Add a new todo
     */
    async addTodo(text: string, priority: Todo['priority'] = 'medium') {
      const { withLoading } = useApi()
      
      await withLoading('addTodo', async () => {
        if (this.isApiMode) {
          // API mode - create via API
          const newTodo = await todoService.createTodo({
            text: text.trim(),
            priority
          })
          
          // Convert dates
          const todoWithDates = {
            ...newTodo,
            createdAt: new Date(newTodo.created_at || newTodo.createdAt),
            completedAt: newTodo.completed_at || newTodo.completedAt ? new Date(newTodo.completed_at || newTodo.completedAt) : undefined
          }
          
          this.todos.unshift(todoWithDates)
        } else {
          // LocalStorage mode - create locally (existing logic)
          const newTodo: Todo = {
            id: Date.now().toString(),
            text: text.trim(),
            completed: false,
            createdAt: new Date(),
            completedAt: undefined,
            priority
          }
          
          this.todos.unshift(newTodo)
          this.saveTodos()
        }
        
        await this.playSound('add')
      }, {
        fallback: () => {
          // Fallback to localStorage if API fails
          const newTodo: Todo = {
            id: Date.now().toString(),
            text: text.trim(),
            completed: false,
            createdAt: new Date(),
            completedAt: undefined,
            priority
          }
          
          this.todos.unshift(newTodo)
          this.saveTodos()
        }
      })
    },

    /**
     * Toggle todo completion
     */
    async toggleTodo(id: string) {
      const { withLoading } = useApi()
      
      await withLoading('toggleTodo', async () => {
        const todo = this.todos.find(t => t.id === id)
        if (!todo) return

        if (this.isApiMode) {
          // API mode - toggle via API
          const updatedTodo = await todoService.toggleTodo(id)
          
          // Update local state
          Object.assign(todo, {
            ...updatedTodo,
            createdAt: new Date(updatedTodo.created_at || updatedTodo.createdAt),
            completedAt: updatedTodo.completed_at || updatedTodo.completedAt ? new Date(updatedTodo.completed_at || updatedTodo.completedAt) : undefined
          })
        } else {
          // LocalStorage mode - toggle locally (existing logic)
          const wasCompleted = todo.completed
          todo.completed = !todo.completed
          
          // Set/unset completion date
          if (todo.completed && !wasCompleted) {
            todo.completedAt = new Date()
          } else if (!todo.completed && wasCompleted) {
            todo.completedAt = undefined
          }
          
          this.saveTodos()
        }
        
        await this.playSound(todo.completed ? 'complete' : 'activate')
      }, {
        fallback: () => {
          // Fallback to localStorage
          const todo = this.todos.find(t => t.id === id)
          if (todo) {
            const wasCompleted = todo.completed
            todo.completed = !todo.completed
            
            if (todo.completed && !wasCompleted) {
              todo.completedAt = new Date()
            } else if (!todo.completed && wasCompleted) {
              todo.completedAt = undefined
            }
            
            this.saveTodos()
          }
        }
      })
    },

    /**
     * Delete a todo
     */
    async deleteTodo(id: string) {
      const { withLoading } = useApi()
      
      await withLoading('deleteTodo', async () => {
        if (this.isApiMode) {
          // API mode - delete via API
          await todoService.deleteTodo(id)
        }
        
        // Remove from local state
        const index = this.todos.findIndex(t => t.id === id)
        if (index > -1) {
          this.todos.splice(index, 1)
          if (!this.isApiMode) {
            this.saveTodos()
          }
        }
        
        await this.playSound('delete')
      }, {
        fallback: () => {
          const index = this.todos.findIndex(t => t.id === id)
          if (index > -1) {
            this.todos.splice(index, 1)
            this.saveTodos()
          }
        }
      })
    },

    /**
     * Update todo text
     */
    async updateTodo(id: string, text: string) {
      const { withLoading } = useApi()
      
      await withLoading('updateTodo', async () => {
        const todo = this.todos.find(t => t.id === id)
        if (!todo) return

        if (this.isApiMode) {
          // API mode - update via API
          const updatedTodo = await todoService.updateTodo(id, { text: text.trim() })
          
          // Update local state
          Object.assign(todo, {
            ...updatedTodo,
            createdAt: new Date(updatedTodo.created_at || updatedTodo.createdAt),
            completedAt: updatedTodo.completed_at || updatedTodo.completedAt ? new Date(updatedTodo.completed_at || updatedTodo.completedAt) : undefined
          })
        } else {
          // LocalStorage mode - update locally
          todo.text = text.trim()
          this.saveTodos()
        }
      }, {
        fallback: () => {
          const todo = this.todos.find(t => t.id === id)
          if (todo) {
            todo.text = text.trim()
            this.saveTodos()
          }
        }
      })
    },

    /**
     * Update todo priority
     */
    async updateTodoPriority(id: string, priority: Todo['priority']) {
      const { withLoading } = useApi()
      
      await withLoading('updatePriority', async () => {
        const todo = this.todos.find(t => t.id === id)
        if (!todo) return

        if (this.isApiMode) {
          // API mode - update via API
          const updatedTodo = await todoService.updateTodoPriority(id, priority)
          
          // Update local state
          Object.assign(todo, {
            ...updatedTodo,
            createdAt: new Date(updatedTodo.created_at || updatedTodo.createdAt),
            completedAt: updatedTodo.completed_at || updatedTodo.completedAt ? new Date(updatedTodo.completed_at || updatedTodo.completedAt) : undefined
          })
        } else {
          // LocalStorage mode - update locally
          todo.priority = priority
          this.saveTodos()
        }
      }, {
        fallback: () => {
          const todo = this.todos.find(t => t.id === id)
          if (todo) {
            todo.priority = priority
            this.saveTodos()
          }
        }
      })
    },

    /**
     * Set filter and refresh data if using API
     */
    async setFilter(filter: TodoState['filter']) {
      this.filter = filter
      
      // If using API, reload data with new filter
      if (this.isApiMode) {
        const { withLoading } = useApi()
        await withLoading('setFilter', async () => {
          await this.loadTodosFromApi()
        })
      }
    },

    /**
     * Set sorting and refresh data if using API
     */
    async setSorting(field: SortField, order?: SortOrder) {
      // If clicking the same field, toggle order; otherwise set new field with desc as default
      if (field === this.sortField && !order) {
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc'
      } else {
        this.sortField = field
        this.sortOrder = order || 'desc'
      }
      
      this.saveSortPreferences()
      
      // If using API, reload data with new sorting
      if (this.isApiMode) {
        const { withLoading } = useApi()
        await withLoading('setSorting', async () => {
          await this.loadTodosFromApi()
        })
      }
    },

    /**
     * Clear completed todos
     */
    async clearCompleted() {
      const { withLoading } = useApi()
      
      await withLoading('clearCompleted', async () => {
        if (this.isApiMode) {
          // API mode - clear via API
          await todoService.clearCompletedTodos()
          // Reload to get updated list
          await this.loadTodosFromApi()
        } else {
          // LocalStorage mode - clear locally
          this.todos = this.todos.filter(todo => !todo.completed)
          this.saveTodos()
        }
        
        await this.playSound('clear')
      }, {
        fallback: () => {
          this.todos = this.todos.filter(todo => !todo.completed)
          this.saveTodos()
        }
      })
    },

    /**
     * Save todos to localStorage (fallback/offline mode)
     */
    saveTodos() {
      localStorage.setItem('vader-todos', JSON.stringify(this.todos))
    },

    /**
     * Save sort preferences
     */
    saveSortPreferences() {
      localStorage.setItem('vader-sort-field', this.sortField)
      localStorage.setItem('vader-sort-order', this.sortOrder)
    },

    /**
     * Play sound effect
     */
    async playSound(type: 'add' | 'complete' | 'activate' | 'delete' | 'clear') {
      try {
        switch (type) {
          case 'add':
            await soundEffects.playImperialTone()
            break
          case 'complete':
            await soundEffects.playLightsaberActivation()
            break
          case 'activate':
            await soundEffects.playTieFighter()
            break
          case 'delete':
            await soundEffects.playBlaster()
            break
          case 'clear':
            await soundEffects.playForcePower()
            break
        }
      } catch (error) {
        console.warn('Sound effect failed:', error)
      }
    },

    /**
     * Force refresh from API
     */
    async refreshFromApi() {
      if (!this.isApiMode) return
      
      const { withLoading } = useApi()
      await withLoading('refresh', async () => {
        await this.loadTodosFromApi()
        this.lastSyncTime = new Date()
      })
    },

    /**
     * Switch between API and localStorage modes
     */
    async switchToApiMode() {
      const apiAvailable = await checkApiAvailability()
      if (apiAvailable) {
        this.isApiMode = true
        await this.loadTodosFromApi()
        await this.syncLocalTodos()
      }
    },

    switchToOfflineMode() {
      this.isApiMode = false
      console.log('📱 Switched to offline mode')
    }
  }
})