import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { User, AuthResponse } from '@/types'
import { authService } from '@/services/auth'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (data: { email: string; password: string; first_name: string; last_name: string; phone?: string }) => Promise<void>
  logout: () => void
  fetchProfile: () => Promise<void>
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (email: string, password: string) => {
        set({ isLoading: true })
        try {
          const response: AuthResponse = await authService.login({ email, password })
          
          localStorage.setItem('access_token', response.access_token)
          localStorage.setItem('refresh_token', response.refresh_token)
          
          set({
            user: response.user,
            isAuthenticated: true,
            isLoading: false,
          })
        } catch (error) {
          set({ isLoading: false })
          throw error
        }
      },

      register: async (data) => {
        set({ isLoading: true })
        try {
          const response: AuthResponse = await authService.register(data)
          
          localStorage.setItem('access_token', response.access_token)
          localStorage.setItem('refresh_token', response.refresh_token)
          
          set({
            user: response.user,
            isAuthenticated: true,
            isLoading: false,
          })
        } catch (error) {
          set({ isLoading: false })
          throw error
        }
      },

      logout: () => {
        authService.logout()
        set({
          user: null,
          isAuthenticated: false,
        })
      },

      fetchProfile: async () => {
        try {
          const user = await authService.getProfile()
          set({ user, isAuthenticated: true })
        } catch (error) {
          set({ user: null, isAuthenticated: false })
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)
