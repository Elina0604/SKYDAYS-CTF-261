<template>
  <div class="todo-view">
    <!-- API Status Indicator -->
    <div class="api-status-container">
      <div class="api-status" :class="{ online: todoStore.isApiMode, offline: !todoStore.isApiMode }">
        <span class="status-indicator"></span>
        <span class="status-text">{{ todoStore.statusMessage }}</span>
        <button 
          v-if="!todoStore.isApiMode && !todoStore.isLoading" 
          @click="tryReconnectApi"
          class="reconnect-btn"
        >
          Reconnect
        </button>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div v-if="todoStore.isLoading" class="loading-overlay">
      <div class="loading-spinner">
        <div class="death-star-loader">
          <div class="loader-core"></div>
        </div>
        <p class="loading-text">{{ todoStore.statusMessage }}</p>
      </div>
    </div>
    <div class="todo-input-container">
      <div class="input-wrapper">
        <input
          v-model="newTodoText"
          @keyup.enter="addTodo"
          type="text"
          placeholder="What must be accomplished, my apprentice?"
          class="todo-input star-wars-font"
          :class="{ 'input-error': showError }"
        />
        <select v-model="newTodoPriority" class="priority-selector">
          <option value="low">Low Priority</option>
          <option value="medium">Medium Priority</option>
          <option value="high">High Priority</option>
        </select>
      </div>
      <button @click="addTodo" class="add-btn" :disabled="!newTodoText.trim() || isAddingTodo">
        <span class="btn-text">
          <span v-if="isAddingTodo" class="loading-dots">Adding</span>
          <span v-else>Execute Order</span>
        </span>
        <span class="btn-glow"></span>
      </button>
    </div>

    <!-- Error Message -->
    <div v-if="showError" class="error-message">
      <p>"{{ todoStore.randomVaderQuote }}"</p>
    </div>

    <!-- Filter Controls -->
    <div class="filter-controls">
      <button
        v-for="filter in filters"
        :key="filter.value"
        @click="todoStore.setFilter(filter.value)"
        class="filter-btn"
        :class="{ active: todoStore.filter === filter.value }"
      >
        {{ filter.label }}
      </button>
    </div>

    <!-- Sorting Controls -->
    <div class="sorting-controls">
      <div class="sort-label">
        <span class="label-text">Order by Imperial Decree:</span>
      </div>
      <div class="sort-buttons">
        <button
          v-for="sortOption in sortOptions"
          :key="sortOption.field"
          @click="todoStore.setSorting(sortOption.field)"
          class="sort-btn"
          :class="{ 
            active: todoStore.sortField === sortOption.field,
            ascending: todoStore.sortField === sortOption.field && todoStore.sortOrder === 'asc',
            descending: todoStore.sortField === sortOption.field && todoStore.sortOrder === 'desc'
          }"
        >
          <span class="sort-text">{{ sortOption.label }}</span>
          <span class="sort-arrow" v-if="todoStore.sortField === sortOption.field">
            {{ todoStore.sortOrder === 'asc' ? '↑' : '↓' }}
          </span>
        </button>
      </div>
    </div>

    <!-- Todo Stats -->
    <div class="todo-stats">
      <div class="stat">
        <span class="stat-number">{{ todoStore.activeTodosCount }}</span>
        <span class="stat-label">Active Missions</span>
      </div>
      <div class="stat">
        <span class="stat-number">{{ todoStore.completedTodosCount }}</span>
        <span class="stat-label">Completed Orders</span>
      </div>
    </div>

    <!-- Todo List -->
    <div class="todo-list-container">
      <transition-group name="todo" tag="div" class="todo-list">
        <TodoItem
          v-for="todo in todoStore.filteredTodos"
          :key="todo.id"
          :todo="todo"
        />
      </transition-group>

      <!-- Empty State -->
      <div v-if="todoStore.filteredTodos.length === 0" class="empty-state">
        <div class="death-star">
          <div class="death-star-laser"></div>
        </div>
        <p v-if="todoStore.filter === 'all'">
          "Your tasks are complete. Most impressive."
        </p>
        <p v-else-if="todoStore.filter === 'active'">
          "No active missions remain."
        </p>
        <p v-else>
          "The Dark Side has no completed tasks to show."
        </p>
      </div>
    </div>

    <!-- Clear Completed Button -->
    <div v-if="todoStore.completedTodosCount > 0" class="clear-completed-container">
      <button @click="clearCompleted" class="clear-btn" :disabled="isClearingCompleted">
        <span v-if="isClearingCompleted" class="loading-dots">Purging</span>
        <span v-else>Purge Completed Orders</span>
        <span class="btn-glow"></span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useTodoStore } from '../stores/todoStore'
import { useApi } from '../composables/useApi'
import TodoItem from '../components/TodoItem.vue'
import type { Todo, SortField } from '../types/todo'

const todoStore = useTodoStore()
const { createLoading } = useApi()

const newTodoText = ref('')
const newTodoPriority = ref<Todo['priority']>('medium')
const showError = ref(false)

// Loading states for specific operations
const { isLoading: isAddingTodo } = createLoading('addTodo')
const { isLoading: isClearingCompleted } = createLoading('clearCompleted')

const filters = [
  { value: 'all', label: 'All Orders' },
  { value: 'active', label: 'Active Missions' },
  { value: 'completed', label: 'Completed' }
] as const

const sortOptions: Array<{ field: SortField; label: string }> = [
  { field: 'name', label: 'Task Name' },
  { field: 'createdAt', label: 'Creation Date' },
  { field: 'completedAt', label: 'Completion Date' },
  { field: 'priority', label: 'Priority Level' }
]

const addTodo = async () => {
  if (!newTodoText.value.trim()) {
    showError.value = true
    setTimeout(() => {
      showError.value = false
    }, 2000)
    return
  }

  await todoStore.addTodo(newTodoText.value, newTodoPriority.value)
  newTodoText.value = ''
  newTodoPriority.value = 'medium'
  showError.value = false
}

const clearCompleted = async () => {
  await todoStore.clearCompleted()
}

const tryReconnectApi = async () => {
  await todoStore.switchToApiMode()
}
</script>

<style scoped>
.todo-view {
  padding: var(--space-xl) 0;
  display: grid;
  gap: var(--space-xl);
}

/* Modern Input Container with Glassmorphism */
.todo-input-container {
  background: var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-2xl);
  padding: var(--space-xl);
  box-shadow: var(--shadow-xl);
  display: grid;
  grid-template-columns: 1fr auto;
  gap: var(--space-lg);
  align-items: end;
  transition: all var(--transition-normal);
}

.todo-input-container:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: var(--color-border-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-xl), 0 0 30px rgba(var(--color-primary-rgb), 0.1);
}

.input-wrapper {
  display: grid;
  gap: var(--space-md);
}

/* Enhanced Input Styling */
.todo-input {
  background: rgba(0, 0, 0, 0.4);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  color: var(--color-text-primary);
  font-size: 1.1rem;
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-normal);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.todo-input:focus {
  border-color: var(--color-primary);
  box-shadow: 
    0 0 0 3px rgba(var(--color-primary-rgb), 0.1),
    0 0 20px rgba(var(--color-primary-rgb), 0.2);
  transform: scale(1.02);
}

.todo-input.input-error {
  border-color: var(--color-error);
  animation: modern-shake 0.4s cubic-bezier(0.36, 0.07, 0.19, 0.97);
  box-shadow: 0 0 20px rgba(232, 67, 147, 0.3);
}

@keyframes modern-shake {
  0%, 100% { transform: translateX(0) scale(1.02); }
  25% { transform: translateX(-8px) scale(1.02); }
  75% { transform: translateX(8px) scale(1.02); }
}

.priority-selector {
  background: rgba(0, 0, 0, 0.6);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-md);
  color: var(--color-text-primary);
  font-size: 0.95rem;
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-fast);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

.priority-selector:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(var(--color-primary-rgb), 0.1);
}

/* Modern Button Design */
.add-btn, .clear-btn {
  position: relative;
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  border: none;
  border-radius: var(--radius-lg);
  padding: var(--space-lg) var(--space-2xl);
  color: white;
  font-size: 1rem;
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
  transition: all var(--transition-normal);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  letter-spacing: 0.02em;
}

.add-btn:hover:not(:disabled), .clear-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--color-primary-light), var(--color-primary));
  transform: translateY(-3px) scale(1.05);
  box-shadow: var(--shadow-xl), var(--shadow-glow);
}

.add-btn:active, .clear-btn:active {
  transform: translateY(-1px) scale(1.02);
  transition: all 0.1s ease-out;
}

.add-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  background: var(--color-bg-tertiary);
  color: var(--color-text-muted);
}

.btn-text {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.btn-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left var(--transition-slow);
  z-index: 1;
}

.add-btn:hover:not(:disabled) .btn-glow, 
.clear-btn:hover:not(:disabled) .btn-glow {
  left: 100%;
}

/* Modern Error Message */
.error-message {
  background: linear-gradient(135deg, 
    rgba(232, 67, 147, 0.1), 
    rgba(232, 67, 147, 0.05)
  );
  border-left: 4px solid var(--color-error);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  margin-bottom: var(--space-lg);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(232, 67, 147, 0.2);
  box-shadow: var(--shadow-md);
}

.error-message p {
  margin: 0;
  color: var(--color-error);
  font-style: italic;
  font-weight: var(--font-weight-medium);
  font-size: 1.05rem;
}

/* Modern Filter Controls with Glass Effect */
.filter-controls {
  display: flex;
  gap: var(--space-md);
  justify-content: center;
  flex-wrap: wrap;
  background: var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-xl);
  padding: var(--space-lg);
  box-shadow: var(--shadow-lg);
}

.filter-btn {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-md) var(--space-lg);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-normal);
  font-weight: var(--font-weight-medium);
  font-size: 0.95rem;
  letter-spacing: 0.01em;
  position: relative;
  overflow: hidden;
}

.filter-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left var(--transition-normal);
}

.filter-btn:hover::before {
  left: 100%;
}

.filter-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: var(--color-border-hover);
  color: var(--color-text-primary);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.filter-btn.active {
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  border-color: var(--color-primary);
  color: white;
  box-shadow: var(--shadow-glow);
  transform: scale(1.05);
}

/* Enhanced Sorting Controls */
.sorting-controls {
  text-align: center;
  background: var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-xl);
  padding: var(--space-xl);
  box-shadow: var(--shadow-lg);
}

.sort-label {
  margin-bottom: var(--space-lg);
}

.label-text {
  color: var(--color-primary);
  font-weight: var(--font-weight-bold);
  font-size: 1.2rem;
  text-shadow: 0 0 10px rgba(var(--color-primary-rgb), 0.4);
  letter-spacing: 0.02em;
  display: inline-block;
  transition: all var(--transition-normal);
}

.label-text:hover {
  transform: scale(1.05);
  text-shadow: 0 0 15px rgba(var(--color-primary-rgb), 0.6);
}

.sort-buttons {
  display: flex;
  gap: var(--space-md);
  justify-content: center;
  flex-wrap: wrap;
}

.sort-btn {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-md) var(--space-lg);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-normal);
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: 0.95rem;
  font-weight: var(--font-weight-medium);
  position: relative;
  overflow: hidden;
  min-width: 120px;
  justify-content: center;
}

.sort-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--color-primary), transparent);
  transform: translateX(-100%);
  transition: transform var(--transition-slow);
}

.sort-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: var(--color-border-hover);
  color: var(--color-text-primary);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.sort-btn.active {
  background: linear-gradient(135deg, 
    rgba(var(--color-primary-rgb), 0.2), 
    rgba(var(--color-primary-rgb), 0.1)
  );
  border-color: var(--color-primary);
  color: white;
  box-shadow: var(--shadow-glow);
}

.sort-btn.active::before {
  animation: scan-line 2s linear infinite;
}

@keyframes scan-line {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.sort-text {
  font-weight: var(--font-weight-medium);
}

.sort-arrow {
  font-size: 1.2rem;
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
  animation: arrow-bounce 1.5s ease-in-out infinite;
  transition: all var(--transition-fast);
}

@keyframes arrow-bounce {
  0%, 100% { 
    transform: scale(1) translateY(0); 
    opacity: 1; 
  }
  50% { 
    transform: scale(1.3) translateY(-2px); 
    opacity: 0.8; 
  }
}

/* Modern Stats Cards */
.todo-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-lg);
}

.stat {
  text-align: center;
  background: var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  padding: var(--space-xl);
  border-radius: var(--radius-xl);
  border: 1px solid var(--glass-border);
  box-shadow: var(--shadow-lg);
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}

.stat::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-secondary));
  opacity: 0.6;
}

.stat:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: var(--shadow-xl), 0 0 30px rgba(var(--color-primary-rgb), 0.15);
  border-color: var(--color-border-hover);
}

.stat-number {
  display: block;
  font-size: clamp(2.5rem, 4vw, 3.5rem);
  font-weight: var(--font-weight-extrabold);
  color: var(--color-primary);
  text-shadow: 
    0 0 15px rgba(var(--color-primary-rgb), 0.6),
    0 2px 4px rgba(0, 0, 0, 0.8);
  margin-bottom: var(--space-sm);
  transition: all var(--transition-normal);
  line-height: 1;
}

.stat:hover .stat-number {
  transform: scale(1.1);
  text-shadow: 
    0 0 25px rgba(var(--color-primary-rgb), 0.8),
    0 4px 8px rgba(0, 0, 0, 0.9);
}

.stat-label {
  font-size: 0.95rem;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: var(--font-weight-semibold);
  opacity: 0.9;
}

.stat:hover .stat-label {
  color: var(--color-text-primary);
  opacity: 1;
}

/* Modern Todo List Container */
.todo-list-container {
  min-height: 300px;
  background: var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-2xl);
  padding: var(--space-xl);
  box-shadow: var(--shadow-lg);
}

.todo-list {
  display: grid;
  gap: var(--space-lg);
}

/* Enhanced Empty State */
.empty-state {
  text-align: center;
  padding: var(--space-3xl) var(--space-xl);
  color: var(--color-text-muted);
}

.death-star {
  width: 120px;
  height: 120px;
  background: 
    radial-gradient(circle at 35% 35%, #404040, #1a1a1a),
    radial-gradient(circle at 65% 65%, rgba(255, 107, 107, 0.1), transparent);
  border-radius: 50%;
  margin: 0 auto var(--space-2xl);
  position: relative;
  box-shadow: 
    inset 0 0 30px rgba(255, 255, 255, 0.08),
    0 0 50px rgba(0, 0, 0, 0.8),
    0 0 100px rgba(var(--color-primary-rgb), 0.1);
  transition: all var(--transition-slow);
}

.empty-state:hover .death-star {
  transform: scale(1.1) rotateY(15deg);
  box-shadow: 
    inset 0 0 40px rgba(255, 255, 255, 0.12),
    0 0 60px rgba(0, 0, 0, 0.9),
    0 0 120px rgba(var(--color-primary-rgb), 0.2);
}

.death-star-laser {
  position: absolute;
  top: 25%;
  right: 25%;
  width: 18px;
  height: 18px;
  background: 
    radial-gradient(circle, var(--color-primary), var(--color-primary-dark));
  border-radius: 50%;
  box-shadow: 
    0 0 25px var(--color-primary),
    0 0 40px rgba(var(--color-primary-rgb), 0.6);
  animation: death-star-pulse 2.5s ease-in-out infinite;
}

@keyframes death-star-pulse {
  0%, 100% {
    box-shadow: 
      0 0 25px var(--color-primary),
      0 0 40px rgba(var(--color-primary-rgb), 0.6);
    transform: scale(1);
  }
  50% {
    box-shadow: 
      0 0 35px var(--color-primary),
      0 0 60px rgba(var(--color-primary-rgb), 0.9),
      0 0 80px rgba(var(--color-primary-rgb), 0.4);
    transform: scale(1.3);
  }
}

.empty-state p {
  font-size: 1.2rem;
  font-style: italic;
  color: var(--color-text-secondary);
  margin: 0;
  font-weight: var(--font-weight-light);
}

/* Clear Completed Button Container */
.clear-completed-container {
  text-align: center;
  padding-top: var(--space-xl);
}

.clear-btn {
  background: linear-gradient(135deg, var(--color-error), #cc1e66);
  border-color: var(--color-error);
  color: white;
}

.clear-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #ff4081, var(--color-error));
  box-shadow: var(--shadow-xl), 0 0 30px rgba(232, 67, 147, 0.4);
}

/* Modern Transitions */
.todo-enter-active {
  animation: slide-in-from-left var(--transition-slow) var(--transition-bounce);
}

.todo-leave-active {
  animation: slide-out-to-right var(--transition-normal) ease-in;
}

@keyframes slide-in-from-left {
  0% {
    opacity: 0;
    transform: translateX(-100px) scale(0.8) rotateX(20deg);
  }
  100% {
    opacity: 1;
    transform: translateX(0) scale(1) rotateX(0);
  }
}

@keyframes slide-out-to-right {
  0% {
    opacity: 1;
    transform: translateX(0) scale(1) rotateX(0);
  }
  100% {
    opacity: 0;
    transform: translateX(100px) scale(0.8) rotateX(-20deg);
  }
}

.todo-move {
  transition: transform var(--transition-slow) ease-out;
}

/* Modern API Status Indicator */
.api-status-container {
  position: fixed;
  top: var(--space-lg);
  right: var(--space-lg);
  z-index: 1000;
}

.api-status {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  background: var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-full);
  padding: var(--space-md) var(--space-lg);
  font-size: 0.85rem;
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-normal);
  box-shadow: var(--shadow-lg);
}

.api-status:hover {
  background: rgba(255, 255, 255, 0.12);
  transform: scale(1.05);
  box-shadow: var(--shadow-xl);
}

.api-status.online {
  border-color: rgba(0, 184, 148, 0.4);
  color: var(--color-success);
}

.api-status.offline {
  border-color: rgba(var(--color-primary-rgb), 0.4);
  color: var(--color-primary);
}

.status-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: currentColor;
  animation: status-pulse 2s ease-in-out infinite;
  box-shadow: 0 0 10px currentColor;
}

@keyframes status-pulse {
  0%, 100% { 
    opacity: 1; 
    transform: scale(1);
  }
  50% { 
    opacity: 0.6; 
    transform: scale(1.2);
  }
}

.reconnect-btn {
  background: rgba(255, 107, 107, 0.2);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-lg);
  padding: var(--space-xs) var(--space-sm);
  color: var(--color-primary);
  font-size: 0.75rem;
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
  transition: all var(--transition-fast);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.reconnect-btn:hover {
  background: rgba(255, 107, 107, 0.4);
  transform: scale(1.1);
  box-shadow: 0 0 15px rgba(var(--color-primary-rgb), 0.3);
}

/* Enhanced Loading Overlay */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(ellipse at center, rgba(0, 0, 0, 0.8) 0%, rgba(0, 0, 0, 0.95) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  animation: fade-in var(--transition-normal) ease-out;
}

@keyframes fade-in {
  0% {
    opacity: 0;
    backdrop-filter: blur(0px);
    -webkit-backdrop-filter: blur(0px);
  }
  100% {
    opacity: 1;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
  }
}

.loading-spinner {
  text-align: center;
  transform: scale(0);
  animation: spinner-appear 0.5s ease-out 0.2s forwards;
}

@keyframes spinner-appear {
  0% {
    transform: scale(0) rotateX(90deg);
    opacity: 0;
  }
  100% {
    transform: scale(1) rotateX(0);
    opacity: 1;
  }
}

.death-star-loader {
  width: 80px;
  height: 80px;
  margin: 0 auto var(--space-lg);
  position: relative;
  animation: loader-orbit 3s linear infinite;
}

.loader-core {
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 35% 35%, var(--color-primary), #333);
  border-radius: 50%;
  position: relative;
  box-shadow: 
    inset 0 0 25px rgba(var(--color-primary-rgb), 0.4),
    0 0 40px rgba(var(--color-primary-rgb), 0.3),
    0 0 80px rgba(var(--color-primary-rgb), 0.1);
}

.loader-core::before {
  content: '';
  position: absolute;
  top: 25%;
  right: 25%;
  width: 16px;
  height: 16px;
  background: 
    radial-gradient(circle, white, var(--color-primary));
  border-radius: 50%;
  box-shadow: 
    0 0 20px var(--color-primary),
    0 0 40px rgba(var(--color-primary-rgb), 0.8);
  animation: laser-flicker 1.2s ease-in-out infinite;
}

@keyframes loader-orbit {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes laser-flicker {
  0%, 100% { 
    opacity: 1; 
    transform: scale(1);
  }
  50% { 
    opacity: 0.6; 
    transform: scale(1.4);
  }
}

.loading-text {
  color: var(--color-primary);
  font-size: 1.2rem;
  font-weight: var(--font-weight-medium);
  margin: 0;
  letter-spacing: 0.05em;
}

/* Loading dots animation */
.loading-dots::after {
  content: '';
  animation: loading-dots 1.5s infinite;
}

@keyframes loading-dots {
  0%, 20% { content: '.'; }
  40% { content: '..'; }
  60%, 100% { content: '...'; }
}

/* Button disabled states */
.add-btn:disabled:hover, .clear-btn:disabled:hover {
  background: var(--color-bg-tertiary);
  transform: none;
  box-shadow: none;
  color: var(--color-text-muted);
}

/* Responsive Design */
@media (max-width: 768px) {
  .todo-view {
    padding: var(--space-lg) 0;
    gap: var(--space-lg);
  }

  .todo-input-container {
    grid-template-columns: 1fr;
    padding: var(--space-lg);
  }
  
  .todo-stats {
    grid-template-columns: 1fr 1fr;
    gap: var(--space-md);
  }
  
  .filter-controls {
    gap: var(--space-sm);
    padding: var(--space-md);
  }
  
  .filter-btn {
    font-size: 0.85rem;
    padding: var(--space-sm) var(--space-md);
  }

  .sort-buttons {
    gap: var(--space-sm);
  }

  .sort-btn {
    font-size: 0.85rem;
    padding: var(--space-sm) var(--space-md);
    min-width: 100px;
  }

  .label-text {
    font-size: 1rem;
  }

  .sorting-controls,
  .filter-controls,
  .todo-list-container {
    padding: var(--space-lg);
  }

  .api-status-container {
    top: var(--space-sm);
    right: var(--space-sm);
  }

  .api-status {
    font-size: 0.75rem;
    padding: var(--space-sm) var(--space-md);
  }
}

@media (max-width: 480px) {
  .todo-view {
    padding: var(--space-md) 0;
    gap: var(--space-md);
  }

  .todo-input-container {
    padding: var(--space-md);
  }

  .todo-stats {
    grid-template-columns: 1fr;
    gap: var(--space-sm);
  }

  .stat-number {
    font-size: 2rem;
  }

  .filter-controls,
  .sorting-controls,
  .todo-list-container {
    padding: var(--space-md);
  }

  .sort-buttons,
  .filter-controls {
    flex-direction: column;
    align-items: stretch;
  }

  .sort-btn,
  .filter-btn {
    width: 100%;
    justify-content: center;
  }

  .death-star {
    width: 80px;
    height: 80px;
  }

  .empty-state {
    padding: var(--space-2xl) var(--space-md);
  }

  .empty-state p {
    font-size: 1rem;
  }
}

/* High-performance animations for mobile */
@media (max-width: 768px) {
  .todo-enter-active,
  .todo-leave-active {
    animation-duration: 0.3s;
  }
  
  .stat:hover {
    transform: translateY(-2px) scale(1.01);
  }
  
  .filter-btn:hover,
  .sort-btn:hover {
    transform: translateY(-1px);
  }
}

/* Reduce motion for accessibility */
@media (prefers-reduced-motion: reduce) {
  .todo-enter-active,
  .todo-leave-active,
  .todo-move {
    animation: none;
    transition: none;
  }

  .death-star-pulse,
  .status-pulse,
  .arrow-bounce,
  .scan-line,
  .loader-orbit,
  .laser-flicker {
    animation: none;
  }

  .stat:hover,
  .filter-btn:hover,
  .sort-btn:hover,
  .add-btn:hover,
  .clear-btn:hover {
    transform: none;
  }

  .loading-spinner {
    animation: none;
    transform: scale(1);
  }
}
</style>