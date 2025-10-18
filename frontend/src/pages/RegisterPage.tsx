import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { toast } from 'sonner'
import { Plane, Mail, Lock, User, Phone } from 'lucide-react'
import { useAuthStore } from '@/store/authStore'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card'

const registerSchema = z.object({
  email: z.string().email('Неверный формат email'),
  password: z.string().min(6, 'Пароль должен быть минимум 6 символов'),
  confirmPassword: z.string(),
  first_name: z.string().min(2, 'Имя должно быть минимум 2 символа'),
  last_name: z.string().min(2, 'Фамилия должна быть минимум 2 символа'),
  phone: z.string().optional(),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Пароли не совпадают',
  path: ['confirmPassword'],
})

type RegisterFormData = z.infer<typeof registerSchema>

export default function RegisterPage() {
  const navigate = useNavigate()
  const { register: registerUser } = useAuthStore()
  const [isLoading, setIsLoading] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  })

  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true)
    try {
      const { confirmPassword, ...registerData } = data
      await registerUser(registerData)
      toast.success('Регистрация успешна! Добро пожаловать!')
      navigate('/')
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || 'Ошибка регистрации'
      toast.error(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-4rem)] bg-muted/30 py-12 px-4">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1 text-center">
          <div className="flex justify-center mb-4">
            <div className="p-3 bg-primary/10 rounded-full">
              <Plane className="h-8 w-8 text-primary" />
            </div>
          </div>
          <CardTitle className="text-2xl font-bold">Регистрация</CardTitle>
          <CardDescription>
            Создайте аккаунт и начните бронировать рейсы
          </CardDescription>
        </CardHeader>

        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            {/* First Name */}
            <div className="space-y-2">
              <Label htmlFor="first_name" className="flex items-center gap-2">
                <User className="h-4 w-4" />
                Имя
              </Label>
              <Input
                id="first_name"
                placeholder="Иван"
                {...register('first_name')}
                disabled={isLoading}
              />
              {errors.first_name && (
                <p className="text-sm text-destructive">{errors.first_name.message}</p>
              )}
            </div>

            {/* Last Name */}
            <div className="space-y-2">
              <Label htmlFor="last_name" className="flex items-center gap-2">
                <User className="h-4 w-4" />
                Фамилия
              </Label>
              <Input
                id="last_name"
                placeholder="Иванов"
                {...register('last_name')}
                disabled={isLoading}
              />
              {errors.last_name && (
                <p className="text-sm text-destructive">{errors.last_name.message}</p>
              )}
            </div>

            {/* Email */}
            <div className="space-y-2">
              <Label htmlFor="email" className="flex items-center gap-2">
                <Mail className="h-4 w-4" />
                Email
              </Label>
              <Input
                id="email"
                type="email"
                placeholder="user@example.com"
                {...register('email')}
                disabled={isLoading}
              />
              {errors.email && (
                <p className="text-sm text-destructive">{errors.email.message}</p>
              )}
            </div>

            {/* Phone */}
            <div className="space-y-2">
              <Label htmlFor="phone" className="flex items-center gap-2">
                <Phone className="h-4 w-4" />
                Телефон (опционально)
              </Label>
              <Input
                id="phone"
                type="tel"
                placeholder="+7 (700) 123-45-67"
                {...register('phone')}
                disabled={isLoading}
              />
            </div>

            {/* Password */}
            <div className="space-y-2">
              <Label htmlFor="password" className="flex items-center gap-2">
                <Lock className="h-4 w-4" />
                Пароль
              </Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                {...register('password')}
                disabled={isLoading}
              />
              {errors.password && (
                <p className="text-sm text-destructive">{errors.password.message}</p>
              )}
            </div>

            {/* Confirm Password */}
            <div className="space-y-2">
              <Label htmlFor="confirmPassword" className="flex items-center gap-2">
                <Lock className="h-4 w-4" />
                Подтвердите пароль
              </Label>
              <Input
                id="confirmPassword"
                type="password"
                placeholder="••••••••"
                {...register('confirmPassword')}
                disabled={isLoading}
              />
              {errors.confirmPassword && (
                <p className="text-sm text-destructive">{errors.confirmPassword.message}</p>
              )}
            </div>

            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? 'Регистрация...' : 'Зарегистрироваться'}
            </Button>
          </form>
        </CardContent>

        <CardFooter className="flex justify-center">
          <div className="text-sm text-center text-muted-foreground">
            Уже есть аккаунт?{' '}
            <Link to="/login" className="text-primary hover:underline font-medium">
              Войти
            </Link>
          </div>
        </CardFooter>
      </Card>
    </div>
  )
}
