<template>
  <div>
    <div class="bg-white shadow rounded-lg p-6 mb-6">
      <div class="flex justify-between items-center mb-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-800">Execution History</h1>
          <p class="text-gray-600" v-if="agent">
            For agent: <router-link :to="`/agents/${agentId}`" class="text-indigo-600 hover:text-indigo-800">
              {{ agent.name }}
            </router-link>
          </p>
        </div>
        <router-link
          :to="`/agents/${agentId}?execute=true`"
          class="btn btn-primary"
        >
          Execute Agent
        </router-link>
      </div>
      
      <div v-if="loading" class="text-center py-10">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-indigo-500 border-t-transparent"></div>
        <p class="mt-2 text-gray-600">Loading executions...</p>
      </div>
      
      <div v-else-if="executions.length === 0" class="text-center py-10">
        <p class="text-gray-500">No execution history found for this agent.</p>
        <router-link
          :to="`/agents/${agentId}?execute=true`"
          class="mt-2 inline-block text-indigo-600 hover:text-indigo-800"
        >
          Try executing this agent
        </router-link>
      </div>
      
      <div v-else class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
        <table class="min-w-full divide-y divide-gray-300">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900">Execution ID</th>
              <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Date</th>
              <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Status</th>
              <th scope="col" class="relative py-3.5 pl-3 pr-4">
                <span class="sr-only">Actions</span>
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200 bg-white">
            <tr v-for="execution in executions" :key="execution.id">
              <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900">
                {{ execution.id.substring(0, 8) }}...
              </td>
              <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                {{ new Date(execution.created_at).toLocaleString() }}
              </td>
              <td class="whitespace-nowrap px-3 py-4 text-sm">
                <span 
                  :class="`px-2 py-1 text-xs rounded-full ${
                    execution.status === 'completed' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-yellow-100 text-yellow-800'
                  }`"
                >
                  {{ execution.status }}
                </span>
              </td>
              <td class="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium">
                <router-link 
                  :to="`/agents/${agentId}/executions/${execution.id}`"
                  class="text-indigo-600 hover:text-indigo-900"
                >
                  View details
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'ExecutionList',
  props: {
    agentId: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const store = useStore()
    const router = useRouter()
    
    // Computed properties
    const agent = computed(() => store.state.agentDetail)
    const executions = computed(() => store.state.executions)
    const loading = computed(() => store.state.loading)
    const isAuthenticated = computed(() => store.getters.isAuthenticated)
    
    onMounted(async () => {
      // Redirect to login if not authenticated
      if (!isAuthenticated.value) {
        router.push({ 
          path: '/login', 
          query: { redirect: `/agents/${props.agentId}/executions` } 
        })
        return
      }
      
      // Fetch agent details if not already loaded
      if (!agent.value || agent.value.id !== props.agentId) {
        await store.dispatch('fetchAgentDetail', props.agentId)
      }
      
      // Fetch executions
      await store.dispatch('fetchExecutions', props.agentId)
    })
    
    return {
      agent,
      executions,
      loading
    }
  }
}
</script>
