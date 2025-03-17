import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './assets/tailwind.css'

const app = createApp(App)

// Global error handler
app.config.errorHandler = (err, vm, info) => {
  console.error('Global error:', err)
  store.dispatch('setError', {
    message: 'An unexpected error occurred',
    details: err.message
  })
}

app.use(router)
app.use(store)
app.mount('#app')
