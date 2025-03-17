<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar />
    <main class="container mx-auto px-4 py-6">
      <div v-if="globalError" class="bg-red-50 p-4 rounded-md text-red-700 mb-6">
        <h3 class="font-medium">{{ globalError.message }}</h3>
        <p v-if="globalError.details" class="mt-1 text-sm">{{ globalError.details }}</p>
        <button 
          @click="clearError" 
          class="mt-2 text-red-700 hover:text-red-900 text-sm font-medium"
        >
          Dismiss
        </button>
      </div>
      <router-view />
    </main>
    <footer class="bg-white shadow-inner p-4 mt-8">
      <div class="container mx-auto text-center text-gray-500">
        <p>© 2025 AgentX Marketplace. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import Navbar from '@/components/Navbar.vue'

export default {
  name: 'App',
  components: {
    Navbar
  },
  computed: {
    ...mapState(['globalError'])
  },
  methods: {
    ...mapActions(['clearError'])
  }
}
</script>
