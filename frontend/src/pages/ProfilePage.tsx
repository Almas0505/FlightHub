import { useState, useEffect } from 'react'
import { User, Mail, Phone, Award, Calendar, Plane, Edit, Save, X } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import api from '@/lib/api'

interface UserProfile {
  id: string
  email: string
  first_name: string
  last_name: string
  phone: string
  tier: string
  loyalty_points: number
  preferred_language: string
  preferred_currency: string
  email_notifications: boolean
  sms_notifications: boolean
  created_at: string
}

const getTierColor = (tier: string) => {
  const colors: Record<string, string> = {
    BRONZE: 'bg-orange-600',
    SILVER: 'bg-gray-400',
    GOLD: 'bg-yellow-500',
    PLATINUM: 'bg-purple-600',
  }
  return colors[tier] || 'bg-gray-400'
}

const getTierBenefits = (tier: string) => {
  const benefits: Record<string, string[]> = {
    BRONZE: ['5% скидка', 'Базовая поддержка'],
    SILVER: ['10% скидка', 'Приоритетная регистрация', 'Поддержка 24/7'],
    GOLD: ['15% скидка', 'Lounge доступ', 'Бесплатный багаж +10кг', 'VIP поддержка'],
    PLATINUM: ['25% скидка', 'Premium Lounge', 'Бизнес класс upgrade', 'Персональный менеджер'],
  }
  return benefits[tier] || []
}

export default function ProfilePage() {
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(false)
  const [editForm, setEditForm] = useState({
    first_name: '',
    last_name: '',
    phone: '',
  })

  useEffect(() => {
    fetchProfile()
  }, [])

  const fetchProfile = async () => {
    try {
      setLoading(true)
      const response = await api.get('/users/me')
      setProfile(response.data)
      setEditForm({
        first_name: response.data.first_name || '',
        last_name: response.data.last_name || '',
        phone: response.data.phone || '',
      })
    } catch (error) {
      console.error('Failed to fetch profile:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    try {
      await api.put('/users/me', editForm)
      await fetchProfile()
      setEditing(false)
    } catch (error) {
      console.error('Failed to update profile:', error)
    }
  }

  if (loading) {
    return (
      <div className="container py-12">
        <div className="flex items-center justify-center min-h-[400px]">
          <p className="text-muted-foreground">Загрузка профиля...</p>
        </div>
      </div>
    )
  }

  if (!profile) {
    return (
      <div className="container py-12">
        <Card>
          <CardContent className="py-12 text-center">
            <p className="text-destructive">Не удалось загрузить профиль</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  const nextTier = profile.tier === 'BRONZE' ? 'SILVER' : profile.tier === 'SILVER' ? 'GOLD' : profile.tier === 'GOLD' ? 'PLATINUM' : null
  const pointsForNextTier = profile.tier === 'BRONZE' ? 5000 : profile.tier === 'SILVER' ? 15000 : profile.tier === 'GOLD' ? 50000 : 0
  const progressPercent = nextTier ? Math.min((profile.loyalty_points / pointsForNextTier) * 100, 100) : 100

  return (
    <div className="container py-8 max-w-6xl">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">Мой профиль</h1>
        <p className="text-muted-foreground">
          Управляйте своей учетной записью и программой лояльности
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Profile Info */}
        <div className="lg:col-span-2 space-y-6">
          {/* Basic Info Card */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2">
                  <User className="h-5 w-5" />
                  Основная информация
                </CardTitle>
                {!editing ? (
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setEditing(true)}
                  >
                    <Edit className="h-4 w-4 mr-2" />
                    Редактировать
                  </Button>
                ) : (
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => {
                        setEditing(false)
                        setEditForm({
                          first_name: profile.first_name || '',
                          last_name: profile.last_name || '',
                          phone: profile.phone || '',
                        })
                      }}
                    >
                      <X className="h-4 w-4 mr-2" />
                      Отмена
                    </Button>
                    <Button size="sm" onClick={handleSave}>
                      <Save className="h-4 w-4 mr-2" />
                      Сохранить
                    </Button>
                  </div>
                )}
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {!editing ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label className="text-muted-foreground">Имя</Label>
                    <p className="text-lg font-medium">{profile.first_name || '—'}</p>
                  </div>
                  <div>
                    <Label className="text-muted-foreground">Фамилия</Label>
                    <p className="text-lg font-medium">{profile.last_name || '—'}</p>
                  </div>
                  <div>
                    <Label className="text-muted-foreground flex items-center gap-2">
                      <Mail className="h-4 w-4" />
                      Email
                    </Label>
                    <p className="text-lg font-medium">{profile.email}</p>
                  </div>
                  <div>
                    <Label className="text-muted-foreground flex items-center gap-2">
                      <Phone className="h-4 w-4" />
                      Телефон
                    </Label>
                    <p className="text-lg font-medium">{profile.phone || '—'}</p>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="first_name">Имя</Label>
                      <Input
                        id="first_name"
                        value={editForm.first_name}
                        onChange={(e) =>
                          setEditForm({ ...editForm, first_name: e.target.value })
                        }
                      />
                    </div>
                    <div>
                      <Label htmlFor="last_name">Фамилия</Label>
                      <Input
                        id="last_name"
                        value={editForm.last_name}
                        onChange={(e) =>
                          setEditForm({ ...editForm, last_name: e.target.value })
                        }
                      />
                    </div>
                  </div>
                  <div>
                    <Label htmlFor="phone">Телефон</Label>
                    <Input
                      id="phone"
                      type="tel"
                      value={editForm.phone}
                      onChange={(e) =>
                        setEditForm({ ...editForm, phone: e.target.value })
                      }
                      placeholder="+7 700 123 4567"
                    />
                  </div>
                  <div>
                    <Label className="text-muted-foreground">Email (не редактируется)</Label>
                    <Input value={profile.email} disabled />
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Account Details Card */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="h-5 w-5" />
                Детали аккаунта
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label className="text-muted-foreground">ID пользователя</Label>
                  <p className="text-sm font-mono">{profile.id.substring(0, 8)}...</p>
                </div>
                <div>
                  <Label className="text-muted-foreground">Дата регистрации</Label>
                  <p className="text-sm">
                    {new Date(profile.created_at).toLocaleDateString('ru-RU', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                    })}
                  </p>
                </div>
                <div>
                  <Label className="text-muted-foreground">Язык</Label>
                  <p className="text-sm">{profile.preferred_language === 'en' ? 'English' : 'Русский'}</p>
                </div>
                <div>
                  <Label className="text-muted-foreground">Валюта</Label>
                  <p className="text-sm">{profile.preferred_currency}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right Column - Loyalty Program */}
        <div className="space-y-6">
          {/* Loyalty Tier Card */}
          <Card className="border-2">
            <CardHeader className="pb-4">
              <CardTitle className="flex items-center gap-2">
                <Award className="h-5 w-5" />
                Программа лояльности
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Tier Badge */}
              <div className="text-center py-6">
                <div
                  className={`inline-flex items-center justify-center w-24 h-24 rounded-full ${getTierColor(
                    profile.tier
                  )} text-white mb-4`}
                >
                  <Award className="h-12 w-12" />
                </div>
                <h3 className="text-2xl font-bold mb-2">{profile.tier}</h3>
                <p className="text-3xl font-bold text-primary">
                  {profile.loyalty_points.toLocaleString()}
                </p>
                <p className="text-sm text-muted-foreground">баллов</p>
              </div>

              {/* Progress to Next Tier */}
              {nextTier && (
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>До {nextTier}</span>
                    <span className="font-medium">
                      {pointsForNextTier - profile.loyalty_points} баллов
                    </span>
                  </div>
                  <div className="h-2 bg-muted rounded-full overflow-hidden">
                    <div
                      className="h-full bg-primary transition-all"
                      data-progress={progressPercent}
                      style={{ width: `${Math.round(progressPercent)}%` } as React.CSSProperties}
                    />
                  </div>
                </div>
              )}

              {/* Benefits */}
              <div>
                <h4 className="font-semibold mb-2">Ваши привилегии:</h4>
                <ul className="space-y-1">
                  {getTierBenefits(profile.tier).map((benefit, index) => (
                    <li key={index} className="text-sm flex items-start gap-2">
                      <span className="text-primary">✓</span>
                      <span>{benefit}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </CardContent>
          </Card>

          {/* Quick Stats */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Plane className="h-5 w-5" />
                Статистика
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-muted-foreground">Всего полетов</span>
                <span className="text-xl font-bold">0</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-muted-foreground">Активных броней</span>
                <span className="text-xl font-bold">0</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-muted-foreground">Стран посещено</span>
                <span className="text-xl font-bold">0</span>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
