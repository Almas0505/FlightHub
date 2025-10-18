import api from './api'
import { Flight, FlightSearchParams, FlightSearchResponse } from '@/types'

export const flightService = {
  // Search flights
  searchFlights: async (params: FlightSearchParams): Promise<FlightSearchResponse> => {
    const response = await api.get('/api/v1/flights/search', { params })
    return response.data
  },

  // Get flight details by ID
  getFlightById: async (id: string): Promise<Flight> => {
    const response = await api.get(`/api/v1/flights/${id}`)
    return response.data
  },

  // Search airports
  searchAirports: async (query: string) => {
    const response = await api.get('/api/v1/airports/search', {
      params: { query },
    })
    return response.data
  },

  // Get popular routes
  getPopularRoutes: async () => {
    const response = await api.get('/api/v1/flights/popular')
    return response.data
  },
}
