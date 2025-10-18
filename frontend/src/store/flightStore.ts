import { create } from 'zustand'
import { Flight, FlightSearchParams } from '@/types'

interface FlightState {
  searchParams: FlightSearchParams | null
  selectedFlight: Flight | null
  setSearchParams: (params: FlightSearchParams) => void
  setSelectedFlight: (flight: Flight | null) => void
  clearSearch: () => void
}

export const useFlightStore = create<FlightState>((set) => ({
  searchParams: null,
  selectedFlight: null,
  
  setSearchParams: (params) => set({ searchParams: params }),
  
  setSelectedFlight: (flight) => set({ selectedFlight: flight }),
  
  clearSearch: () => set({ searchParams: null, selectedFlight: null }),
}))
