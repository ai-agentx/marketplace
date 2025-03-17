import { createStore } from 'vuex'
import axios from 'axios'

// Configure axios
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add api key from local storage if available
const apiKey = localStorage.getItem('apiKey')
if (apiKey) {
  api.defaults.headers.common['X-API-Key'] = apiKey
}

export default createStore({
  state: {
    user: null,
    apiKey: apiKey || '',
    agents: [],
    agentDetail: null,
    executions: [],
    executionDetail: null,
    globalError: null,
    loading: false
  },
  getters: {
    isAuthenticated: state => !!state.user,
    isAdmin: state => state.user?.role === 'admin',
    getAgentById: state => id => {
      return state.agents.find(agent => agent.id === id) || null
    }
  },
  mutations: {
    SET_API_KEY(state, apiKey) {
      state.apiKey = apiKey
      if (apiKey) {
        localStorage.setItem('apiKey', apiKey)
        api.defaults.headers.common['X-API-Key'] = apiKey
      } else {
        localStorage.removeItem('apiKey')
        delete api.defaults.headers.common['X-API-Key']
      }
    },
    SET_USER(state, user) {
      state.user = user
    },
    SET_AGENTS(state, agents) {
      state.agents = agents
    },
    SET_AGENT_DETAIL(state, agent) {
      state.agentDetail = agent
    },
    SET_EXECUTIONS(state, executions) {
      state.executions = executions
    },
    SET_EXECUTION_DETAIL(state, execution) {
      state.executionDetail = execution
    },
    SET_ERROR(state, error) {
      state.globalError = error
    },
    CLEAR_ERROR(state) {
      state.globalError = null
    },
    SET_LOADING(state, status) {
      state.loading = status
    }
  },
  actions: {
    // Auth actions
    async login({ commit }, apiKey) {
      commit('SET_API_KEY', apiKey)
      
      try {
        // For this example, we'll simulate user validation
        // In a real app, you would validate the API key with the backend
        const response = await api.get('/health')
        
        if (response.status === 200) {
          // Simulate user info based on API key
          const user = {
            id: 'user_id',
            role: apiKey === 'test_key' ? 'admin' : 'user'
          }
          commit('SET_USER', user)
          return user
        }
      } catch (error) {
        commit('SET_API_KEY', '')
        commit('SET_USER', null)
        throw new Error('Invalid API key')
      }
    },
    
    logout({ commit }) {
      commit('SET_API_KEY', '')
      commit('SET_USER', null)
    },
    
    // Agent actions
    async fetchAgents({ commit }, searchParams = {}) {
      commit('SET_LOADING', true)
      try {
        const response = await api.get('/agents', { params: searchParams })
        commit('SET_AGENTS', response.data.agents || [])
      } catch (error) {
        commit('SET_ERROR', {
          message: 'Failed to fetch agents',
          details: error.message
        })
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchAgentDetail({ commit }, agentId) {
      commit('SET_LOADING', true)
      try {
        const response = await api.get(`/agents/${agentId}`)
        commit('SET_AGENT_DETAIL', response.data)
      } catch (error) {
        commit('SET_ERROR', {
          message: 'Failed to fetch agent details',
          details: error.message
        })
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async createAgent({ commit }, agentData) {
      commit('SET_LOADING', true)
      try {
        const response = await api.post('/agents', agentData)
        return response.data
      } catch (error) {
        commit('SET_ERROR', {
          message: 'Failed to create agent',
          details: error.message
        })
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async updateAgent({ commit }, { agentId, agentData }) {
      commit('SET_LOADING', true)
      try {
        const response = await api.put(`/agents/${agentId}`, agentData)
        return response.data
      } catch (error) {
        commit('SET_ERROR', {
          message: 'Failed to update agent',
          details: error.message
        })
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async deleteAgent({ commit }, agentId) {
      commit('SET_LOADING', true)
      try {
        const response = await api.delete(`/agents/${agentId}`)
        return response.data
      } catch (error) {
        commit('SET_ERROR', {
          message: 'Failed to delete agent',
          details: error.message
        })
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // Execution actions
    async executeAgent({ commit }, { agentId, executionData }) {
      commit('SET_LOADING', true)
      try {
        const response = await api.post(`/agents/${agentId}/execute`, executionData)
        return response.data
      } catch (error) {
        commit('SET_ERROR', {
          message: 'Failed to execute agent',
          details: error.message
        })
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchExecutions({ commit }, agentId) {
      commit('SET_LOADING', true)
      try {
        const response = await api.get(`/agents/${agentId}/executions`)
        commit('SET_EXECUTIONS', response.data.executions || [])
      } catch (error) {
        commit('SET_ERROR', {
          message: 'Failed to fetch executions',
          details: error.message
        })
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchExecutionDetail({ commit }, { agentId, executionId }) {
      commit('SET_LOADING', true)
      try {
        const response = await api.get(`/agents/${agentId}/executions/${executionId}`)
        commit('SET_EXECUTION_DETAIL', response.data)
      } catch (error) {
        commit('SET_ERROR', {
          message: 'Failed to fetch execution details',
          details: error.message
        })
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // Error handling
    setError({ commit }, error) {
      commit('SET_ERROR', error)
    },
    
    clearError({ commit }) {
      commit('CLEAR_ERROR')
    }
  }
})
