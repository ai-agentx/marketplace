<template>
  <div class="bg-white shadow rounded-lg overflow-hidden">
    <div class="p-6 border-b">
      <h1 class="text-2xl font-bold text-gray-800">Register a New Agent</h1>
      <p class="text-gray-600 mt-2">
        Fill out the form below to register your AI agent in the marketplace
      </p>
    </div>
    
    <div v-if="success" class="bg-green-50 m-6 p-4 rounded-md text-green-700">
      <h3 class="font-medium">Agent Registered Successfully!</h3>
      <p class="mt-2">Your agent has been registered with ID: {{ registeredAgentId }}</p>
      <div class="mt-4 flex space-x-4">
        <router-link 
          :to="`/agents/${registeredAgentId}`"
          class="text-green-700 font-medium hover:text-green-900"
        >
          View Agent Details
        </router-link>
        <button
          @click="resetForm"
          class="text-indigo-600 font-medium hover:text-indigo-800"
        >
          Register Another Agent
        </button>
      </div>
    </div>
    
    <form v-else @submit.prevent="handleSubmit" class="p-6 space-y-6">
      <!-- Basic Information -->
      <div>
        <h2 class="text-lg font-semibold text-gray-800 mb-4">Basic Information</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label for="name" class="form-label">Name <span class="text-red-500">*</span></label>
            <input 
              id="name" 
              v-model="formData.name" 
              type="text" 
              class="form-input" 
              :class="{'border-red-500': formErrors.name}"
              placeholder="Agent name"
            />
            <p v-if="formErrors.name" class="mt-1 text-sm text-red-600">{{ formErrors.name }}</p>
          </div>
          
          <div>
            <label for="version" class="form-label">Version <span class="text-red-500">*</span></label>
            <input 
              id="version" 
              v-model="formData.version" 
              type="text" 
              class="form-input" 
              :class="{'border-red-500': formErrors.version}"
              placeholder="e.g., 1.0.0"
            />
            <p v-if="formErrors.version" class="mt-1 text-sm text-red-600">{{ formErrors.version }}</p>
          </div>
          
          <div>
            <label for="author" class="form-label">Author <span class="text-red-500">*</span></label>
            <input 
              id="author" 
              v-model="formData.author" 
              type="text" 
              class="form-input" 
              :class="{'border-red-500': formErrors.author}"
              placeholder="Your name or organization"
            />
            <p v-if="formErrors.author" class="mt-1 text-sm text-red-600">{{ formErrors.author }}</p>
          </div>
          
          <div>
            <label for="contact_email" class="form-label">Contact Email</label>
            <input 
              id="contact_email" 
              v-model="formData.contact_email" 
              type="email" 
              class="form-input"
              :class="{'border-red-500': formErrors.contact_email}"
              placeholder="contact@example.com"
            />
            <p v-if="formErrors.contact_email" class="mt-1 text-sm text-red-600">{{ formErrors.contact_email }}</p>
          </div>
          
          <div class="md:col-span-2">
            <label for="description" class="form-label">Description <span class="text-red-500">*</span></label>
            <textarea 
              id="description" 
              v-model="formData.description" 
              rows="3" 
              class="form-input"
              :class="{'border-red-500': formErrors.description}"
              placeholder="Describe what your agent does"
            ></textarea>
            <p v-if="formErrors.description" class="mt-1 text-sm text-red-600">{{ formErrors.description }}</p>
          </div>
          
          <div>
            <label for="homepage_url" class="form-label">Homepage URL</label>
            <input 
              id="homepage_url" 
              v-model="formData.homepage_url" 
              type="url" 
              class="form-input"
              :class="{'border-red-500': formErrors.homepage_url}"
              placeholder="https://example.com"
            />
            <p v-if="formErrors.homepage_url" class="mt-1 text-sm text-red-600">{{ formErrors.homepage_url }}</p>
          </div>
          
          <div>
            <label for="api_endpoint" class="form-label">API Endpoint <span class="text-red-500">*</span></label>
            <input 
              id="api_endpoint" 
              v-model="formData.api_endpoint" 
              type="url" 
              class="form-input"
              :class="{'border-red-500': formErrors.api_endpoint}"
              placeholder="https://api.example.com/agent"
            />
            <p v-if="formErrors.api_endpoint" class="mt-1 text-sm text-red-600">{{ formErrors.api_endpoint }}</p>
          </div>
        </div>
      </div>
      
      <!-- Tags -->
      <div>
        <h2 class="text-lg font-semibold text-gray-800 mb-4">Tags</h2>
        <div class="flex items-center mb-2">
          <input 
            v-model="tagInput" 
            type="text" 
            placeholder="Add a tag..." 
            class="form-input"
            @keydown.enter.prevent="addTag"
          />
          <button
            type="button" 
            @click="addTag"
            class="ml-2 bg-indigo-600 text-white p-2 rounded hover:bg-indigo-500"
          >
            Add
          </button>
        </div>
        <div class="flex flex-wrap gap-2 mt-2">
          <span 
            v-for="(tag, index) in formData.tags" 
            :key="index"
            class="bg-indigo-50 text-indigo-700 px-2 py-1 rounded-full flex items-center"
          >
            {{ tag }}
            <button 
              type="button"
              @click="removeTag(index)" 
              class="ml-1 text-indigo-500 hover:text-indigo-700"
            >
              &times;
            </button>
          </span>
        </div>
      </div>
      
      <!-- Capabilities -->
      <div>
        <h2 class="text-lg font-semibold text-gray-800 mb-4">Capabilities</h2>
        <p v-if="formErrors.capabilities" class="mt-1 text-sm text-red-600">{{ formErrors.capabilities }}</p>
        
        <div 
          v-for="(capability, index) in formData.capabilities" 
          :key="index"
          class="border rounded-md p-4 mb-4"
        >
          <div class="flex justify-between items-center mb-4">
            <h3 class="font-medium text-gray-800">Capability {{ index + 1 }}</h3>
            <button
              v-if="formData.capabilities.length > 1"
              type="button"
              @click="removeCapability(index)"
              class="text-red-600 hover:text-red-800"
            >
              Remove
            </button>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label :for="`capability_${index}_name`" class="form-label">Name <span class="text-red-500">*</span></label>
              <input 
                :id="`capability_${index}_name`" 
                v-model="capability.name" 
                type="text" 
                class="form-input"
                :class="{'border-red-500': formErrors[`capability_${index}_name`]}"
                placeholder="e.g., summarize_text"
              />
              <p v-if="formErrors[`capability_${index}_name`]" class="mt-1 text-sm text-red-600">
                {{ formErrors[`capability_${index}_name`] }}
              </p>
            </div>
            
            <div class="md:col-span-2">
              <label :for="`capability_${index}_description`" class="form-label">Description <span class="text-red-500">*</span></label>
              <textarea 
                :id="`capability_${index}_description`" 
                v-model="capability.description" 
                rows="2" 
                class="form-input"
                :class="{'border-red-500': formErrors[`capability_${index}_description`]}"
                placeholder="Describe what this capability does"
              ></textarea>
              <p v-if="formErrors[`capability_${index}_description`]" class="mt-1 text-sm text-red-600">
                {{ formErrors[`capability_${index}_description`] }}
              </p>
            </div>
          </div>
          
          <div>
            <h4 class="text-sm font-medium text-gray-800 mb-2">Parameters</h4>
            <div class="mb-2">
              <textarea 
                v-model="parametersInput" 
                rows="4" 
                class="form-input text-sm font-mono"
                placeholder='{"text": {"type": "string", "description": "The text to summarize"}, "max_bullets": {"type": "integer", "description": "Maximum number of bullet points", "default": 5}}'
              ></textarea>
              <p class="mt-1 text-xs text-gray-500">
                Enter parameters as a JSON object. Example: <code>{"param_name": {"type": "string", "description": "Description", "default": "Default value"}}</code>
              </p>
            </div>
            <div class="flex justify-end">
              <button
                type="button"
                @click="parseParameters(index)"
                class="text-indigo-600 hover:text-indigo-800 text-sm"
              >
                Parse Parameters
              </button>
            </div>
            
            <div v-if="Object.keys(capability.parameters).length > 0" class="mt-2 border-t pt-2">
              <h5 class="text-sm font-medium text-gray-700">Current Parameters:</h5>
              <ul class="mt-1 text-sm space-y-1">
                <li v-for="(param, paramName) in capability.parameters" :key="paramName" class="flex justify-between">
                  <span>
                    <strong>{{ paramName }}</strong>
                    <template v-if="param.description">({{ param.description }})</template>
                  </span>
                  <button
                    type="button"
                    @click="removeParameter(index, paramName)"
                    class="text-red-600 hover:text-red-800 text-xs"
                  >
                    Remove
                  </button>
                </li>
              </ul>
            </div>
          </div>
        </div>
        
        <button
          type="button"
          @click="addCapability"
          class="mt-2 text-indigo-600 hover:text-indigo-800"
        >
          + Add another capability
        </button>
      </div>
      
      <!-- Authentication & Pricing -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h2 class="text-lg font-semibold text-gray-800 mb-4">Authentication</h2>
          <div>
            <label for="auth_type" class="form-label">Authentication Type</label>
            <select id="auth_type" v-model="formData.auth_type" class="form-input">
              <option value="none">None</option>
              <option value="api_key">API Key</option>
              <option value="oauth">OAuth</option>
            </select>
          </div>
          
          <div v-if="formData.auth_type === 'api_key'" class="mt-4">
            <label for="auth_header_name" class="form-label">Header Name</label>
            <input 
              id="auth_header_name" 
              v-model="authDetails.header_name" 
              type="text" 
              class="form-input"
              placeholder="X-API-Key"
            />
          </div>
        </div>
        
        <div>
          <h2 class="text-lg font-semibold text-gray-800 mb-4">Pricing</h2>
          <div>
            <label for="pricing_model" class="form-label">Pricing Model</label>
            <select id="pricing_model" v-model="formData.pricing_model" class="form-input">
              <option value="free">Free</option>
              <option value="pay_per_call">Pay Per Call</option>
              <option value="subscription">Subscription</option>
            </select>
          </div>
          
          <div v-if="formData.pricing_model === 'pay_per_call'" class="mt-4 grid grid-cols-2 gap-4">
            <div>
              <label for="cost_per_call" class="form-label">Cost Per Call</label>
              <input 
                id="cost_per_call" 
                v-model.number="pricingDetails.cost_per_call" 
                type="number" 
                step="0.01" 
                min="0" 
                class="form-input"
                placeholder="0.01"
              />
            </div>
            <div>
              <label for="currency" class="form-label">Currency</label>
              <select id="currency" v-model="pricingDetails.currency" class="form-input">
                <option value="USD">USD</option>
                <option value="EUR">EUR</option>
                <option value="GBP">GBP</option>
              </select>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Form submission -->
      <div class="border-t pt-6 flex justify-end">
        <button
          type="button"
          @click="$router.push('/agents')"
          class="btn btn-secondary mr-4"
        >
          Cancel
        </button>
        <button
          type="submit"
          :disabled="loading"
          :class="`btn btn-primary ${loading ? 'opacity-75 cursor-not-allowed' : ''}`"
        >
          {{ loading ? 'Registering...' : 'Register Agent' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'AgentRegister',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const formData = reactive({
      name: '',
      description: '',
      version: '1.0.0',
      author: '',
      contact_email: '',
      homepage_url: '',
      api_endpoint: '',
      capabilities: [
        {
          name: '',
          description: '',
          parameters: {}
        }
      ],
      auth_type: 'none',
      auth_details: null,
      pricing_model: 'free',
      pricing_details: null,
      tags: []
    })
    
    const formErrors = ref({})
    const loading = ref(false)
    const success = ref(false)
    const registeredAgentId = ref('')
    const tagInput = ref('')
    const parametersInput = ref('')
    
    // Auth details and pricing details
    const authDetails = reactive({
      header_name: 'X-API-Key'
    })
    
    const pricingDetails = reactive({
      cost_per_call: 0.01,
      currency: 'USD'
    })
    
    // Computed property for checking authentication
    const isAuthenticated = computed(() => store.getters.isAuthenticated)
    
    // Redirect to login if not authenticated
    onMounted(() => {
      if (!isAuthenticated.value) {
        router.push({ 
          path: '/login', 
          query: { redirect: '/register-agent' } 
        })
      }
    })
    
    // Form validation
    const validateForm = () => {
      const errors = {}
      
      if (!formData.name.trim()) errors.name = 'Name is required'
      if (!formData.description.trim()) errors.description = 'Description is required'
      if (!formData.version.trim()) errors.version = 'Version is required'
      if (!formData.author.trim()) errors.author = 'Author is required'
      if (!formData.api_endpoint.trim()) errors.api_endpoint = 'API endpoint is required'
      
      if (formData.contact_email && !/^\S+@\S+\.\S+$/.test(formData.contact_email)) {
        errors.contact_email = 'Invalid email format'
      }
      
      if (formData.homepage_url && !/^https?:\/\/\S+\.\S+/.test(formData.homepage_url)) {
        errors.homepage_url = 'Invalid URL format. Must start with http:// or https://'
      }
      
      // Validate capabilities
      if (formData.capabilities.length === 0) {
        errors.capabilities = 'At least one capability is required'
      } else {
        formData.capabilities.forEach((cap, index) => {
          if (!cap.name.trim()) {
            errors[`capability_${index}_name`] = 'Capability name is required'
          }
          if (!cap.description.trim()) {
            errors[`capability_${index}_description`] = 'Capability description is required'
          }
        })
      }
      
      formErrors.value = errors
      return Object.keys(errors).length === 0
    }
    
    // Handle form submission
    const handleSubmit = async () => {
      if (!validateForm()) {
        return
      }
      
      try {
        loading.value = true
        
        // Process form data for submission
        const processedData = { ...formData }
        
        // Handle auth details
        if (processedData.auth_type === 'api_key') {
          processedData.auth_details = { ...authDetails }
        } else {
          processedData.auth_details = null
        }
        
        // Handle pricing details
        if (processedData.pricing_model === 'pay_per_call') {
          processedData.pricing_details = { ...pricingDetails }
        } else {
          processedData.pricing_details = null
        }
        
        // Submit the agent data
        const response = await store.dispatch('createAgent', processedData)
        
        // Handle success
        registeredAgentId.value = response.agent_id
        success.value = true
      } catch (error) {
        store.dispatch('setError', {
          message: 'Failed to register agent',
          details: error.message
        })
      } finally {
        loading.value = false
      }
    }
    
    // Reset form after successful submission
    const resetForm = () => {
      Object.assign(formData, {
        name: '',
        description: '',
        version: '1.0.0',
        author: '',
        contact_email: '',
        homepage_url: '',
        api_endpoint: '',
        capabilities: [
          {
            name: '',
            description: '',
            parameters: {}
          }
        ],
        auth_type: 'none',
        auth_details: null,
        pricing_model: 'free',
        pricing_details: null,
        tags: []
      })
      
      success.value = false
      registeredAgentId.value = ''
    }
    
    // Tag management
    const addTag = () => {
      if (tagInput.value.trim() && !formData.tags.includes(tagInput.value.trim())) {
        formData.tags.push(tagInput.value.trim())
        tagInput.value = ''
      }
    }
    
    const removeTag = (index) => {
      formData.tags.splice(index, 1)
    }
    
    // Capability management
    const addCapability = () => {
      formData.capabilities.push({
        name: '',
        description: '',
        parameters: {}
      })
    }
    
    const removeCapability = (index) => {
      formData.capabilities.splice(index, 1)
    }
    
    // Parameter management
    const parseParameters = (capabilityIndex) => {
      try {
        const params = JSON.parse(parametersInput.value)
        formData.capabilities[capabilityIndex].parameters = params
        parametersInput.value = ''
      } catch (error) {
        alert('Invalid JSON format. Please check your parameter syntax.')
      }
    }
    
    const removeParameter = (capabilityIndex, paramName) => {
      const params = { ...formData.capabilities[capabilityIndex].parameters }
      delete params[paramName]
      formData.capabilities[capabilityIndex].parameters = params
    }
    
    return {
      formData,
      formErrors,
      loading,
      success,
      registeredAgentId,
      tagInput,
      parametersInput,
      authDetails,
      pricingDetails,
      handleSubmit,
      resetForm,
      addTag,
      removeTag,
      addCapability,
      removeCapability,
      parseParameters,
      removeParameter
    }
  }
}
</script>
