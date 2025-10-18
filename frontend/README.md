# FlightHub Frontend

Современный, красивый frontend для платформы бронирования авиабилетов FlightHub.

## 🎨 Технологии

- **React 18** - UI библиотека
- **TypeScript** - Type safety
- **Vite** - Build tool & dev server
- **Tailwind CSS** - Utility-first CSS
- **shadcn/ui** - Beautiful UI components
- **React Router v6** - Client-side routing
- **TanStack Query** - Server state management
- **Zustand** - Client state management
- **React Hook Form + Zod** - Form handling & validation
- **Axios** - HTTP client
- **Sonner** - Toast notifications
- **Lucide React** - Beautiful icons
- **Framer Motion** - Animations

## 📦 Установка

### Предварительные требования

- Node.js 20+ (рекомендуется)
- npm или yarn

### Локальная разработка

```bash
# Перейти в директорию frontend
cd frontend

# Установить зависимости
npm install

# Запустить dev сервер
npm run dev
```

Приложение будет доступно по адресу: http://localhost:3000

## 🚀 Сборка для Production

```bash
# Build
npm run build

# Preview production build
npm run preview
```

## 🐳 Docker

### Собрать Docker образ

```bash
docker build -t flighthub-frontend .
```

### Запустить контейнер

```bash
docker run -p 3000:80 flighthub-frontend
```

### Docker Compose (вся система)

Из корневой директории проекта:

```bash
docker-compose up -d
```

Frontend будет доступен на порту 3000.

## 📁 Структура проекта

```
frontend/
├── src/
│   ├── components/          # React компоненты
│   │   ├── ui/             # UI компоненты (Button, Card и т.д.)
│   │   └── layout/         # Layout компоненты (Header, Footer)
│   ├── pages/              # Страницы приложения
│   │   ├── HomePage.tsx
│   │   ├── LoginPage.tsx
│   │   ├── RegisterPage.tsx
│   │   ├── FlightSearchPage.tsx
│   │   ├── BookingPage.tsx
│   │   └── ...
│   ├── services/           # API сервисы
│   │   ├── api.ts          # Axios instance
│   │   ├── auth.ts         # Auth API
│   │   ├── flights.ts      # Flights API
│   │   ├── bookings.ts     # Bookings API
│   │   └── payments.ts     # Payments API
│   ├── store/              # Zustand state management
│   │   ├── authStore.ts
│   │   └── flightStore.ts
│   ├── types/              # TypeScript types
│   │   └── index.ts
│   ├── lib/                # Утилиты
│   │   └── utils.ts
│   ├── App.tsx             # Root component
│   ├── main.tsx            # Entry point
│   └── index.css           # Global styles
├── public/                 # Static assets
├── Dockerfile
├── nginx.conf
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── vite.config.ts
└── README.md
```

## 🎯 Основные фичи

### ✅ Реализовано

- 🎨 Современный UI/UX дизайн
- 📱 Responsive дизайн (mobile-first)
- 🔐 JWT авторизация с auto-refresh
- 🛡️ Protected routes
- 🎨 Hero секция с поиском
- 📍 Популярные направления
- 🔄 API интеграция
- 📝 Формы с валидацией
- 🌐 Routing
- 🎯 State management
- 🎨 Toast notifications
- 🔄 Loading states
- ❌ Error handling

### 🚧 В разработке

- ✈️ Поиск и фильтрация рейсов
- 📋 Детали рейса
- 🎫 Процесс бронирования
- 💳 Интеграция оплаты
- 📱 Личный кабинет
- 📊 История бронирований
- 🎁 Программа лояльности
- 🌙 Dark mode
- 🌍 i18n (Интернационализация)
- 📊 Dashboard с аналитикой

## 🔌 API Интеграция

Frontend взаимодействует с backend через API Gateway на порту 8000.

### Environment Variables

Создайте файл `.env.local` в корне `frontend/`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

### Основные endpoints

- `POST /api/v1/users/register/` - Регистрация
- `POST /api/v1/users/login/` - Вход
- `GET /api/v1/users/profile/` - Профиль
- `GET /api/v1/flights/search` - Поиск рейсов
- `GET /api/v1/flights/:id` - Детали рейса
- `POST /api/v1/bookings/` - Создание бронирования
- `GET /api/v1/bookings/` - Список бронирований
- `POST /api/v1/payments/` - Создание платежа

## 🎨 Дизайн система

### Цветовая схема

- **Primary**: Blue (#3b82f6) - Основной цвет для кнопок, ссылок
- **Secondary**: Gray - Второстепенные элементы
- **Accent**: Light blue - Акценты и hover states
- **Destructive**: Red - Ошибки и удаление
- **Muted**: Light gray - Фоны и неактивные элементы

### Typography

- **Font**: System font stack (Inter, SF Pro, Segoe UI)
- **Headings**: Bold, различные размеры
- **Body**: Regular, 14-16px

### Компоненты

Все UI компоненты построены на базе shadcn/ui:
- Button - различные варианты (default, outline, ghost и т.д.)
- Card - для контентных блоков
- Input - поля ввода с валидацией
- Label - метки для форм
- Toast - уведомления (через Sonner)

## 🔧 Разработка

### Добавление новых UI компонентов

Используйте shadcn/ui CLI для добавления компонентов:

```bash
npx shadcn-ui@latest add [component-name]
```

Например:
```bash
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add dropdown-menu
npx shadcn-ui@latest add select
```

### Code Style

```bash
# Lint
npm run lint

# Type check
npm run type-check
```

## 🧪 Тестирование

```bash
# Run tests (когда будут добавлены)
npm run test

# Coverage
npm run test:coverage
```

## 📚 Полезные ресурсы

- [React Документация](https://react.dev/)
- [Vite Документация](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [shadcn/ui](https://ui.shadcn.com/)
- [React Router](https://reactrouter.com/)
- [TanStack Query](https://tanstack.com/query)
- [Zustand](https://zustand-demo.pmnd.rs/)

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Лицензия

MIT

## 👨‍💻 Автор

FlightHub Team

---

**Happy Coding! ✈️**
