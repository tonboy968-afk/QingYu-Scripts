import { api } from './index.js'

export function getScripts(params) {
  return api.get('/v1/scripts', { params })
}
export function createScript(data) {
  return api.post('/v1/scripts', data)
}
export function updateScript(id, data) {
  return api.put(`/v1/scripts/${id}`, data)
}
export function deleteScript(id) {
  return api.delete(`/v1/scripts/${id}`)
}
export function getScript(id) {
  return api.get(`/v1/scripts/${id}`)
}
