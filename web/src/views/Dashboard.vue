<template>
  <div>
    <div class="bg-white shadow rounded-lg p-6 mb-6">
      <h1 class="text-2xl font-bold text-gray-800 mb-2">AgentX Marketplace Dashboard</h1>
      <p class="text-gray-600">
        Discover and interact with AI agents for a variety of tasks and capabilities.
      </p>
    </div>

    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="text-indigo-600 font-semibold">Loading dashboard...</div>
    </div>

    <template v-else>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div class="bg-indigo-50 p-6 rounded-lg shadow">
          <h2 class="text-lg font-semibold text-indigo-800 mb-2">Available Agents</h2>
          <p class="text-3xl font-bold text-indigo-600">{{ stats.totalAgents }}</p>
          <router-link
            to="/agents"
            class="mt-4 inline-block text-indigo-600 hover:text-indigo-800"
          >
            Browse all agents →
          </router-link>
        </div>

        <div v-if="isAuthenticated" class="bg-green-50 p-6 rounded-lg shadow">
          <h2 class="text-lg font-semibold text-green-800 mb-2">Your Executions</h2>
          <p class="text-3xl font-bold text-green-600">{{ stats.recentExecutions.length }}</p>
          <router-link
            :to="stats.featuredAgents.length > 0 ? `/agents/${stats.featuredAgents[0].id}/executions` : '/agents'"
            class="mt-4 inline-block text-green-600 hover:text-green-800"
          >
            View execution history →
          </router-link>
        </div>

        <div v-if="isAdmin" class="bg-purple-50 p-6 rounded-lg shadow">
          <h2 class="text-lg font-semibold text-purple-800 mb-2">Admin Actions</h2>
          <router-link
            to="/register-agent"
            class="block mt-2 text-purple-600 hover:text-purple-800"
          >
            Register new agent →
          </router-link>
          <router-link
            to="/agents"
            class="block mt-2 text-purple-600 hover:text-purple-800"
          >
            Manage agents →
          </router-link>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-white shadow rounded-lg p-6">
          <h2 class="text-xl font-bold text-gray-800 mb-4">Featured Agents</h2>
          <div v-if="stats.featuredAgents.length > 0" class="space-y-4">
            <div 
              v-for="agent in stats.featuredAgents" 
              :key="agent.id" 
              class="border-b pb-4 last:border-b-0"
            >
              <h3 class="text-lg font-semibold text-indigo-600">{{ agent.name }}</h3>
              <p class="text-gray-600 text-sm mb-2">{{ agent.description }}</p>
              <div class="flex flex-wrap gap-2 mb-2">
                <span 
                  v-for="tag in agent.tags" 
                  :key="tag" 
                  class="bg-indigo-100 text-indigo-800 text-xs px-2 py-1 rounded-full"
                >
                  {{ tag }}
                </span>
              </div>
              <router-link
                :to="`/agents/${agent.id}`"
                class="text-indigo-600 hover:text-indigo-800 text-sm font-medium"
              >
                View details →
              </router-link>
            </div>
          </div>
          <p v-else class="text-gray-500">No agents available. Be the first to register one!</p>
          <router-link
            to="/agents"
            class="mt-4 inline-block text-indigo-600 hover:text-indigo-800 font-medium"
          >
            See all agents →
          </router-link>
        </div>

        <div v-if="isAuthenticated" class="bg-white shadow rounded-lg p-6">
          <h2 class="text-xl font-bold text-gray-800 mb-4">Recent Executions</h2>
          <div v-if="stats.recentExecutions.length > 0" class="space-y-4">
            <div 
              v-for="execution in stats.recentExecutions" 
              :key="execution.id" 
              class="border-b pb-4 last:border-b-0"
            >
              <div class="flex justify-between items-start">
                <div>
                  <h3 class="text-gray-800 font-medium">Execution ID: {{ execution.id.substring(0, 8) }}...</h3>
                  <p class="text-gray-500 text-sm">
                    {{ new Date(execution.created_at).toLocaleString() }}
                  </p>
                </div>
                <span 
                  :class="`px-2 py-1 text-xs rounded-full ${
                    execution.status === 'completed' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-yellow-100 text-yellow-800'
                  }`"
                >
                  {{ execution.status }}
                </span>
              </div>
              <router-link
                :to="`/agents/${execution.agent_id}/executions/${execution.id}`"
                class="text-indigo-600 hover:text-indigo-800 text-sm font-medium"
              >
                View details →
              </router-link>
            </div>
          </div>
          <p v-else class="text-gray-500">No recent executions. Try running an agent!</p>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { mapGetters, mapActions, mapState } from 'vuex'
import { ref, onMounted } from 'vue'

export default {
  name: 'Dashboard',
  setup() {
    const stats = ref({
      totalAgents: 0,
      featuredAgents: [],
      recentExecutions: []
    })

    return {
      stats
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'isAdmin']),
    ...mapState(['loading', 'agents'])
  },
  methods: {
    ...mapActions(['fetchAgents']),
    
    async loadDashboardData() {
      // Fetch agents if not already loaded
      if (this.agents.length === 0) {
        await this.fetchAgents()
      }
      
      // Calculate dashboard stats
      this.stats.totalAgents = this.agents.length
      
      // Get featured agents (just taking a few for display)
      this.stats.featuredAgents = this.agents.slice(0, 3)
      
      // Get recent executions
      // In a real app, we would fetch this from the API
      this.stats.recentExecutions = this.isAuthenticated && this.agents.length > 0 
        ? [
            {
              id: 'execution-1',
              agent_id: this.agents[0].id,
              created_at: new Date().toISOString(),
              status: 'completed'
            },
            {
              id: 'execution-2',
              agent_id: this.agents[0].id,
              created_at: new Date(Date.now() - 3600000).toISOString(),
              status: 'pending'
            }
          ]
        : []
    }
  },
  mounted() {
    this.loadDashboardData()
  }
}
</script>