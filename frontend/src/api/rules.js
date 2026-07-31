import { api } from './index.js'

export function getRules(params) {
  return api.get('/v1/rules', { params })
}
export function createRule(data) {
  return api.post('/v1/rules', data)
}
export function updateRule(id, data) {
  return api.put(`/v1/rules/${id}`, data)
}
export function deleteRule(id) {
  return api.delete(`/v1/rules/${id}`)
}
