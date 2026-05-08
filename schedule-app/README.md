# Генератор расписания смен

Веб-приложение для составления и генерации расписания смен с возможностью копирования в Telegram.

## Технологии

### Frontend
- React 18 + TypeScript
- Vite
- TailwindCSS
- shadcn/ui
- Zustand (state management)
- @dnd-kit (drag-and-drop)

### Backend
- Node.js + Express
- Prisma ORM
- PostgreSQL

## Быстрый старт

### Предварительные требования
- Node.js 18+
- PostgreSQL 14+

### База данных
```bash
sudo -u postgres psql -c "CREATE DATABASE schedule_db;"
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"
```

### Backend
```bash
cd schedule-app/server
cp .env.example .env
npm install
npx prisma generate
npx prisma db push
npm run dev
```
Сервер запустится на `http://localhost:3001`

### Frontend
```bash
cd schedule-app/client
npm install
npm run dev
```
Клиент запустится на `http://localhost:5173`

## Функционал

- Создание расписания с датой и днём недели
- Добавление блоков разделки/сборки
- Drag-and-drop перестановка блоков
- Inline-редактирование полей
- Генерация текста для Telegram с точным форматированием
- Копирование в буфер обмена одной кнопкой
- Экспорт в TXT
- Шаблоны расписаний
- История сохранённых расписаний
- Автосохранение
- Горячие клавиши (Ctrl+B, Ctrl+M, Ctrl+G, Ctrl+S, Ctrl+N)

## API Endpoints

| Метод  | URL                          | Описание                    |
|--------|------------------------------|-----------------------------|
| GET    | /api/schedules               | Список расписаний           |
| GET    | /api/schedules/:id           | Получить расписание         |
| POST   | /api/schedules               | Создать расписание          |
| PUT    | /api/schedules/:id           | Обновить расписание         |
| PUT    | /api/schedules/:id/autosave  | Автосохранение              |
| DELETE | /api/schedules/:id           | Удалить расписание          |
| GET    | /api/schedules/:id/generate  | Сгенерировать текст         |
| GET    | /api/templates               | Список шаблонов             |
| POST   | /api/templates               | Создать шаблон              |
| DELETE | /api/templates/:id           | Удалить шаблон              |
| GET    | /api/workers                 | Список работников           |
| POST   | /api/workers                 | Создать работника           |
| PUT    | /api/workers/:id             | Обновить работника          |
| DELETE | /api/workers/:id             | Удалить работника           |
| GET    | /api/health                  | Health check                |

## Структура БД (Prisma)

- **schedules** — расписания (дата, день недели, блоки в JSON)
- **templates** — шаблоны расписаний
- **workers** — справочник работников
