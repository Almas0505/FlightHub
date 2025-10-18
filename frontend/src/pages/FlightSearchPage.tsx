import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { Plane, Briefcase, ArrowRight, Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import api from '@/lib/api'

interface FlightSegment {
  id: string
  airline: {
    code: string
    name: string
  }
  flight_number: string
  departure: {
    airport_code: string
    city: string
    datetime: string
  }
  arrival: {
    airport_code: string
    city: string
    datetime: string
  }
  duration_minutes: number
}

interface Flight {
  id: string
  segments: FlightSegment[]
  price: {
    total: number
    currency: string
  }
  cabin_class: string
  stops: number
}

export default function FlightSearchPage() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const [flights, setFlights] = useState<Flight[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchFlights = async () => {
      try {
        setLoading(true)
        setError(null)
        
        const params = {
          from_airport: searchParams.get('from_airport') || 'ALA',
          to_airport: searchParams.get('to_airport') || 'DXB',
          departure_date: searchParams.get('departure_date') || new Date().toISOString().split('T')[0],
          passengers: searchParams.get('passengers') || '1',
          cabin_class: searchParams.get('cabin_class') || 'economy',
        }

        const response = await api.get('/flights/search', { params })
        setFlights(response.data.flights || [])
      } catch (err) {
        const error = err as { response?: { data?: { detail?: string } } }
        setError(error.response?.data?.detail || 'Ошибка при поиске рейсов')
      } finally {
        setLoading(false)
      }
    }

    fetchFlights()
  }, [searchParams])

  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60)
    const mins = minutes % 60
    return `${hours}ч ${mins}м`
  }

  const formatTime = (datetime: string) => {
    return new Date(datetime).toLocaleTimeString('ru-RU', { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('ru-RU').format(price)
  }

  const getAirlineLogo = (code: string) => {
    const logos: Record<string, string> = {
      'KC': '🇰🇿',
      'EK': '🇦🇪',
      'TK': '🇹🇷',
      'QR': '🇶🇦',
      'SU': '🇷🇺',
      'FZ': '🇦🇪',
    }
    return logos[code] || '✈️'
  }

  if (loading) {
    return (
      <div className="container py-12">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <Loader2 className="h-12 w-12 animate-spin text-primary mx-auto mb-4" />
            <p className="text-muted-foreground">Ищем лучшие рейсы...</p>
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container py-12">
        <Card className="border-destructive">
          <CardContent className="pt-6">
            <p className="text-destructive text-center">{error}</p>
            <div className="text-center mt-4">
              <Button onClick={() => navigate('/')}>
                Вернуться к поиску
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="container py-8">
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-2">Результаты поиска</h1>
        <p className="text-muted-foreground">
          Найдено рейсов: <span className="font-semibold">{flights.length}</span>
        </p>
      </div>

      {flights.length === 0 ? (
        <Card>
          <CardContent className="py-12 text-center">
            <Plane className="h-16 w-16 mx-auto mb-4 text-muted-foreground" />
            <h3 className="text-xl font-semibold mb-2">Рейсы не найдены</h3>
            <p className="text-muted-foreground mb-4">
              Попробуйте изменить параметры поиска
            </p>
            <Button onClick={() => navigate('/')}>
              Новый поиск
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {flights.map((flight) => {
            const segment = flight.segments[0]
            return (
              <Card 
                key={flight.id} 
                className="hover:shadow-lg transition-shadow cursor-pointer"
                onClick={() => navigate(`/flights/${flight.id}`)}
              >
                <CardContent className="p-6">
                  <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
                    {/* Airline Logo & Name */}
                    <div className="md:col-span-2">
                      <div className="text-center">
                        <div className="text-4xl mb-2">
                          {getAirlineLogo(segment.airline.code)}
                        </div>
                        <p className="text-sm font-medium">{segment.airline.name}</p>
                        <p className="text-xs text-muted-foreground">
                          {segment.flight_number}
                        </p>
                      </div>
                    </div>

                    {/* Flight Details */}
                    <div className="md:col-span-7">
                      <div className="flex items-center justify-between">
                        {/* Departure */}
                        <div className="flex-1">
                          <p className="text-2xl font-bold">
                            {formatTime(segment.departure.datetime)}
                          </p>
                          <p className="text-sm font-medium">
                            {segment.departure.airport_code}
                          </p>
                          <p className="text-xs text-muted-foreground">
                            {segment.departure.city}
                          </p>
                        </div>

                        {/* Duration & Stops */}
                        <div className="flex-1 px-4">
                          <div className="flex items-center justify-center gap-2 mb-1">
                            <div className="h-px flex-1 bg-muted-foreground/30" />
                            <Plane className="h-4 w-4 text-muted-foreground" />
                            <div className="h-px flex-1 bg-muted-foreground/30" />
                          </div>
                          <p className="text-xs text-center text-muted-foreground">
                            {formatDuration(segment.duration_minutes)}
                          </p>
                          {flight.stops > 0 && (
                            <p className="text-xs text-center text-orange-600 font-medium">
                              {flight.stops} пересадка
                            </p>
                          )}
                          {flight.stops === 0 && (
                            <p className="text-xs text-center text-green-600 font-medium">
                              Прямой
                            </p>
                          )}
                        </div>

                        {/* Arrival */}
                        <div className="flex-1 text-right">
                          <p className="text-2xl font-bold">
                            {formatTime(segment.arrival.datetime)}
                          </p>
                          <p className="text-sm font-medium">
                            {segment.arrival.airport_code}
                          </p>
                          <p className="text-xs text-muted-foreground">
                            {segment.arrival.city}
                          </p>
                        </div>
                      </div>

                      {/* Additional Info */}
                      <div className="flex gap-2 mt-4">
                        <Badge variant="outline" className="text-xs">
                          <Briefcase className="h-3 w-3 mr-1" />
                          1 место багажа
                        </Badge>
                        <Badge variant="outline" className="text-xs capitalize">
                          {flight.cabin_class}
                        </Badge>
                      </div>
                    </div>

                    {/* Price & Book Button */}
                    <div className="md:col-span-3 text-center md:text-right">
                      <div className="mb-4">
                        <p className="text-sm text-muted-foreground mb-1">
                          от
                        </p>
                        <p className="text-3xl font-bold text-primary">
                          {formatPrice(flight.price.total)}
                        </p>
                        <p className="text-sm text-muted-foreground">
                          {flight.price.currency}
                        </p>
                      </div>
                      <Button 
                        className="w-full gap-2"
                        onClick={(e) => {
                          e.stopPropagation()
                          navigate(`/booking/${flight.id}`)
                        }}
                      >
                        Выбрать
                        <ArrowRight className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>
      )}
    </div>
  )
}
