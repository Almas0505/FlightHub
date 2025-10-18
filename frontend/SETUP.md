# 🚀 Инструкция по запуску Frontend FlightHub

## Быстрый старт (3 способа)

### 🔥 Способ 1: Локальная разработка (Рекомендуется для разработки)

```powershell
# 1. Перейти в директорию frontend
cd frontend

# 2. Установить зависимости
npm install

# 3. Запустить dev сервер
npm run dev
```

Приложение будет доступно на: **http://localhost:3000**

### 🐳 Способ 2: Только frontend в Docker

```powershell
# Из директории frontend
cd frontend

# Собрать образ
docker build -t flighthub-frontend .

# Запустить контейнер
docker run -p 3000:80 flighthub-frontend
```

Приложение будет доступно на: **http://localhost:3000**

### 🎯 Способ 3: Вся система через Docker Compose (Production-like)

```powershell
# Из корневой директории проекта
cd c:\Projects\flighthub

# Запустить всю систему (включая backend + frontend)
docker-compose up -d

# Проверить статус
docker-compose ps
```

Приложение будет доступно на:
- **Frontend**: http://localhost:3000
- **API Gateway**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs

## 📋 Требования

### Для локальной разработки:
- Node.js 20+ (проверить: `node --version`)
- npm или yarn
- Backend должен быть запущен на localhost:8000

### Для Docker:
- Docker Desktop (Windows)
- 4GB RAM минимум

## 🔧 Конфигурация

### Environment Variables

Создайте файл `.env.local` в директории `frontend/`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

**Важно**: 
- Для локальной разработки используйте `http://localhost:8000`
- Для production используйте реальный URL вашего API

## 📦 Установка зависимостей

```powershell
cd frontend
npm install
```

Устанавливаемые пакеты:
- ✅ React 18 + React DOM
- ✅ React Router v6
- ✅ TypeScript
- ✅ Tailwind CSS + shadcn/ui
- ✅ Axios (HTTP client)
- ✅ TanStack Query (data fetching)
- ✅ Zustand (state management)
- ✅ React Hook Form + Zod (forms)
- ✅ Framer Motion (animations)
- ✅ Lucide React (icons)
- ✅ Sonner (toast notifications)

## 🎨 Доступные скрипты

```powershell
# Development сервер с hot reload
npm run dev

# Production build
npm run build

# Preview production build локально
npm run preview

# Lint проверка
npm run lint

# Type checking
npm run type-check
```

## 🔗 Интеграция с Backend

Frontend подключается к API Gateway на порту 8000.

### Запустить Backend

```powershell
# Из корневой директории
docker-compose up -d postgres mongodb redis rabbitmq api-gateway flight-search booking-service user-service payment-service
```

### Проверить доступность API

```powershell
# Health check
curl http://localhost:8000/health

# API Documentation
# Откройте в браузере: http://localhost:8000/docs
```

## 🎯 Структура проекта

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/              # shadcn/ui компоненты
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── input.tsx
│   │   │   └── label.tsx
│   │   └── layout/          # Layout компоненты
│   │       ├── Header.tsx
│   │       ├── Footer.tsx
│   │       └── MainLayout.tsx
│   ├── pages/               # Страницы
│   │   ├── HomePage.tsx         ✅ Готово
│   │   ├── LoginPage.tsx        ✅ Готово
│   │   ├── RegisterPage.tsx     ✅ Готово
│   │   ├── FlightSearchPage.tsx 🚧 В разработке
│   │   ├── BookingPage.tsx      🚧 В разработке
│   │   ├── PaymentPage.tsx      🚧 В разработке
│   │   ├── MyBookingsPage.tsx   🚧 В разработке
│   │   ├── ProfilePage.tsx      🚧 В разработке
│   │   └── NotFoundPage.tsx     ✅ Готово
│   ├── services/            # API сервисы
│   │   ├── api.ts          # Axios config
│   │   ├── auth.ts         # Auth API
│   │   ├── flights.ts      # Flights API
│   │   ├── bookings.ts     # Bookings API
│   │   └── payments.ts     # Payments API
│   ├── store/              # State management
│   │   ├── authStore.ts
│   │   └── flightStore.ts
│   ├── types/              # TypeScript types
│   │   └── index.ts
│   ├── lib/                # Utilities
│   │   └── utils.ts
│   ├── App.tsx             # Root component
│   ├── main.tsx            # Entry point
│   └── index.css           # Global styles
├── public/
├── Dockerfile
├── nginx.conf
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── vite.config.ts
└── README.md
```

## ✅ Что уже реализовано

### Основа приложения
- ✅ React 18 + TypeScript + Vite
- ✅ Tailwind CSS + shadcn/ui
- ✅ Routing (React Router v6)
- ✅ State management (Zustand)
- ✅ API интеграция (Axios + TanStack Query)
- ✅ Form validation (React Hook Form + Zod)
- ✅ Toast notifications (Sonner)

### UI Компоненты
- ✅ Button (variants: default, outline, ghost, link)
- ✅ Card (с Header, Content, Footer)
- ✅ Input (с валидацией)
- ✅ Label
- ✅ Header (навигация, mobile menu)
- ✅ Footer

### Страницы
- ✅ **Home Page** - Hero секция, поиск, популярные направления
- ✅ **Login Page** - Форма входа с валидацией
- ✅ **Register Page** - Форма регистрации
- ✅ **404 Page** - Not Found

### Фичи
- ✅ JWT Authentication
- ✅ Protected Routes
- ✅ Auto token refresh
- ✅ Responsive дизайн
- ✅ Loading states
- ✅ Error handling
- ✅ Docker готов к деплою

## 🚧 В разработке

- 🚧 Flight Search Page (с фильтрами)
- 🚧 Flight Details Page
- 🚧 Booking Process
- 🚧 Payment Integration
- 🚧 User Profile
- 🚧 Bookings History
- 🚧 Dark Mode
- 🚧 i18n (мультиязычность)

## 🎨 Дизайн особенности

### Цветовая схема
- **Primary**: Синий (#3b82f6) - для основных действий
- **Gradient Hero**: from-blue-600 via-blue-700 to-blue-900
- **Muted backgrounds**: серый/50 для секций
- **Cards**: белые с тенями и hover эффектами

### Анимации
- Hover эффекты на кнопках и картах
- Transform scale на popular destinations
- Smooth transitions

### Responsive
- Mobile-first подход
- Breakpoints: sm, md, lg, xl, 2xl
- Burger menu для мобильных

## 🔍 Тестирование

### Проверка работоспособности:

1. **Главная страница**: http://localhost:3000
   - Должна показать Hero секцию
   - Форма поиска
   - Популярные направления

2. **Регистрация**: http://localhost:3000/register
   - Форма с валидацией
   - Создание аккаунта

3. **Вход**: http://localhost:3000/login
   - Авторизация через JWT
   - Перенаправление на главную

4. **Protected routes**:
   - `/profile` - требует авторизации
   - `/my-bookings` - требует авторизации

## ⚠️ Возможные проблемы и решения

### 1. "Cannot connect to API"
**Проблема**: Frontend не может подключиться к backend
**Решение**:
```powershell
# Проверить что API Gateway запущен
curl http://localhost:8000/health

# Проверить .env.local файл
cat frontend/.env.local

# Должно быть: VITE_API_BASE_URL=http://localhost:8000
```

### 2. "CORS Error"
**Проблема**: CORS блокирует запросы
**Решение**: Backend уже настроен для CORS. Убедитесь что используете правильный URL.

### 3. "Module not found"
**Проблема**: Не установлены зависимости
**Решение**:
```powershell
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### 4. "Port 3000 already in use"
**Проблема**: Порт занят
**Решение**:
```powershell
# Изменить порт в vite.config.ts
# или убить процесс на порту 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

## 📚 Полезные команды

```powershell
# Посмотреть логи в Docker
docker-compose logs -f frontend

# Остановить только frontend
docker-compose stop frontend

# Перезапустить frontend
docker-compose restart frontend

# Пересобрать образ
docker-compose up -d --build frontend

# Зайти в контейнер
docker exec -it flighthub-frontend sh
```

## 🚀 Production Deployment

### Build для production

```powershell
cd frontend
npm run build
```

Результат будет в папке `dist/`

### Docker Image

```powershell
# Build
docker build -t flighthub-frontend:latest .

# Push to registry
docker tag flighthub-frontend:latest your-registry/flighthub-frontend:latest
docker push your-registry/flighthub-frontend:latest
```

## 📖 Документация

- [React Docs](https://react.dev/)
- [Vite Docs](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [shadcn/ui](https://ui.shadcn.com/)
- [Backend API Docs](http://localhost:8000/docs)

## 🤝 Contributing

Хотите добавить новую фичу?

1. Создайте новый компонент в `src/components/`
2. Добавьте новую страницу в `src/pages/`
3. Обновите роутинг в `App.tsx`
4. Добавьте API сервис в `src/services/`
5. Обновите типы в `src/types/`

## 💡 Tips & Tricks

1. **Hot Module Replacement (HMR)** работает автоматически
2. Используйте **React DevTools** для отладки
3. **TypeScript** подскажет ошибки до запуска
4. **Tailwind IntelliSense** - установите расширение для VS Code
5. Смотрите Network tab в DevTools для отладки API запросов

---

**Happy Coding! ✈️🚀**

**Вопросы?** Открывайте issue или смотрите [README.md](./README.md)
