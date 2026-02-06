<template>
  <div class="todo-item" :class="[priorityClass, { completed: todo.completed, editing: isEditing }]">
    <div class="todo-content">
      <!-- Priority Indicator -->
      <div class="priority-indicator" :class="todo.priority">
        <div class="priority-glow"></div>
      </div>

      <!-- Checkbox -->
      <button 
        @click="toggleTodo" 
        class="todo-checkbox"
        :class="{ checked: todo.completed, loading: isToggling }"
        :disabled="isToggling"
        :aria-label="todo.completed ? 'Mark as incomplete' : 'Mark as complete'"
      >
        <div class="checkbox-inner">
          <div v-if="todo.completed && !isToggling" class="checkmark">✓</div>
          <div v-if="isToggling" class="checkbox-spinner"></div>
        </div>
      </button>

      <!-- Todo Text -->
      <div class="todo-text-container" @dblclick="startEditing">
        <input
          v-if="isEditing"
          v-model="editText"
          @keyup.enter="saveEdit"
          @keyup.escape="cancelEdit"
          @blur="saveEdit"
          class="todo-edit-input"
          ref="editInput"
        />
        <span 
          v-else
          class="todo-text"
          :class="{ completed: todo.completed }"
        >
          {{ todo.text }}
        </span>
      </div>

      <!-- Priority Selector (when editing) -->
      <select
        v-if="isEditing"
        v-model="editPriority"
        class="priority-edit-selector"
      >
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>

      <!-- Actions -->
      <div class="todo-actions">
        <button
          v-if="!isEditing"
          @click="startEditing"
          class="action-btn edit-btn"
          aria-label="Edit todo"
        >
          ✎
        </button>
        
        <button
          v-if="isEditing"
          @click="saveEdit"
          class="action-btn save-btn"
          :disabled="isSaving"
          aria-label="Save changes"
        >
          <span v-if="isSaving" class="btn-spinner"></span>
          <span v-else>✓</span>
        </button>
        
        <button
          v-if="isEditing"
          @click="cancelEdit"
          class="action-btn cancel-btn"
          aria-label="Cancel editing"
        >
          ✕
        </button>
        
        <button
          @click="deleteTodo"
          class="action-btn delete-btn"
          :disabled="isDeleting"
          aria-label="Delete todo"
        >
          <span v-if="isDeleting" class="btn-spinner"></span>
          <span v-else>🗲</span>
        </button>
      </div>
    </div>

    <!-- Creation Date -->
    <div class="todo-meta">
      <span class="creation-date">
        Created: {{ formatDate(todo.createdAt) }}
      </span>
      <span v-if="todo.completed && todo.completedAt" class="completion-date">
        Completed: {{ formatDate(todo.completedAt) }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue'
import { useTodoStore } from '../stores/todoStore'
import { useApi } from '../composables/useApi'
import type { Todo } from '../types/todo'

interface Props {
  todo: Todo
}

const props = defineProps<Props>()
const todoStore = useTodoStore()
const { createLoading } = useApi()

const isEditing = ref(false)
const editText = ref('')
const editPriority = ref<Todo['priority']>('medium')
const editInput = ref<HTMLInputElement>()

// Loading states for different operations
const { isLoading: isToggling } = createLoading(`toggle-${props.todo.id}`)
const { isLoading: isSaving } = createLoading(`save-${props.todo.id}`)
const { isLoading: isDeleting } = createLoading(`delete-${props.todo.id}`)

const priorityClass = computed(() => `priority-${props.todo.priority}`)

const startEditing = () => {
  if (props.todo.completed) return
  
  isEditing.value = true
  editText.value = props.todo.text
  editPriority.value = props.todo.priority
  
  nextTick(() => {
    editInput.value?.focus()
    editInput.value?.select()
  })
}

const saveEdit = async () => {
  if (!editText.value.trim()) {
    cancelEdit()
    return
  }
  
  try {
    const promises = []
    
    if (editText.value.trim() !== props.todo.text) {
      promises.push(todoStore.updateTodo(props.todo.id, editText.value))
    }
    
    if (editPriority.value !== props.todo.priority) {
      promises.push(todoStore.updateTodoPriority(props.todo.id, editPriority.value))
    }
    
    if (promises.length > 0) {
      await Promise.all(promises)
    }
    
    isEditing.value = false
  } catch (error) {
    console.error('Failed to save todo:', error)
    // Don't close editing mode if save failed
  }
}

const cancelEdit = () => {
  isEditing.value = false
  editText.value = ''
  editPriority.value = 'medium'
}

const toggleTodo = async () => {
  await todoStore.toggleTodo(props.todo.id)
}

const deleteTodo = async () => {
  await todoStore.deleteTodo(props.todo.id)
}

const formatDate = (date: Date) => {
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}
</script>

<style scoped>
.todo-item {
  background: var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-2xl);
  padding: var(--space-xl);
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-md);
}

.todo-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--priority-color), rgba(255, 255, 255, 0.2));
  opacity: 0.8;
  border-radius: var(--radius-2xl) var(--radius-2xl) 0 0;
}

.todo-item::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.05) 0%, 
    transparent 50%, 
    rgba(255, 255, 255, 0.02) 100%
  );
  pointer-events: none;
  border-radius: var(--radius-2xl);
  opacity: 0;
  transition: opacity var(--transition-normal);
}

.todo-item:hover::after {
  opacity: 1;
}

/* Priority Color Variables */
.todo-item.priority-low {
  --priority-color: var(--color-success);
}

.todo-item.priority-medium {
  --priority-color: var(--color-warning);
}

.todo-item.priority-high {
  --priority-color: var(--color-error);
}

.todo-item:hover {
  border-color: var(--color-border-hover);
  background: rgba(255, 255, 255, 0.12);
  transform: translateY(-4px) scale(1.02);
  box-shadow: 
    var(--shadow-xl), 
    0 0 40px rgba(var(--priority-color), 0.1);
}

.todo-item.completed {
  opacity: 0.7;
  background: rgba(0, 0, 0, 0.3);
}

.todo-item.completed:hover {
  opacity: 0.9;
  transform: translateY(-2px) scale(1.01);
}

.todo-item.editing {
  border-color: var(--color-primary);
  box-shadow: 
    var(--shadow-xl),
    0 0 30px rgba(var(--color-primary-rgb), 0.2);
  background: rgba(255, 255, 255, 0.15);
}

/* Modern Content Layout */
.todo-content {
  display: grid;
  grid-template-columns: auto auto 1fr auto auto;
  align-items: center;
  gap: var(--space-lg);
}

/* Enhanced Priority Indicator */
.priority-indicator {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: 
    radial-gradient(circle at 30% 30%, var(--priority-color), 
    color-mix(in srgb, var(--priority-color) 80%, black));
  position: relative;
  flex-shrink: 0;
  box-shadow: 
    0 0 15px rgba(var(--priority-color), 0.4),
    inset 0 2px 4px rgba(255, 255, 255, 0.2);
}

.priority-indicator::after {
  content: '';
  position: absolute;
  top: -3px;
  left: -3px;
  right: -3px;
  bottom: -3px;
  border-radius: 50%;
  border: 1px solid var(--priority-color);
  opacity: 0.3;
}

.priority-glow {
  position: absolute;
  top: -6px;
  left: -6px;
  right: -6px;
  bottom: -6px;
  border-radius: 50%;
  background: var(--priority-color);
  opacity: 0.2;
  filter: blur(6px);
  animation: priority-breathe 3s ease-in-out infinite;
}

@keyframes priority-breathe {
  0%, 100% { 
    transform: scale(1); 
    opacity: 0.2; 
  }
  50% { 
    transform: scale(1.4); 
    opacity: 0.1; 
  }
}

/* Modern Checkbox Design */
.todo-checkbox {
  width: 28px;
  height: 28px;
  border: 2px solid var(--color-border);
  border-radius: var(--radius-md);
  background: rgba(0, 0, 0, 0.3);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-normal);
  flex-shrink: 0;
  position: relative;
  overflow: hidden;
}

.todo-checkbox::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left var(--transition-normal);
}

.todo-checkbox:hover::before {
  left: 100%;
}

.todo-checkbox:hover {
  border-color: var(--color-primary);
  background: rgba(var(--color-primary-rgb), 0.1);
  transform: scale(1.1);
  box-shadow: 0 0 20px rgba(var(--color-primary-rgb), 0.2);
}

.todo-checkbox.checked {
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  border-color: var(--color-primary);
  box-shadow: 
    0 0 20px rgba(var(--color-primary-rgb), 0.4),
    inset 0 2px 4px rgba(255, 255, 255, 0.2);
}

.checkbox-inner {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.checkmark {
  color: white;
  font-weight: var(--font-weight-bold);
  font-size: 16px;
  animation: checkmark-pop 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

@keyframes checkmark-pop {
  0% { 
    transform: scale(0) rotate(180deg); 
    opacity: 0; 
  }
  50% {
    transform: scale(1.3) rotate(90deg);
  }
  100% { 
    transform: scale(1) rotate(0deg); 
    opacity: 1; 
  }
}

/* Enhanced Text Container */
.todo-text-container {
  min-width: 0;
  flex: 1;
}

.todo-text {
  font-size: 1.1rem;
  color: var(--color-text-primary);
  line-height: 1.5;
  word-wrap: break-word;
  display: block;
  transition: all var(--transition-normal);
  font-weight: var(--font-weight-medium);
  letter-spacing: 0.01em;
}

.todo-text.completed {
  text-decoration: line-through;
  color: var(--color-text-muted);
  opacity: 0.7;
}

.todo-edit-input {
  width: 100%;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 2px solid var(--color-primary);
  border-radius: var(--radius-lg);
  padding: var(--space-md);
  color: var(--color-text-primary);
  font-size: 1.1rem;
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-fast);
}

.todo-edit-input:focus {
  border-color: var(--color-primary-light);
  box-shadow: 
    0 0 0 3px rgba(var(--color-primary-rgb), 0.1),
    0 0 20px rgba(var(--color-primary-rgb), 0.2);
  transform: scale(1.02);
}

.priority-edit-selector {
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-sm);
  color: var(--color-text-primary);
  font-size: 0.9rem;
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-fast);
}

.priority-edit-selector:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(var(--color-primary-rgb), 0.1);
}

/* Modern Action Buttons */
.todo-actions {
  display: flex;
  gap: var(--space-sm);
  flex-shrink: 0;
}

.action-btn {
  width: 36px;
  height: 36px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  color: var(--color-text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-normal);
  font-size: 14px;
  position: relative;
  overflow: hidden;
}

.action-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left var(--transition-normal);
}

.action-btn:hover::before {
  left: 100%;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: var(--color-border-hover);
  color: var(--color-text-primary);
  transform: scale(1.1);
  box-shadow: var(--shadow-md);
}

.action-btn:active {
  transform: scale(1.05);
  transition: all 0.1s ease-out;
}

/* Specific Button Colors */
.edit-btn:hover {
  background: rgba(0, 123, 255, 0.2);
  border-color: var(--color-accent-blue);
  color: var(--color-accent-blue);
  box-shadow: 0 0 20px rgba(0, 123, 255, 0.2);
}

.save-btn:hover {
  background: rgba(0, 184, 148, 0.2);
  border-color: var(--color-success);
  color: var(--color-success);
  box-shadow: 0 0 20px rgba(0, 184, 148, 0.2);
}

.cancel-btn:hover {
  background: rgba(255, 118, 117, 0.2);
  border-color: var(--color-accent-orange);
  color: var(--color-accent-orange);
  box-shadow: 0 0 20px rgba(255, 118, 117, 0.2);
}

.delete-btn:hover {
  background: rgba(232, 67, 147, 0.2);
  border-color: var(--color-error);
  color: var(--color-error);
  transform: scale(1.15);
  box-shadow: 0 0 25px rgba(232, 67, 147, 0.3);
}

/* Enhanced Meta Information */
.todo-meta {
  margin-top: var(--space-lg);
  padding-top: var(--space-lg);
  border-top: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
  align-items: flex-start;
}

.creation-date,
.completion-date {
  font-size: 0.8rem;
  font-style: italic;
  font-weight: var(--font-weight-light);
  opacity: 0.8;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  gap: var(--space-xs);
}

.creation-date {
  color: var(--color-text-muted);
}

.completion-date {
  color: var(--color-success);
  font-weight: var(--font-weight-medium);
}

.creation-date::before {
  content: '📅';
  font-size: 0.7rem;
  opacity: 0.6;
}

.completion-date::before {
  content: '✅';
  font-size: 0.7rem;
}

.todo-meta:hover .creation-date,
.todo-meta:hover .completion-date {
  opacity: 1;
}

/* Loading States */
.todo-checkbox.loading {
  opacity: 0.7;
  pointer-events: none;
}

.checkbox-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid transparent;
  border-top: 2px solid var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.btn-spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 1px solid transparent;
  border-top: 1px solid currentColor;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.action-btn:disabled:hover {
  transform: none;
  box-shadow: none;
  background: rgba(0, 0, 0, 0.4);
  border-color: var(--color-border);
  color: var(--color-text-secondary);
}

/* Responsive Design */
@media (max-width: 768px) {
  .todo-item {
    padding: var(--space-lg);
  }
  
  .todo-content {
    gap: var(--space-md);
    grid-template-columns: auto auto 1fr auto;
  }
  
  .todo-text {
    font-size: 1rem;
  }
  
  .action-btn {
    width: 32px;
    height: 32px;
    font-size: 12px;
  }
  
  .todo-actions {
    gap: var(--space-xs);
  }

  .priority-indicator {
    width: 14px;
    height: 14px;
  }

  .todo-checkbox {
    width: 26px;
    height: 26px;
  }
}

@media (max-width: 480px) {
  .todo-content {
    grid-template-columns: 1fr;
    gap: var(--space-md);
    text-align: left;
  }
  
  .todo-text-container {
    order: -2;
    width: 100%;
  }
  
  .priority-edit-selector {
    order: -1;
    width: 100%;
  }

  .priority-indicator,
  .todo-checkbox {
    order: 1;
  }

  .todo-actions {
    order: 2;
    justify-self: start;
  }

  .todo-meta {
    margin-top: var(--space-md);
    padding-top: var(--space-md);
  }
}

/* Performance optimizations */
.todo-item,
.action-btn,
.todo-checkbox,
.priority-indicator {
  will-change: transform;
}

/* Reduce animations on mobile for better performance */
@media (max-width: 768px) {
  .priority-breathe {
    animation-duration: 4s;
  }
  
  .todo-item:hover {
    transform: translateY(-2px) scale(1.01);
  }
  
  .action-btn:hover {
    transform: scale(1.05);
  }
}

/* Accessibility and reduced motion */
@media (prefers-reduced-motion: reduce) {
  .priority-breathe,
  .checkmark-pop,
  .spin {
    animation: none;
  }
  
  .todo-item:hover,
  .action-btn:hover,
  .todo-checkbox:hover {
    transform: none;
  }
  
  .checkbox-spinner,
  .btn-spinner {
    animation: none;
    border-top-color: currentColor;
  }
}
</style>