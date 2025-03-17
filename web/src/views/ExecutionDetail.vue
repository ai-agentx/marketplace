<template>
  <div>
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="text-indigo-600 font-semibold">Loading execution details...</div>
    </div>
    
    <template v-else-if="execution">
      <div class="bg-white shadow rounded-lg overflow-hidden mb-6">
        <div class="p-6 border-b">
          <div class="flex justify-between items-start">
            <div>
              <h1 class="text-2xl font-bold text-gray-800">Execution Details</h1>
              <p class="text-gray-600" v-if="agent">
                For agent: <router-link :to="`/agents/${agentId}`" class="text-indigo-600 hover:text-indigo-800">
                  {{ agent.name }}
                </router-link>
              </p>
            </div>
            <div class="flex space-x-2">
              <router-link
                :to="`/agents/${agentId}/executions`"
                class="bg-gray-100 text-gray-700 px-3 py-1 rounded hover:bg-gray-200"
              >
                View All Executions
              </router-link>
              <router-link
                :to="`/agents/${agentId}?execute=true`"
                class="bg-indigo-600 text-white px-3 py-1 rounded hover:bg-indigo-500"
              >
                Execute Again
              </router-link>
            </div>
          </div>
        </div>
        
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <h2 class="text-lg font-medium text-gray-800 mb-3">Execution Information</h2>
              <div class="bg-gray-50 p-4 rounded">
                <dl class="space-y-2">
                  <div class="grid grid-cols-3 gap-2">
                    <dt class="text-gray-500">Execution ID:</dt>
                    <dd class="col-span-2 text-gray-700">{{ execution.id }}</dd>
                  </div>
                  <div class="grid grid-cols-3 gap-2">
                    <dt class="text-gray-500">Created At:</dt>
                    <dd class="col-span-2 text-gray-700">{{ new Date(execution.created_at).toLocaleString() }}</dd>
                  </div>
                  <div class="grid grid-cols-3 gap-2">
                    <dt class="text-gray-500">Completed At:</dt>
                    <dd class="col-span-2 text-gray-700">
                      {{ execution.completed_at ? new Date(execution.completed_at).toLocaleString() : 'N/A' }}
                    </dd>
                  </div>
                  <div class="grid grid-cols-3 gap-2">
                    <dt class="text-gray-500">Status:</dt>
                    <dd class="col-span-2">
                      <span 
                        :class="`px-2 py-1 text-xs rounded-full ${
                          execution.status === 'completed' 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-yellow-100 text-yellow-800'
                        }`"
                      >
                        {{ execution.status }}
                      </span>
                    </dd>
                  </div>
                </dl>
              </div>
            </div>
            
            <div>
              <h2 class="text-lg font-medium text-gray-800 mb-3">Input Data</h2>
              <div class="bg-gray-50 p-4 rounded">
                <pre class="text-sm overflow-x-auto whitespace-pre-wrap break-words text-gray-700">{{ JSON.stringify(execution.input, null, 2) }}</pre>
              </div>
            </div>
          </div>
          
          <div v-if="execution.parameters && Object.keys(execution.parameters).length > 0" class="mb-6">
            <h2 class="text-lg font-medium text-gray-800 mb-3">Execution Parameters</h2>
            <div class="bg-gray-50 p-4 rounded">
              <pre class="text-sm overflow-x-auto whitespace-pre-wrap break-words text-gray-700">{{ JSON.stringify(execution.parameters, null, 2) }}</pre>
            </div>
          </div>
          
          <div>
            <h2 class="text-lg font-medium text-gray-800 mb-3">Result</h2>
            <div class="bg-gray-50 p-4 rounded">
              <pre class="text-sm overflow-x-auto whitespace-pre-wrap break-words text-gray-700">{{ JSON.stringify(execution.result, null, 2) }}</pre>
            </div>
          </div>
        </div>
      </div>
    </template>
    
    <div v-else-if="error" class="bg-red-50 p-4 rounded-md text-red-700 mb-6">
      <p>{{ error }}</p>
      <router-link
        :to="`/agents/${agentId}/executions`"
        class="mt-4 inline-block text-indigo-600 hover:text-indigo-800"
      >
        Return to execution list
      </router-link>
    </div>
    
    <div v-else class="bg-yellow-50 p-4 rounded-md text-yellow-700 mb-6">
      <p>Execution not found.</p>
      <router-link
        :to="`/agents/${agentId}/executions`"
        class="mt-4 inline-block text-indigo-600 hover:text-indigo-800"
      >
        Return to execution list
      </router-link>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'ExecutionDetail',
  props: {
    agentId: {
      type: String,
      required: true
    },
    executionId: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const store = useStore()
    const router = useRouter()
    
    const error = ref(null)
    
    // Computed properties
    const agent = computed(() => store.state.agentDetail)
    const execution = computed(() => store.state.executionDetail)
    const loading = computed(() => store.state.loading)
    const isAuthenticated = computed(() => store.getters.isAuthenticated)
    
    onMounted(async () => {
      // Redirect to login if not authenticated
      if (!isAuthenticated.value) {
        router.push({ 
          path: '/login', 
          query: { redirect: `/agents/${props.agentId}/executions/${props.executionId}` } 
        })
        return
      }
      
      try {
        // Fetch agent details if not already loaded
        if (!agent.value || agent.value.id !== props.agentId) {
          await store.dispatch('fetchAgentDetail', props.agentId)
        }
        
        // Fetch execution details
        await store.dispatch('fetchExecutionDetail', {
          agentId: props.agentId,
          executionId: props.executionId
        })
      } catch (err) {
        console.error('Error fetching execution details:', err)
        error.value = 'Failed to load execution details. Please try again later.'
      }
    })
    
    return {
      agent,
      execution,
      loading,
      error
    }
  }
}
</script>
