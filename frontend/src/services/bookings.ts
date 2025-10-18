import api from './api'
import { Booking, BookingRequest } from '@/types'

export const bookingService = {
  // Create new booking
  createBooking: async (data: BookingRequest): Promise<Booking> => {
    const response = await api.post('/api/v1/bookings/', data)
    return response.data
  },

  // Get all user bookings
  getMyBookings: async (): Promise<Booking[]> => {
    const response = await api.get('/api/v1/bookings/')
    return response.data
  },

  // Get booking by ID
  getBookingById: async (id: string): Promise<Booking> => {
    const response = await api.get(`/api/v1/bookings/${id}/`)
    return response.data
  },

  // Cancel booking
  cancelBooking: async (id: string): Promise<Booking> => {
    const response = await api.post(`/api/v1/bookings/${id}/cancel/`)
    return response.data
  },

  // Download ticket PDF
  downloadTicket: async (id: string): Promise<Blob> => {
    const response = await api.get(`/api/v1/bookings/${id}/ticket/`, {
      responseType: 'blob',
    })
    return response.data
  },
}
