import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

// Import views
import Dashboard from '../views/Dashboard.vue'
import AgentList from '../views/AgentList.vue'
import AgentDetail from '../views/AgentDetail.vue'
import AgentRegister from '../views/AgentRegister.vue'
import ExecutionList from '../views/ExecutionList.vue'
import ExecutionDetail from '../views/ExecutionDetail.vue'
import Login from '../views/Login.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/agents',
    name: 'AgentList',
    component: AgentList
  },
  {
    path: '/agents/:agentId',
    name: 'AgentDetail',
    component: AgentDetail,
    props: true
  },
  {
    path: '/agents/:agentId/executions',
    name: 'ExecutionList',
    component: ExecutionList,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/agents/:agentId/executions/:executionId',
    name: 'ExecutionDetail',
    component: ExecutionDetail,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/register-agent',
    name: 'AgentRegister',
    component: AgentRegister,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Navigation guard for protected routes
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const isAuthenticated = store.getters.isAuthenticated

  if (requiresAuth && !isAuthenticated) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } else {
    next()
  }
})

export default router
