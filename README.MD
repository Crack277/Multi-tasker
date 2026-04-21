# Task Management API

Многофункциональный RESTful API для управления задачами, проектами и пользователями. Построен на FastAPI с использованием асинхронных технологий.

## 🚀 Основные возможности

- **Управление пользователями**: регистрация, аутентификация, профили
- **Управление проектами**: создание, обновление, удаление проектов
- **Управление задачами**: создание, назначение, приоритеты, статусы
- **Категоризация**: гибкая система категорий с цветовой маркировкой
- **JWT аутентификация**: безопасная авторизация с черным списком токенов
- **Redis**: кэширование и управление сессиями
- **Email уведомления**: подтверждение действий через SMTP
- **Загрузка файлов**: аватары пользователей и иконки проектов
- **Миграции БД**: Alembic для управления схемой базы данных
- **Docker**: контейнеризация приложения и зависимостей

## 🛠 Технологический стек

- **FastAPI** - веб-фреймворк
- **SQLAlchemy 2.0** - асинхронная ORM
- **Alembic** - миграции базы данных
- **PostgreSQL** - основная база данных
- **Redis** - кэширование и blacklist токенов
- **AIOFiles** - асинхронная работа с файлами
- **Aiosmtplib** - асинхронная отправка email
- **JWT** - аутентификация
- **Pydantic** - валидация данных
- **Poetry** - управление зависимостями
- **Docker & Docker Compose** - контейнеризация

## 📂 Структура проекта

```
├── alembic/ # Миграции базы данных
├── src/
│ ├── api/ # API слой
│ │ ├── repositories/ # Репозитории (работа с БД)
│ │ ├── routers/ # Маршруты API
│ │ ├── schemas/ # Pydantic схемы
│ │ ├── services/ # Бизнес-логика
│ │ └── utils/ # Утилиты
│ │   ├── smtp/ # Email уведомления
│ │   │ ├── email_body.py
│ │   │ ├── send_email.py
│ │   │ ├── smtp_email_backend.py
│ │   │ └── task.py
│ │   ├── static/ # Статические файлы
│ │   │ └── photo/ # Загруженные изображения
│ │   └── security.py # JWT и хэширование
│ ├── database/ # Настройка БД
│ │ └── database_helper.py
│ ├── models/ # SQLAlchemy модели
│ ├── config.py # Конфигурация приложения
│ └── redis.py # Redis клиент
└── main.py # Точка входа

```

## 🔧 Установка и запуск

### Клонирование репозитория

```bash
git clone https://github.com/Crack277/Multi-tasker.git
```

### Установка зависимостей

```bash
poetry install #--no-root
```

### Настройка переменных окружения

```
# APP
APP_CONFIG__HOST=localhost
APP_CONFIG__PORT=8000
# DB
APP_CONFIG__DB__USERNAME=postgres
APP_CONFIG__DB__PASSWORD=postgres
APP_CONFIG__DB__HOST=localhost
APP_CONFIG__DB__PORT=5432
APP_CONFIG__DB__NAME=postgres
APP_CONFIG__DB__ECHO=false
# REDIS
APP_CONFIG__REDIS__HOST=localhost
APP_CONFIG__REDIS__PORT=6379
APP_CONFIG__REDIS__DB=0
#APP_CONFIG__REDIS__PASSWORD=None Если без пароля - оставить так, иначе - поменять
# JWTTOKEN
APP_CONFIG__ACCESS_TOKEN__SECRET_KEY=1234567890
```

### Применение миграций

```bash
alembic upgrade head
```

### Запуск приложения

```bash
python main.py
# или
poetry run python main.py
```

## 📊 Модели данных

### User (Пользователь)

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `Integer` | Уникальный идентификатор |
| `email` | `String` | Email пользователя (уникальный) |
| `hashed_password` | `String` | Хэшированный пароль |
| `confirm_code` | `String` | Код подтверждения (6 цифр) |
| `is_superuser` | `Boolean` | Флаг администратора |

### Profile (Профиль)

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `Integer` | Уникальный идентификатор |
| `name` | `String(50)` | Имя пользователя |
| `email` | `String` | Email (связь с User) |
| `photo` | `String` | URL аватара |
| `user_id` | `Integer` | Внешний ключ к User |

### Project (Проект)

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `Integer` | Уникальный идентификатор |
| `name` | `String(100)` | Название проекта |
| `icon` | `String(100)` | URL иконки |
| `owner_id` | `Integer` | ID владельца |

### Category (Категория)

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `Integer` | Уникальный идентификатор |
| `name` | `String(100)` | Название категории |
| `marker` | `String(7)` | Цвет категории (HEX, например `#cac4b0`) |
| `user_id` | `Integer` | ID создателя |

### Task (Задача)

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `Integer` | Уникальный идентификатор |
| `title` | `String(100)` | Заголовок задачи |
| `description` | `Text` | Описание |
| `priority` | `Enum` | Приоритет: `very_urgent`, `urgent`, `can_wait`, `not_urgent` |
| `status` | `Enum` | Статус: `in_progress`, `completed` |
| `deadline` | `DateTime` | Дедлайн |
| `created_at` | `DateTime` | Дата создания |
| `updated_at` | `DateTime` | Дата обновления |
| `author_id` | `Integer` | ID создателя |
| `assignee_id` | `Integer` | ID исполнителя |
| `project_id` | `Integer` | ID проекта |
| `category_id` | `Integer` | ID категории |

## 📧 Email уведомления

Email утилиты находятся в `src/api/utils/smtp/`:

| Файл | Описание |
|------|----------|
| `email_body.py` | Формирование HTML/текстовых шаблонов писем |
| `send_email.py` | Асинхронная отправка email через aiosmtplib |
| `smtp_email_backend.py` | Синхронный бэкенд для отправки email |
| `task.py` | Celery задачи для асинхронной отправки (опционально) |

## 🗄 Redis

Redis используется для:

- **Хранения черного списка JWT токенов** (logout)
- **Кэширования данных** (при необходимости)

## 🚦 Пагинация
Все эндпоинты, возвращающие списки, поддерживают пагинацию через параметры:

- **page - номер страницы (по умолчанию 1)**

- **page_size - размер страницы (по умолчанию 10)**

## 🔒 Безопасность
- **Пароли хэшируются с использованием sha256_crypt (в security.py)**

- **JWT токены имеют ограниченное время жизни (по умолчанию 15 минут)**

- **Токены могут быть отозваны через blacklist в Redis**

- **Поддержка CORS (при необходимости)**

- **Валидация всех входных данных через Pydantic**

- **Защита от SQL инъекций через SQLAlchemy ORM**

- **Напиши кодом в markdown**
