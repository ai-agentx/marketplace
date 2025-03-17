<template>
  <div>
    <div class="bg-white shadow rounded-lg p-6 mb-6">
      <div class="flex justify-between items-center mb-4">
        <h1 class="text-2xl font-bold text-gray-800">Browse Agents</h1>
        <router-link
          to="/register-agent"
          class="btn btn-primary"
        >
          Register New Agent
        </router-link>
      </div>
      
      <!-- Search and filters -->
      <form @submit.prevent="handleSearch" class="mb-6">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4 mb-4">
          <div>
            <label for="query" class="form-label">
              Search
            </label>
            <input
              type="text"
              id="query"
              v-model="searchParams.query"
              placeholder="Search agents..."
              class="form-input"
            />
          </div>
          <div>
            <label for="capabilities" class="form-label">
              Capabilities
            </label>
            <input
              type="text"
              id="capabilities"
              v-model="searchParams.capabilities"
              placeholder="e.g., summarize_text"
              class="form-input"
            />
          </div>
          <div>
            <label for="tags" class="form-label">
              Tags
            </label>
            <input
              type="text"
              id="tags"
              v-model="searchParams.tags"
              placeholder="e.g., nlp,text"
              class="form-input"
            />
          </div>
          <div>
            <label for="author" class="form-label">
              Author
            </label>
            <input
              type="text"
              id="author"
              v-model="searchParams.author"
              placeholder="e.g., ExampleCorp"
              class="form-input"
            />
          </div>
          <div>
            <label for="pricing_model" class="form-label">
              Pricing Model
            </label>
            <select
              id="pricing_model"
              v-model="searchParams.pricing_model"
              class="form-input"
            >
              <option value="">All</option>
              <option value="free">Free</option>
              <option value="pay_per_call">Pay Per Call</option>
              <option value="subscription">Subscription</option>
            </select>
          </div>
        </div>
        <div class="flex justify-between items-center">
          <button
            type="button"
            @click="clearFilters"
            class="text-gray-500 hover:text-gray-700"
          >
            Clear filters
          </button>
          <button
            type="submit"
            class="btn btn-primary"
          >
            Search
          </button>
        </div>
      </form>
      
      <!-- Results -->
      <div v-if="loading" class="text-center py-10">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-indigo-500 border-t-transparent"></div>
        <p class="mt-2 text-gray-600">Loading agents...</p>
      </div>
      
      <div v-else-if="agents.length === 0" class="text-center py-10">
        <p class="text-gray-500">No agents found matching your criteria.</p>
        <button
          @click="clearFilters"
          class="mt-2 text-indigo-600 hover:text-indigo-800"
        >
          Clear filters and try again
        </button>
      </div>
      
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="agent in agents" 
          :key="agent.id" 
          class="bg-white border rounded-lg shadow-sm hover:shadow-md transition-shadow"
        >
          <div class="p-5 border-b">
            <h2 class="text-xl font-semibold text-gray-800">{{ agent.name }}</h2>
            <p class="text-gray-500 text-sm mt-1">By: {{ agent.author }}</p>
            <div class="flex flex-wrap gap-1 mt-2">
              <span 
                v-for="tag in agent.tags" 
                :key="tag" 
                class="bg-indigo-50 text-indigo-700 text-xs px-2 py-1 rounded-full"
              >
                {{ tag }}
              </span>
            </div>
          </div>
          <div class="p-5">
            <p class="text-gray-600 mb-4">{{ agent.description }}</p>
            <div class="flex flex-wrap gap-y-2 gap-x-4 text-sm mb-4">
              <div>
                <span class="text-gray-500">Version:</span> {{ agent.version }}
              </div>
              <div>
                <span class="text-gray-500">Pricing:</span> {{ agent.pricing_model || 'Free' }}
              </div>
              <div>
                <span class="text-gray-500">Auth:</span> {{ agent.auth_type }}
              </div>
            </div>
            <div class="border-t pt-4 flex justify-between">
              <router-link 
                :to="`/agents/${agent.id}`"
                class="text-indigo-600 hover:text-indigo-800 font-medium"
              >
                View Details
              </router-link>
              <router-link 
                :to="`/agents/${agent.id}?execute=true`"
                class="bg-indigo-600 text-white px-3 py-1 rounded hover:bg-indigo-500 text-sm"
              >
                Execute Agent
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { mapState, mapActions } from 'vuex'

export default {
  name: 'AgentList',
  setup() {
    const searchParams = ref({
      query: '',
      capabilities: '',
      tags: '',
      author: '',
      pricing_model: '',
    })

    return {
      searchParams
    }
  },
  computed: {
    ...mapState(['agents', 'loading'])
  },
  methods: {
    ...mapActions(['fetchAgents']),
    
    handleSearch() {
      // Filter out empty search params
      const filteredParams = Object.entries(this.searchParams)
        .filter(([_, value]) => value !== '')
        .reduce((obj, [key, value]) => ({ ...obj, [key]: value }), {})
      
      this.fetchAgents(filteredParams)
    },
    
    clearFilters() {
      this.searchParams = {
        query: '',
        capabilities: '',
        tags: '',
        author: '',
        pricing_model: '',
      }
      this.fetchAgents()
    }
  },
  mounted() {
    this.fetchAgents()
  }
}
</script>
