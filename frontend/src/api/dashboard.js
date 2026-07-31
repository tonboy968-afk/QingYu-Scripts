import { api } from './index.js'

export function getDashboardStats() {
  return api.get('/v1/dashboard/stats')
}
