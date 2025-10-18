import { Link } from 'react-router-dom'
import { Plane, Mail, Phone, MapPin } from 'lucide-react'

export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="border-t bg-muted/50 mt-auto">
      <div className="container py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* About */}
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <Plane className="h-5 w-5 text-primary" />
              <span className="font-bold">FlightHub</span>
            </div>
            <p className="text-sm text-muted-foreground">
              Современная платформа для поиска и бронирования авиабилетов по всему миру.
            </p>
          </div>

          {/* Links */}
          <div>
            <h3 className="font-semibold mb-4">Компания</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <Link to="/about" className="hover:text-primary transition-colors">
                  О нас
                </Link>
              </li>
              <li>
                <Link to="/careers" className="hover:text-primary transition-colors">
                  Карьера
                </Link>
              </li>
              <li>
                <Link to="/press" className="hover:text-primary transition-colors">
                  Пресса
                </Link>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="font-semibold mb-4">Поддержка</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <Link to="/help" className="hover:text-primary transition-colors">
                  Помощь
                </Link>
              </li>
              <li>
                <Link to="/terms" className="hover:text-primary transition-colors">
                  Условия использования
                </Link>
              </li>
              <li>
                <Link to="/privacy" className="hover:text-primary transition-colors">
                  Политика конфиденциальности
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="font-semibold mb-4">Контакты</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li className="flex items-center gap-2">
                <Mail className="h-4 w-4" />
                support@flighthub.com
              </li>
              <li className="flex items-center gap-2">
                <Phone className="h-4 w-4" />
                +7 (700) 123-45-67
              </li>
              <li className="flex items-center gap-2">
                <MapPin className="h-4 w-4" />
                Алматы, Казахстан
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t mt-8 pt-8 text-center text-sm text-muted-foreground">
          <p>&copy; {currentYear} FlightHub. Все права защищены.</p>
        </div>
      </div>
    </footer>
  )
}
