import api from './api'
import { Payment, PaymentRequest } from '@/types'

export const paymentService = {
  // Create payment
  createPayment: async (data: PaymentRequest): Promise<Payment> => {
    const response = await api.post('/api/v1/payments/', data)
    return response.data
  },

  // Get payment by ID
  getPaymentById: async (id: string): Promise<Payment> => {
    const response = await api.get(`/api/v1/payments/${id}/`)
    return response.data
  },

  // Cancel payment (refund)
  cancelPayment: async (id: string): Promise<Payment> => {
    const response = await api.post(`/api/v1/payments/${id}/cancel/`)
    return response.data
  },
}
