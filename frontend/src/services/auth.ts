import api from './api'
import { LoginRequest, RegisterRequest, AuthResponse, User, LoyaltyInfo } from '@/types'

export const authService = {
  // Register new user
  register: async (data: RegisterRequest): Promise<AuthResponse> => {
    const response = await api.post('/api/v1/users/register/', data)
    return response.data
  },

  // Login
  login: async (data: LoginRequest): Promise<AuthResponse> => {
    const response = await api.post('/api/v1/users/login/', data)
    return response.data
  },

  // Logout
  logout: async (): Promise<void> => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  },

  // Get current user profile
  getProfile: async (): Promise<User> => {
    const response = await api.get('/api/v1/users/profile/')
    return response.data
  },

  // Update profile
  updateProfile: async (data: Partial<User>): Promise<User> => {
    const response = await api.patch('/api/v1/users/profile/', data)
    return response.data
  },

  // Get loyalty info
  getLoyaltyInfo: async (): Promise<LoyaltyInfo> => {
    const response = await api.get('/api/v1/users/loyalty_info/')
    return response.data
  },
}
