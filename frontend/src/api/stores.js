import { api } from './index.js'

export function getStores() {
  return api.get('/v1/stores')
}
export function createStore(data) {
  return api.post('/v1/stores', data)
}
export function updateStore(id, data) {
  return api.put(`/v1/stores/${id}`, data)
}
export function deleteStore(id) {
  return api.delete(`/v1/stores/${id}`)
}
