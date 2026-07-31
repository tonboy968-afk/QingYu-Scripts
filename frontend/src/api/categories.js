import { api } from './index.js'

export function getCategories() {
  return api.get('/v1/categories')
}
export function createCategory(data) {
  return api.post('/v1/categories', data)
}
export function updateCategory(id, data) {
  return api.put(`/v1/categories/${id}`, data)
}
export function deleteCategory(id) {
  return api.delete(`/v1/categories/${id}`)
}
