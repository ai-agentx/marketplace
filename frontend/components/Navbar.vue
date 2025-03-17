<template>
  <nav class="bg-indigo-600 shadow-md">
    <div class="container mx-auto px-4">
      <div class="flex justify-between h-16">
        <div class="flex">
          <div class="flex-shrink-0 flex items-center">
            <router-link to="/" class="text-white font-bold text-xl">
              Agent Marketplace
            </router-link>
          </div>
          <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
            <router-link
              to="/"
              class="text-white hover:text-indigo-100 px-3 py-2 rounded-md text-sm font-medium"
            >
              Dashboard
            </router-link>
            <router-link
              to="/agents"
              class="text-white hover:text-indigo-100 px-3 py-2 rounded-md text-sm font-medium"
            >
              Browse Agents
            </router-link>
            <router-link
              v-if="isAuthenticated"
              to="/register-agent"
              class="text-white hover:text-indigo-100 px-3 py-2 rounded-md text-sm font-medium"
            >
              Register Agent
            </router-link>
          </div>
        </div>
        
        <div class="hidden sm:ml-6 sm:flex sm:items-center">
          <div v-if="isAuthenticated" class="flex items-center space-x-4">
            <span class="text-white text-sm">
              {{ isAdmin ? 'Admin' : 'User' }}
            </span>
            <button
              @click="logout"
              class="bg-indigo-500 text-white hover:bg-indigo-400 px-3 py-2 rounded-md text-sm font-medium"
            >
              Logout
            </button>
          </div>
          <router-link
            v-else
            to="/login"
            class="bg-white text-indigo-600 hover:bg-indigo-50 px-3 py-2 rounded-md text-sm font-medium"
          >
            Login
          </router-link>
        </div>
        
        <!-- Mobile menu button -->
        <div class="-mr-2 flex items-center sm:hidden">
          <button
            @click="isMenuOpen = !isMenuOpen"
            class="inline-flex items-center justify-center p-2 rounded-md text-indigo-100 hover:text-white hover:bg-indigo-500 focus:outline-none focus:bg-indigo-500 focus:text-white"
          >
            <svg
              class="h-6 w-6"
              stroke="currentColor"
              fill="none"
              viewBox="0 0 24 24"
            >
              <path
                v-if="isMenuOpen"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
              <path
                v-else
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile menu -->
    <div v-if="isMenuOpen" class="sm:hidden">
      <div class="pt-2 pb-3 space-y-1">
        <router-link
          to="/"
          class="text-white hover:bg-indigo-500 block px-3 py-2 rounded-md text-base font-medium"
          @click="isMenuOpen = false"
        >
          Dashboard
        </router-link>
        <router-link
          to="/agents"
          class="text-white hover:bg-indigo-500 block px-3 py-2 rounded-md text-base font-medium"
          @click="isMenuOpen = false"
        >
          Browse Agents
        </router-link>
        <router-link
          v-if="isAuthenticated"
          to="/register-agent"
          class="text-white hover:bg-indigo-500 block px-3 py-2 rounded-md text-base font-medium"
          @click="isMenuOpen = false"
        >
          Register Agent
        </router-link>
      </div>
      <div class="pt-4 pb-3 border-t border-indigo-500">
        <div v-if="isAuthenticated" class="flex items-center px-5">
          <div class="ml-3">
            <div class="text-base font-medium leading-none text-white">
              {{ isAdmin ? 'Admin' : 'User' }}
            </div>
            <button
              @click="handleMobileLogout"
              class="mt-3 bg-indigo-500 text-white hover:bg-indigo-400 px-3 py-2 rounded-md text-sm font-medium"
            >
              Logout
            </button>
          </div>
        </div>
        <div v-else class="mt-3 px-2 space-y-1">
          <router-link
            to="/login"
            class="block px-3 py-2 rounded-md text-base font-medium text-white bg-indigo-500 hover:bg-indigo-400"
            @click="isMenuOpen = false"
          >
            Login
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'Navbar',
  setup() {
    const isMenuOpen = ref(false)
    const router = useRouter()
    
    const handleMobileLogout = async function() {
      isMenuOpen.value = false
      await this.logout()
      router.push('/login')
    }
    
    return {
      isMenuOpen,
      handleMobileLogout
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'isAdmin'])
  },
  methods: {
    ...mapActions(['logout']),
    async handleLogout() {
      await this.logout()
      this.$router.push('/login')
    }
  }
}
</script>
