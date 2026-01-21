# Task Tracker - Telegram Bot with Web App

A comprehensive task management system built with Telegram Bot and Mini App integration. Users can manage their tasks both through Telegram bot commands and a beautiful web interface.

## 🌟 Features

- **Telegram Bot Integration**: Interact with your tasks directly through Telegram
  - `/start` - Get started and access the web app
  - `/mytasks` - View your tasks summary
  - `/addtask` - Quickly add a new task via bot
  - Inline buttons for task management

- **Web App Interface**: Full-featured task manager with:
  - Create, update, and delete tasks
  - Set task priorities (Low, Medium, High)
  - Track task status (To Do, In Progress, Done)
  - Set deadlines for tasks
  - Real-time statistics dashboard
  - Responsive design with Telegram theme integration

- **Robust Architecture**:
  - Async/await throughout the codebase
  - Type hints for Python code
  - Proper error handling and logging
  - Database migrations with Alembic
  - Docker Compose for easy deployment

## 🛠 Tech Stack

### Backend
- **Bot**: [aiogram 3.3+](https://docs.aiogram.dev/) - Modern Telegram Bot framework
- **API**: [FastAPI 0.108+](https://fastapi.tiangolo.com/) - High-performance async web framework
- **Database**: PostgreSQL 15 with SQLAlchemy 2.0 ORM
- **Cache**: Redis 7 for sessions and queues
- **Migrations**: Alembic for database version control

### Frontend
- **Framework**: React 18 with Vite
- **SDK**: [@twa-dev/sdk](https://github.com/twa-dev/sdk) - Telegram Mini App SDK
- **HTTP Client**: Axios for API communication
- **Styling**: Custom CSS with Telegram theme integration

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx as reverse proxy
- **Bot Mode**: Polling for local development, webhook support for production

## 📋 Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- (Optional) ngrok for local WebApp testing
- (Production only) Domain name with SSL certificate

## 🏠 Local Development (Polling Mode)

The project is configured for local development using **polling mode** instead of webhooks.

### Quick Start

1. **Clone the Repository**
```bash
git clone https://github.com/ThreadsofDaemonS/TelegramBotWithWebApp.git
cd TelegramBotWithWebApp
```

2. **Configure Environment Variables**
```bash
cp .env.example .env
```

Edit `.env` file with your configuration:
```env
# Required: Get this from @BotFather
BOT_TOKEN=your_bot_token_here

# WebApp URL (use localhost for initial setup)
WEBAPP_URL=http://localhost

# Database credentials (you can keep defaults for development)
POSTGRES_USER=taskbot
POSTGRES_PASSWORD=changeme
POSTGRES_DB=tasktracker
```

3. **Start the Services**
```bash
docker-compose up -d --build
```

This will start all services:
- PostgreSQL database
- Redis cache
- Bot service (polling mode)
- API service (FastAPI)
- Frontend service (React)
- Nginx reverse proxy

4. **Run Database Migrations**
```bash
docker-compose exec api alembic upgrade head
```

5. **Test Your Bot**
- Open Telegram and search for your bot
- Send `/start` command
- You'll see a welcome message with keyboard buttons!

### Testing WebApp Locally

Since Telegram WebApp requires HTTPS and public URL, use **ngrok** for testing:

```bash
# Install ngrok: https://ngrok.com

# Run ngrok
ngrok http 80

# Copy the https URL (e.g., https://abc123.ngrok.io)
# Update .env: WEBAPP_URL=https://abc123.ngrok.io

# Restart bot
docker-compose restart bot
```

Now the blue WebApp buttons will work!

### WebApp Buttons

The bot has **two ways** to open the WebApp:

1. **Menu Button** - Blue "Открыть" button in chat header (configured automatically)
2. **Keyboard Button** - "📱 Открыть Task Tracker" button at bottom of chat

Both are configured automatically on bot startup.

### Additional Keyboard Buttons

The reply keyboard also includes quick action buttons:
- **📋 Мои задачи** - View your tasks summary
- **📊 Статистика** - See your task statistics
- **ℹ️ Помощь** - Get help and command list

## 🚀 Production Deployment (Webhook Mode)

For production deployment with webhook:

### 1. Clone the Repository

```bash
git clone https://github.com/ThreadsofDaemonS/TelegramBotWithWebApp.git
cd TelegramBotWithWebApp
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` file with your production configuration:

```env
# Required: Get this from @BotFather
BOT_TOKEN=your_bot_token_here

# Required: Your domain URL for WebApp
WEBAPP_URL=https://yourdomain.com

# Database credentials
POSTGRES_USER=taskbot
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=tasktracker

# Frontend URL (used for CORS)
FRONTEND_URL=https://yourdomain.com

# Generate a secure secret key for production
SECRET_KEY=your-secure-secret-key-here
```

**Note:** For production, you'll need to modify `backend/bot/main.py` to use webhook mode instead of polling, and uncomment the webhook router in `backend/api/main.py`.

### 3. Start the Services

```bash
docker-compose up -d --build
```

This will start all services:
- PostgreSQL database
- Redis cache
- Bot service (polling mode for local, webhook for production)
- API service (FastAPI)
- Frontend service (React)
- Nginx reverse proxy

### 4. Run Database Migrations

```bash
docker-compose exec api alembic upgrade head
```

### 5. Open Your Bot

1. Open Telegram and search for your bot
2. Send `/start` command
3. Click "Open Task Manager" or use the Menu/Keyboard buttons to launch the web app
4. Start creating and managing tasks!

## 🔧 Development

### Bot Commands

- `/start` - Initialize bot and show welcome message with keyboard
- `/mytasks` - View your tasks summary
- `/addtask` - Quickly add a new task via bot
- `/stats` - View your task statistics (alias: "📊 Статистика" button)
- `/help` - Get help information (alias: "ℹ️ Помощь" button)

### Local Development Without Docker

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql+asyncpg://taskbot:changeme@localhost:5432/tasktracker"
export BOT_TOKEN="your_token"
export WEBAPP_URL="http://localhost"

# Run API
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Run Bot (in another terminal)
python -m bot.main
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 📁 Project Structure

```
TelegramBotWithWebApp/
├── docker-compose.yml          # Docker services configuration
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
│
├── backend/                   # Backend services
│   ├── Dockerfile            # Backend container configuration
│   ├── requirements.txt      # Python dependencies
│   ├── alembic.ini          # Alembic configuration
│   │
│   ├── bot/                 # Telegram Bot (aiogram3)
│   │   ├── main.py         # Bot entry point
│   │   ├── config.py       # Bot configuration
│   │   ├── handlers/       # Command handlers
│   │   │   ├── start.py    # /start command
│   │   │   └── tasks.py    # Task-related commands
│   │   ├── keyboards/      # Inline keyboards
│   │   │   └── inline.py   # Keyboard builders
│   │   └── middlewares/    # Bot middlewares
│   │       └── database.py # Database session middleware
│   │
│   ├── api/                # FastAPI application
│   │   ├── main.py        # API entry point
│   │   ├── config.py      # API configuration
│   │   ├── auth.py        # Telegram Web App authentication
│   │   ├── dependencies.py # Dependency injection
│   │   └── routers/       # API endpoints
│   │       ├── webhook.py  # Webhook handler
│   │       └── tasks.py    # Tasks CRUD operations
│   │
│   ├── database/          # Database layer
│   │   ├── models.py     # SQLAlchemy models (User, Task)
│   │   ├── database.py   # Database connection
│   │   └── migrations/   # Alembic migrations
│   │       └── env.py    # Migration environment
│   │
│   └── shared/           # Shared code
│       └── schemas.py    # Pydantic schemas
│
├── frontend/             # React Web App
│   ├── Dockerfile       # Frontend container (multi-stage build)
│   ├── package.json     # npm dependencies
│   ├── vite.config.js   # Vite configuration
│   ├── index.html       # HTML entry point
│   └── src/
│       ├── main.jsx     # React entry point
│       ├── App.jsx      # Main application component
│       ├── components/  # React components
│       │   ├── TaskList.jsx    # Task list view
│       │   ├── TaskItem.jsx    # Single task card
│       │   └── AddTask.jsx     # Task creation modal
│       ├── services/    # API client
│       │   └── api.js   # Axios instance and API methods
│       └── styles/      # CSS styles
│           └── App.css  # Application styles
│
└── nginx/               # Nginx reverse proxy
    ├── Dockerfile      # Nginx container
    └── nginx.conf      # Nginx configuration
```

## 🔧 Development

### Local Development Without Docker

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql+asyncpg://user:pass@localhost:5432/db"
export BOT_TOKEN="your_token"

# Run API
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Run Bot (in another terminal)
python -m bot.main
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Database Migrations

Create a new migration:
```bash
docker-compose exec api alembic revision --autogenerate -m "Description"
```

Apply migrations:
```bash
docker-compose exec api alembic upgrade head
```

Rollback:
```bash
docker-compose exec api alembic downgrade -1
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f bot
docker-compose logs -f api
docker-compose logs -f frontend
```

## 📊 Database Schema

### User Model
```
- id (primary key)
- telegram_id (unique)
- username
- first_name
- last_name
- created_at
```

### Task Model
```
- id (primary key)
- user_id (foreign key → users.id)
- title
- description
- status (todo, in_progress, done)
- priority (low, medium, high)
- deadline (nullable)
- created_at
- updated_at
```

## 🔐 Security

- Telegram Web App authentication using initData validation
- HMAC-SHA256 signature verification
- Secure secret key for production
- PostgreSQL password protection
- Environment variables for sensitive data
- No hardcoded credentials

## 🌐 API Documentation

Once the API is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Main Endpoints

- `POST /webhook` - Telegram webhook handler
- `GET /api/tasks` - List user tasks
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{task_id}` - Update a task
- `DELETE /api/tasks/{task_id}` - Delete a task
- `GET /api/tasks/stats` - Get user statistics

## 🎨 Screenshots

<!-- Add screenshots here after deployment -->

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [aiogram](https://docs.aiogram.dev/) - Telegram Bot framework
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Telegram Mini Apps](https://core.telegram.org/bots/webapps) - Web App platform

## 📧 Support

For support, please open an issue on GitHub or contact the maintainers.

## 🔄 Updates

Check the [CHANGELOG](CHANGELOG.md) for version history and updates.

---

**Happy Task Tracking! 🎉**