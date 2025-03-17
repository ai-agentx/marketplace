<template>
  <div class="space-y-6">
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="text-indigo-600 font-semibold">Loading agent details...</div>
    </div>
    
    <template v-else-if="agent">
      <div class="bg-white shadow rounded-lg overflow-hidden">
        <!-- Header -->
        <div class="p-6 border-b">
          <div class="flex justify-between items-start">
            <div>
              <h1 class="text-2xl font-bold text-gray-800">{{ agent.name }}</h1>
              <p class="text-gray-500">
                By: {{ agent.author }} • Version: {{ agent.version }}
              </p>
            </div>
            <div class="flex space-x-2">
              <router-link
                :to="`/agents/${agentId}/executions`"
                class="bg-gray-100 text-gray-700 px-3 py-1 rounded hover:bg-gray-200"
              >
                Execution History
              </router-link>
              
              <template v-if="isAdmin">
                <router-link
                  :to="`/agents/${agentId}/edit`"
                  class="bg-indigo-100 text-indigo-700 px-3 py-1 rounded hover:bg-indigo-200"
                >
                  Edit
                </router-link>
                <button
                  @click="handleDeleteAgent"
                  class="bg-red-100 text-red-700 px-3 py-1 rounded hover:bg-red-200"
                >
                  Delete
                </button>
              </template>
              
              <button
                @click="showExecuteForm = !showExecuteForm"
                :class="`px-3 py-1 rounded ${
                  showExecuteForm
                    ? 'bg-gray-200 text-gray-800'
                    : 'bg-indigo-600 text-white hover:bg-indigo-500'
                }`"
              >
                {{ showExecuteForm ? 'Hide Execution' : 'Execute Agent' }}
              </button>
            </div>
          </div>
          <div class="flex flex-wrap mt-4 gap-2">
            <span 
              v-for="tag in agent.tags" 
              :key="tag" 
              class="bg-indigo-50 text-indigo-700 text-xs px-2 py-1 rounded-full"
            >
              {{ tag }}
            </span>
          </div>
        </div>

        <!-- Details -->
        <div class="p-6">
          <h2 class="text-xl font-semibold text-gray-800 mb-4">Description</h2>
          <p class="text-gray-700 mb-6">{{ agent.description }}</p>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <h3 class="text-lg font-medium text-gray-800 mb-2">Details</h3>
              <div class="bg-gray-50 p-4 rounded">
                <dl class="space-y-2">
                  <div class="grid grid-cols-3 gap-2">
                    <dt class="text-gray-500">API Endpoint:</dt>
                    <dd class="col-span-2 text-gray-700">{{ agent.api_endpoint }}</dd>
                  </div>
                  <div class="grid grid-cols-3 gap-2">
                    <dt class="text-gray-500">Auth Type:</dt>
                    <dd class="col-span-2 text-gray-700">{{ agent.auth_type }}</dd>
                  </div>
                  <div class="grid grid-cols-3 gap-2">
                    <dt class="text-gray-500">Pricing Model:</dt>
                    <dd class="col-span-2 text-gray-700">{{ agent.pricing_model || 'Free' }}</dd>
                  </div>
                  <div v-if="agent.pricing_model !== 'free' && agent.pricing_details" class="grid grid-cols-3 gap-2">
                    <dt class="text-gray-500">Pricing Details:</dt>
                    <dd class="col-span-2 text-gray-700">
                      {{ agent.pricing_details.cost_per_call }} {{ agent.pricing_details.currency }} per call
                    </dd>
                  </div>
                  <div v-if="agent.contact_email" class="grid grid-cols-3 gap-2">
                    <dt class="text-gray-500">Contact:</dt>
                    <dd class="col-span-2 text-gray-700">
                      <a 
                        :href="`mailto:${agent.contact_email}`" 
                        class="text-indigo-600 hover:text-indigo-800"
                      >
                        {{ agent.contact_email }}
                      </a>
                    </dd>
                  </div>
                  <div v-if="agent.homepage_url" class="grid grid-cols-3 gap-2">
                    <dt class="text-gray-500">Homepage:</dt>
                    <dd class="col-span-2 text-gray-700">
                      <a 
                        :href="agent.homepage_url"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="text-indigo-600 hover:text-indigo-800"
                      >
                        {{ agent.homepage_url }}
                      </a>
                    </dd>
                  </div>
                </dl>
              </div>
            </div>
            
            <div>
              <h3 class="text-lg font-medium text-gray-800 mb-2">Capabilities</h3>
              <div class="space-y-4">
                <div 
                  v-for="(capability, index) in agent.capabilities" 
                  :key="index" 
                  class="bg-gray-50 p-4 rounded"
                >
                  <h4 class="font-medium text-gray-800">{{ capability.name }}</h4>
                  <p class="text-gray-600 text-sm mb-2">{{ capability.description }}</p>
                  <div v-if="capability.parameters && Object.keys(capability.parameters).length > 0">
                    <h5 class="text-sm font-medium text-gray-700 mt-2">Parameters:</h5>
                    <ul class="mt-1 text-sm text-gray-600">
                      <li 
                        v-for="(paramConfig, paramName) in capability.parameters" 
                        :key="paramName"
                        class="ml-4 list-disc"
                      >
                        <span class="font-medium">{{ paramName }}</span>
                        <template v-if="paramConfig.description">: {{ paramConfig.description }}</template>
                        <template v-if="paramConfig.default !== undefined"> (Default: {{ paramConfig.default }})</template>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Execution Form -->
      <div v-if="showExecuteForm" class="bg-white shadow rounded-lg overflow-hidden">
        <div class="p-6 border-b">
          <h2 class="text-xl font-semibold text-gray-800">Execute Agent</h2>
          <p class="text-gray-600">
            {{ primaryCapability 
              ? `Execute the ${primaryCapability.name} capability.`
              : 'Execute this agent.' }}
          </p>
        </div>
        
        <div class="p-6">
          <form @submit.prevent="handleExecute">
            <!-- Input Data -->
            <div class="mb-6">
              <h3 class="text-lg font-medium text-gray-800 mb-3">Input Data</h3>
              <div v-if="primaryCapability && primaryCapability.parameters" class="space-y-4">
                <div 
                  v-for="(paramConfig, paramName) in primaryCapability.parameters" 
                  :key="paramName"
                >
                  <label 
                    :for="paramName" 
                    class="form-label"
                  >
                    {{ paramName }} <template v-if="paramConfig.description">({{ paramConfig.description }})</template>
                  </label>
                  <input
                    :type="paramConfig.type === 'integer' ? 'number' : 'text'"
                    :id="paramName"
                    v-model="executionInputData[paramName]"
                    :placeholder="paramConfig.default !== undefined ? `Default: ${paramConfig.default}` : ''"
                    class="form-input"
                  />
                </div>
              </div>
              <div v-else>
                <label for="text" class="form-label">
                  Input Text
                </label>
                <textarea
                  id="text"
                  v-model="executionInputData.text"
                  rows="4"
                  placeholder="Enter your input text here..."
                  class="form-input"
                ></textarea>
              </div>
            </div>

            <!-- Execution Parameters -->
            <div v-if="primaryCapability && primaryCapability.parameters" class="mb-6">
              <h3 class="text-lg font-medium text-gray-800 mb-3">Execution Parameters</h3>
              <div class="space-y-4">
                <div>
                  <label for="max_tokens" class="form-label">
                    Max Tokens
                  </label>
                  <input
                    type="number"
                    id="max_tokens"
                    v-model="executionParams.max_tokens"
                    placeholder="Default: 1000"
                    class="form-input"
                  />
                </div>
              </div>
            </div>
            
            <div class="flex justify-end">
              <button
                type="submit"
                :disabled="executionLoading"
                :class="`btn btn-primary ${
                  executionLoading ? 'opacity-75 cursor-not-allowed' : ''
                }`"
              >
                {{ executionLoading ? 'Executing...' : 'Execute Agent' }}
              </button>
            </div>
          </form>

          <!-- Execution Results -->
          <div v-if="executionError" class="mt-6 bg-red-50 p-4 rounded-md text-red-700">
            <p>{{ executionError }}</p>
          </div>
          
          <div v-if="executionResult" class="mt-6">
            <h3 class="text-lg font-medium text-gray-800 mb-3">Execution Results</h3>
            <div class="bg-gray-50 p-4 rounded-md">
              <div class="mb-2 flex justify-between">
                <span class="text-gray-500">Status: 
                  <span :class="`ml-2 px-2 py-1 text-xs rounded-full ${
                    executionResult.status === 'completed' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-yellow-100 text-yellow-800'
                  }`">
                    {{ executionResult.status }}
                  </span>
                </span>
                <span class="text-gray-500">ID: 
                  <span class="ml-2 text-gray-700">{{ executionResult.id.substring(0, 8) }}...</span>
                </span>
              </div>
              <div class="border-t pt-4 mt-2">
                <h4 class="font-medium text-gray-800 mb-2">Result:</h4>
                <pre class="bg-gray-100 p-3 rounded text-sm overflow-x-auto">
                  {{ JSON.stringify(executionResult.result, null, 2) }}
                </pre>
              </div>
              <div class="mt-4 text-right">
                <router-link
                  :to="`/agents/${agentId}/executions/${executionResult.id}`"
                  class="text-indigo-600 hover:text-indigo-800"
                >
                  View Full Execution Details →
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    
    <div v-else-if="error" class="bg-red-50 p-4 rounded-md text-red-700 mb-6">
      <p>{{ error }}</p>
      <button
        @click="$router.push('/agents')"
        class="mt-4 text-indigo-600 hover:text-indigo-800"
      >
        Return to agent list
      </button>
    </div>
    
    <div v-else class="bg-yellow-50 p-4 rounded-md text-yellow-700 mb-6">
      <p>Agent not found.</p>
      <button
        @click="$router.push('/agents')"
        class="mt-4 text-indigo-600 hover:text-indigo-800"
      >
        Return to agent list
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex'

export default {
  name: 'AgentDetail',
  props: {
    agentId: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const store = useStore()
    const route = useRoute()
    const router = useRouter()
    
    const agent = computed(() => store.state.agentDetail)
    const loading = computed(() => store.state.loading)
    const isAuthenticated = computed(() => store.getters.isAuthenticated)
    const isAdmin = computed(() => store.getters.isAdmin)
    
    const showExecuteForm = ref(false)
    const executionParams = ref({})
    const executionInputData = ref({})
    const executionLoading = ref(false)
    const executionResult = ref(null)
    const executionError = ref(null)
    const error = ref(null)
    
    // Check if we should show the execution form based on URL parameter
    watch(() => route.query, (query) => {
      if (query.execute === 'true') {
        showExecuteForm.value = true
      }
    }, { immediate: true })
    
    // Get primary capability for execution form
    const primaryCapability = computed(() => {
      if (agent.value?.capabilities?.length > 0) {
        return agent.value.capabilities[0]
      }
      return null
    })
    
    // Initialize execution parameters with defaults when agent data is loaded
    watch(agent, (newAgent) => {
      if (newAgent?.capabilities?.length > 0) {
        const capability = newAgent.capabilities[0]
        if (capability.parameters) {
          // Extract default parameter values
          const defaultParams = {}
          Object.entries(capability.parameters).forEach(([key, paramConfig]) => {
            if (paramConfig.default !== undefined) {
              defaultParams[key] = paramConfig.default
            }
          })
          executionParams.value = defaultParams
        }
      }
    })
    
    // Fetch agent details
    onMounted(async () => {
      try {
        await store.dispatch('fetchAgentDetail', props.agentId)
      } catch (err) {
        error.value = 'Failed to load agent details. Please try again later.'
      }
    })
    
    // Handle execution
    const handleExecute = async () => {
      if (!isAuthenticated.value) {
        router.push({ 
          path: '/login', 
          query: { redirect: `/agents/${props.agentId}?execute=true` } 
        })
        return
      }
      
      try {
        executionLoading.value = true
        executionError.value = null
        executionResult.value = null
        
        // Prepare execution request
        const executionRequest = {
          agent_id: props.agentId,
          input_data: executionInputData.value,
          execution_parameters: executionParams.value,
          auth_credentials: {} // In a real app, you'd include auth credentials if needed
        }
        
        // Execute the agent
        const result = await store.dispatch('executeAgent', {
          agentId: props.agentId,
          executionData: executionRequest
        })
        
        executionResult.value = result
      } catch (err) {
        executionError.value = 'Failed to execute agent. Please check your parameters and try again.'
      } finally {
        executionLoading.value = false
      }
    }
    
    // Handle delete
    const handleDeleteAgent = async () => {
      if (confirm('Are you sure you want to delete this agent? This action cannot be undone.')) {
        try {
          await store.dispatch('deleteAgent', props.agentId)
          router.push({ 
            path: '/agents', 
            query: { message: `Agent "${agent.value.name}" deleted successfully.` } 
          })
        } catch (err) {
          alert('Failed to delete agent. Please try again later.')
        }
      }
    }
    
    return {
      agent,
      loading,
      isAuthenticated,
      isAdmin,
      showExecuteForm,
      executionParams,
      executionInputData,
      executionLoading,
      executionResult,
      executionError,
      error,
      primaryCapability,
      handleExecute,
      handleDeleteAgent
    }
  }
}
</script>
