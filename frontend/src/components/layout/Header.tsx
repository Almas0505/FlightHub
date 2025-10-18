import { Link, useNavigate } from 'react-router-dom'
import { Plane, User, LogOut, Menu } from 'lucide-react'
import { useAuthStore } from '@/store/authStore'
import { Button } from '@/components/ui/button'
import { useState } from 'react'

export default function Header() {
  const { isAuthenticated, user, logout } = useAuthStore()
  const navigate = useNavigate()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between">
        {/* Logo */}
        <Link to="/" className="flex items-center space-x-2">
          <Plane className="h-6 w-6 text-primary" />
          <span className="text-xl font-bold">FlightHub</span>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center space-x-6">
          <Link to="/flights" className="text-sm font-medium hover:text-primary transition-colors">
            Поиск рейсов
          </Link>
          {isAuthenticated && (
            <Link to="/my-bookings" className="text-sm font-medium hover:text-primary transition-colors">
              Мои бронирования
            </Link>
          )}
        </nav>

        {/* Right Side */}
        <div className="hidden md:flex items-center space-x-4">
          {isAuthenticated ? (
            <>
              <Link to="/profile">
                <Button variant="ghost" size="sm" className="gap-2">
                  <User className="h-4 w-4" />
                  {user?.first_name || 'Профиль'}
                </Button>
              </Link>
              <Button variant="outline" size="sm" onClick={handleLogout} className="gap-2">
                <LogOut className="h-4 w-4" />
                Выйти
              </Button>
            </>
          ) : (
            <>
              <Link to="/login">
                <Button variant="ghost" size="sm">
                  Войти
                </Button>
              </Link>
              <Link to="/register">
                <Button size="sm">
                  Регистрация
                </Button>
              </Link>
            </>
          )}
        </div>

        {/* Mobile Menu Button */}
        <button
          className="md:hidden"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          <Menu className="h-6 w-6" />
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t">
          <nav className="container py-4 flex flex-col space-y-4">
            <Link
              to="/flights"
              className="text-sm font-medium hover:text-primary transition-colors"
              onClick={() => setMobileMenuOpen(false)}
            >
              Поиск рейсов
            </Link>
            {isAuthenticated && (
              <>
                <Link
                  to="/my-bookings"
                  className="text-sm font-medium hover:text-primary transition-colors"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Мои бронирования
                </Link>
                <Link
                  to="/profile"
                  className="text-sm font-medium hover:text-primary transition-colors"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Профиль
                </Link>
                <Button variant="outline" size="sm" onClick={handleLogout}>
                  Выйти
                </Button>
              </>
            )}
            {!isAuthenticated && (
              <>
                <Link to="/login" onClick={() => setMobileMenuOpen(false)}>
                  <Button variant="ghost" size="sm" className="w-full">
                    Войти
                  </Button>
                </Link>
                <Link to="/register" onClick={() => setMobileMenuOpen(false)}>
                  <Button size="sm" className="w-full">
                    Регистрация
                  </Button>
                </Link>
              </>
            )}
          </nav>
        </div>
      )}
    </header>
  )
}
