import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, Plane, Calendar, Users, TrendingUp, Shield, Clock, Award } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent } from '@/components/ui/card'
import { Label } from '@/components/ui/label'

export default function HomePage() {
  const navigate = useNavigate()
  const [searchParams, setSearchParams] = useState({
    from_airport: '',
    to_airport: '',
    departure_date: '',
    passengers: '1',
  })

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    const params = new URLSearchParams(searchParams as any)
    navigate(`/flights?${params.toString()}`)
  }

  const popularDestinations = [
    { city: 'Дубай', code: 'DXB', image: '🏝️', from: '150,000' },
    { city: 'Стамбул', code: 'IST', image: '🕌', from: '120,000' },
    { city: 'Москва', code: 'SVO', image: '🏛️', from: '80,000' },
    { city: 'Ташкент', code: 'TAS', image: '🌆', from: '45,000' },
  ]

  const features = [
    {
      icon: TrendingUp,
      title: 'Лучшие цены',
      description: 'Сравниваем предложения от всех авиакомпаний',
    },
    {
      icon: Shield,
      title: 'Безопасные платежи',
      description: 'SSL шифрование и защита данных',
    },
    {
      icon: Clock,
      title: '24/7 Поддержка',
      description: 'Круглосуточная помощь на русском языке',
    },
    {
      icon: Award,
      title: 'Программа лояльности',
      description: 'Накапливайте баллы и получайте скидки',
    },
  ]

  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-blue-600 via-blue-700 to-blue-900 text-white py-20 md:py-32">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZGVmcz48cGF0dGVybiBpZD0iZ3JpZCIgd2lkdGg9IjQwIiBoZWlnaHQ9IjQwIiBwYXR0ZXJuVW5pdHM9InVzZXJTcGFjZU9uVXNlIj48cGF0aCBkPSJNIDQwIDAgTCAwIDAgMCA0MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJyZ2JhKDI1NSwyNTUsMjU1LDAuMSkiIHN0cm9rZS13aWR0aD0iMSIvPjwvcGF0dGVybj48L2RlZnM+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0idXJsKCNncmlkKSIvPjwvc3ZnPg==')] opacity-20" />
        
        <div className="container relative z-10">
          <div className="text-center max-w-3xl mx-auto mb-12">
            <h1 className="text-4xl md:text-6xl font-bold mb-6 animate-fade-in">
              Найдите свой идеальный рейс
            </h1>
            <p className="text-xl md:text-2xl text-blue-100">
              Сравните цены, выберите лучший вариант и забронируйте билеты онлайн
            </p>
          </div>

          {/* Search Form */}
          <Card className="max-w-4xl mx-auto shadow-2xl">
            <CardContent className="p-6">
              <form onSubmit={handleSearch} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {/* From */}
                  <div className="space-y-2">
                    <Label htmlFor="from" className="flex items-center gap-2">
                      <Plane className="h-4 w-4" />
                      Откуда
                    </Label>
                    <Input
                      id="from"
                      placeholder="ALA (Алматы)"
                      value={searchParams.from_airport}
                      onChange={(e) =>
                        setSearchParams({ ...searchParams, from_airport: e.target.value })
                      }
                      required
                    />
                  </div>

                  {/* To */}
                  <div className="space-y-2">
                    <Label htmlFor="to" className="flex items-center gap-2">
                      <Plane className="h-4 w-4 rotate-90" />
                      Куда
                    </Label>
                    <Input
                      id="to"
                      placeholder="DXB (Дубай)"
                      value={searchParams.to_airport}
                      onChange={(e) =>
                        setSearchParams({ ...searchParams, to_airport: e.target.value })
                      }
                      required
                    />
                  </div>

                  {/* Date */}
                  <div className="space-y-2">
                    <Label htmlFor="date" className="flex items-center gap-2">
                      <Calendar className="h-4 w-4" />
                      Дата вылета
                    </Label>
                    <Input
                      id="date"
                      type="date"
                      value={searchParams.departure_date}
                      onChange={(e) =>
                        setSearchParams({ ...searchParams, departure_date: e.target.value })
                      }
                      min={new Date().toISOString().split('T')[0]}
                      required
                    />
                  </div>

                  {/* Passengers */}
                  <div className="space-y-2">
                    <Label htmlFor="passengers" className="flex items-center gap-2">
                      <Users className="h-4 w-4" />
                      Пассажиры
                    </Label>
                    <Input
                      id="passengers"
                      type="number"
                      min="1"
                      max="9"
                      value={searchParams.passengers}
                      onChange={(e) =>
                        setSearchParams({ ...searchParams, passengers: e.target.value })
                      }
                      required
                    />
                  </div>
                </div>

                <Button type="submit" size="lg" className="w-full md:w-auto gap-2">
                  <Search className="h-5 w-5" />
                  Найти рейсы
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Popular Destinations */}
      <section className="py-16 md:py-24 bg-muted/30">
        <div className="container">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Популярные направления</h2>
            <p className="text-muted-foreground text-lg">
              Самые востребованные маршруты из Алматы
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {popularDestinations.map((dest) => (
              <Card
                key={dest.code}
                className="cursor-pointer hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1"
                onClick={() => {
                  setSearchParams({
                    ...searchParams,
                    from_airport: 'ALA',
                    to_airport: dest.code,
                  })
                }}
              >
                <CardContent className="p-6">
                  <div className="text-6xl mb-4 text-center">{dest.image}</div>
                  <h3 className="text-xl font-semibold mb-2 text-center">{dest.city}</h3>
                  <p className="text-sm text-muted-foreground text-center mb-4">{dest.code}</p>
                  <div className="text-center">
                    <span className="text-sm text-muted-foreground">от </span>
                    <span className="text-2xl font-bold text-primary">{dest.from}</span>
                    <span className="text-sm text-muted-foreground"> ₸</span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 md:py-24">
        <div className="container">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Почему выбирают нас</h2>
            <p className="text-muted-foreground text-lg">
              Преимущества бронирования через FlightHub
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon
              return (
                <div key={index} className="text-center">
                  <div className="inline-flex items-center justify-center w-16 h-16 bg-primary/10 rounded-full mb-4">
                    <Icon className="h-8 w-8 text-primary" />
                  </div>
                  <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                  <p className="text-muted-foreground">{feature.description}</p>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 md:py-24 bg-gradient-to-r from-blue-600 to-blue-800 text-white">
        <div className="container text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Готовы к путешествию?
          </h2>
          <p className="text-xl mb-8 text-blue-100 max-w-2xl mx-auto">
            Зарегистрируйтесь сейчас и получите бонусные баллы на первое бронирование
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              size="lg"
              variant="secondary"
              onClick={() => navigate('/register')}
              className="text-lg px-8"
            >
              Создать аккаунт
            </Button>
            <Button
              size="lg"
              variant="outline"
              onClick={() => navigate('/flights')}
              className="text-lg px-8 bg-white/10 text-white border-white hover:bg-white hover:text-blue-600"
            >
              Найти рейс
            </Button>
          </div>
        </div>
      </section>
    </div>
  )
}
