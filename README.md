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
- **Webhook**: Direct webhook integration (no polling)

## 📋 Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Domain name with SSL certificate (for production)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/ThreadsofDaemonS/TelegramBotWithWebApp.git
cd TelegramBotWithWebApp
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` file with your configuration:

```env
# Required: Get this from @BotFather
BOT_TOKEN=your_bot_token_here

# Required: Your domain URL for webhook
WEBHOOK_URL=https://yourdomain.com/webhook

# Database credentials (you can keep defaults for development)
POSTGRES_USER=taskbot
POSTGRES_PASSWORD=changeme
POSTGRES_DB=tasktracker

# Optional: Frontend URL (used for CORS and web app button)
FRONTEND_URL=https://yourdomain.com

# Optional: Generate a secure secret key for production
SECRET_KEY=your-secret-key-here
```

### 3. Start the Services

```bash
docker-compose up -d
```

This will start all services:
- PostgreSQL database
- Redis cache
- Bot service
- API service
- Frontend service
- Nginx reverse proxy

### 4. Run Database Migrations

```bash
docker-compose exec api alembic upgrade head
```

### 5. Set Up Webhook

The webhook is automatically configured when the bot starts. To manually set it:

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<YOUR_WEBHOOK_URL>"
```

### 6. Test Your Bot

1. Open Telegram and search for your bot
2. Send `/start` command
3. Click "Open Task Manager" to launch the web app
4. Start creating and managing tasks!

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