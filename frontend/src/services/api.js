import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://api.buildforu.pw'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  register: (data) => api.post('/api/auth/register', data),
  login: (data) => api.post('/api/auth/login', data),
  getProfile: () => api.get('/api/auth/profile'),
  regenerateKey: () => api.post('/api/auth/regenerate-key'),
}

export const dashboardAPI = {
  getStats: () => api.get('/api/dashboard/stats'),
  getPayments: (params) => api.get('/api/dashboard/payments', { params }),
  getLedgers: (params) => api.get('/api/dashboard/ledgers', { params }),
  getPendingVerifications: () => api.get('/api/dashboard/verifications'),
  verifyPayment: (paymentId, data) => api.post(`/api/dashboard/verifications/${paymentId}/verify`, data),
}

export default api

