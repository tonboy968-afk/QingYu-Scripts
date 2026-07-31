import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import ScriptTemplatesView from '../views/ScriptTemplatesView.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/dashboard', name: 'Dashboard', component: DashboardView },
  { path: '/scripts/templates', name: 'ScriptTemplates', component: ScriptTemplatesView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
