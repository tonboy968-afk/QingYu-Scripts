import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import ScriptsView from '../views/ScriptsView.vue'
import CategoriesView from '../views/CategoriesView.vue'
import StoresView from '../views/StoresView.vue'

const routes = [
  { path: '/dashboard', name: 'Dashboard', component: DashboardView },
  { path: '/scripts', name: 'Scripts', component: ScriptsView },
  { path: '/categories', name: 'Categories', component: CategoriesView },
  { path: '/stores', name: 'Stores', component: StoresView },
  { path: '/', redirect: '/dashboard' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
