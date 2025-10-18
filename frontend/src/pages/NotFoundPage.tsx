import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'

export default function NotFoundPage() {
  return (
    <div className="container flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] text-center">
      <h1 className="text-9xl font-bold text-primary">404</h1>
      <h2 className="text-3xl font-bold mt-4 mb-2">Страница не найдена</h2>
      <p className="text-muted-foreground mb-8">
        Страница, которую вы ищете, не существует или была удалена.
      </p>
      <Link to="/">
        <Button size="lg">Вернуться на главную</Button>
      </Link>
    </div>
  )
}
