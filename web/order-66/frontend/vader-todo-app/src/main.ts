import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './style.css'
import { useTodoStore } from './stores/todoStore'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Initialize the todo store after mounting
app.mount('#app')

// Initialize store after app is mounted
const todoStore = useTodoStore()
todoStore.initialize().catch(error => {
  console.error('Failed to initialize todo store:', error)
})