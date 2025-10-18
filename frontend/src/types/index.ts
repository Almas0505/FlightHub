// User Types
export interface User {
  id: string
  email: string
  first_name: string
  last_name: string
  phone?: string
  created_at: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  password: string
  first_name: string
  last_name: string
  phone?: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
  user: User
}

// Flight Types
export interface Airport {
  code: string
  name: string
  city: string
  country: string
}

export interface FlightSegment {
  departure_airport: string
  arrival_airport: string
  departure_time: string
  arrival_time: string
  flight_number: string
  airline: string
  duration: number
  aircraft_type?: string
}

export interface Flight {
  id: string
  airline: string
  flight_number: string
  departure_airport: string
  arrival_airport: string
  departure_time: string
  arrival_time: string
  duration: number
  price: number
  currency: string
  available_seats: number
  cabin_class: 'economy' | 'business' | 'first'
  segments: FlightSegment[]
  baggage_allowance?: string
  meal_service?: boolean
}

export interface FlightSearchParams {
  from_airport: string
  to_airport: string
  departure_date: string
  return_date?: string
  passengers: number
  cabin_class?: 'economy' | 'business' | 'first'
}

export interface FlightSearchResponse {
  results: Flight[]
  total: number
  from_cache: boolean
  search_id: string
}

// Booking Types
export interface Passenger {
  title: 'MR' | 'MS' | 'MRS'
  first_name: string
  last_name: string
  date_of_birth: string
  passport_number: string
  nationality: string
  email?: string
}

export interface BookingRequest {
  flight_id: string
  passengers: Passenger[]
  contact_email: string
  contact_phone: string
}

export interface Booking {
  id: string
  pnr: string
  status: 'PENDING' | 'CONFIRMED' | 'CANCELLED' | 'EXPIRED'
  flight_details: Flight
  passengers: Passenger[]
  total_amount: number
  currency: string
  contact_email: string
  contact_phone: string
  created_at: string
  expires_at?: string
  confirmed_at?: string
}

// Payment Types
export interface PaymentRequest {
  booking_id: string
  payment_method: 'card' | 'bank_transfer' | 'wallet'
  card_token?: string
  save_card?: boolean
}

export interface Payment {
  id: string
  booking_id: string
  amount: number
  currency: string
  status: 'pending' | 'completed' | 'failed' | 'refunded'
  payment_method: string
  created_at: string
}

// Loyalty Program
export interface LoyaltyInfo {
  level: 'BRONZE' | 'SILVER' | 'GOLD' | 'PLATINUM'
  points: number
  next_level_points: number
  benefits: string[]
}

// API Response
export interface ApiError {
  error: string
  message: string
  details?: Record<string, string[]>
}
