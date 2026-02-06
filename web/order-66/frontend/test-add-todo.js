// Quick test to verify add todo functionality
import { useTodoStore } from '../src/stores/todoStore'
import { createPinia, setActivePinia } from 'pinia'

// Setup test environment
setActivePinia(createPinia())
const store = useTodoStore()

console.log('Initial todos count:', store.todos.length)

// Test adding a todo
store.addTodo('Test todo item', 'high')

console.log('After adding todo:', store.todos.length)
console.log('Latest todo:', store.todos[0])

// Test the filtered todos getter
console.log('Filtered todos:', store.filteredTodos.length)
console.log('Active todos count:', store.activeTodosCount)

console.log('✅ Add todo functionality test complete!')