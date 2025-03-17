<template>
  <div class="flex justify-center items-center min-h-[70vh]">
    <div class="w-full max-w-md">
      <div class="bg-white p-8 shadow rounded-lg">
        <div class="text-center mb-6">
          <h1 class="text-2xl font-bold text-gray-800">Login to Agent Marketplace</h1>
          <p class="text-gray-600 mt-2">Enter your API key to access the marketplace</p>
        </div>
        
        <div v-if="error" class="bg-red-50 text-red-700 p-3 rounded mb-4">
          {{ error }}
        </div>
        
        <form @submit.prevent="handleSubmit">
          <div class="mb-4">
            <label 
              for="apiKey" 
              class="form-label"
            >
              API Key
            </label>
            <input
              type="password"
              id="apiKey"
              v-model="apiKey"
              placeholder="Enter your API key"
              class="form-input p-3"
              autofocus
            />
            <p class="mt-1 text-xs text-gray-500">
              For testing, you can use: <code class="bg-gray-100 px-1 py-0.5 rounded">test_key</code>
            </p>
          </div>
          
          <button
            type="submit"
            :disabled="loading"
            :class="`w-full btn btn-primary py-3 ${
              loading ? 'opacity-75 cursor-not-allowed' : ''
            }`"
          >
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </form>
        
        <div class="mt-6 text-center text-sm text-gray-600">
          <p>
            Don't have an API key? Contact your administrator or check the documentation for details
            on how to obtain one.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'

export default {
  name: 'Login',
  setup() {
    const store = useStore()
    const router = useRouter()
    const route = useRoute()
    
    const apiKey = ref('')
    const error = ref('')
    const loading = ref(false)
    
    // If user is already authenticated, redirect them
    const isAuthenticated = computed(() => store.getters.isAuthenticated)
    const redirect = computed(() => route.query.redirect || '/')
    
    watch(isAuthenticated, (value) => {
      if (value) {
        router.push(redirect.value)
      }
    })
    
    onMounted(() => {
      if (isAuthenticated.value) {
        router.push(redirect.value)
      }
    })
    
    const handleSubmit = async () => {
      if (!apiKey.value.trim()) {
        error.value = 'API key is required'
        return
      }
      
      try {
        loading.value = true
        error.value = ''
        
        // Attempt to login with the provided API key
        await store.dispatch('login', apiKey.value)
        
        // Navigate to the page they were trying to access
        router.push(redirect.value)
      } catch (err) {
        console.error('Login error:', err)
        error.value = 'Invalid API key. Please try again.'
      } finally {
        loading.value = false
      }
    }
    
    return {
      apiKey,
      error,
      loading,
      handleSubmit
    }
  }
}
</script>