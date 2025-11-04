import axios from 'axios';

// Create an axios instance with base configuration
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Item API methods
export const itemApi = {
  getAll(page = 1) {
    return apiClient.get(`/items/?page=${page}`);
  },
  getOne(id) {
    return apiClient.get(`/items/${id}/`);
  },
  create(data) {
    return apiClient.post('/items/', data);
  },
  update(id, data) {
    return apiClient.patch(`/items/${id}/`, data);
  },
  delete(id) {
    return apiClient.delete(`/items/${id}/`);
  },
};

// Customer API methods
export const customerApi = {
  getAll(page = 1) {
    return apiClient.get(`/customers/?page=${page}`);
  },
  getOne(id) {
    return apiClient.get(`/customers/${id}/`);
  },
  create(data) {
    return apiClient.post('/customers/', data);
  },
  update(id, data) {
    return apiClient.patch(`/customers/${id}/`, data);
  },
  delete(id) {
    return apiClient.delete(`/customers/${id}/`);
  },
};

export default apiClient;
