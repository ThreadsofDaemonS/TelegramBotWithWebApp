# Task Tracker - Telegram Bot with Web App

A comprehensive task management system built with Telegram Bot and Mini App integration. Users can manage their tasks both through Telegram bot commands and a beautiful web interface.

## 🌟 Features

- **Telegram Bot Integration**: Interact with your tasks directly through Telegram
  - `/start` - Get started and access the web app
  - `/mytasks` - View your tasks summary
  - `/addtask` - Quickly add a new task via bot
  - Reply keyboard with quick access buttons
  - Menu button (blue button in chat header) for quick app access
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
- **Bot Mode**: Polling mode for local development (webhook support for production)

## 📋 Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- (Optional) ngrok for WebApp testing locally
- (Optional) Domain name with SSL certificate for production webhook mode

## 🚀 Quick Start

For local development, the bot uses **polling mode** instead of webhooks, so no public URL is required!

### 1. Clone the Repository

```bash
git clone https://github.com/ThreadsofDaemonS/TelegramBotWithWebApp.git
cd TelegramBotWithWebApp
```

### 2. Create Bot and Get Token

1. Open Telegram and find [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the instructions
3. Copy the bot token you receive

### 3. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` file with your bot token:

```env
# Required: Get this from @BotFather
BOT_TOKEN=your_bot_token_here

# For local development
WEBAPP_URL=http://localhost

# Database credentials (you can keep defaults for development)
POSTGRES_USER=taskbot
POSTGRES_PASSWORD=changeme
POSTGRES_DB=tasktracker

# Leave other settings as default
```

**For Telegram WebApp to work, also create `frontend/.env`:**

```bash
# Create frontend/.env from example
cp frontend/.env.example frontend/.env
```

This tells the frontend where to send API requests. When using ngrok, update this to your ngrok URL.

### 4. Start the Services

```bash
docker-compose up -d --build
```

This will start all services:
- PostgreSQL database
- Redis cache
- Bot service (polling mode)
- API service
- Frontend service
- Nginx reverse proxy

### 5. Run Database Migrations

```bash
docker-compose exec api alembic upgrade head
```

### 6. Test Your Bot

1. Open Telegram and search for your bot
2. Send `/start` command
3. You'll see a reply keyboard with buttons

### 7. Opening the Web App

To open the Task Tracker Web App:
1. Start the bot with `/start`
2. **Click the blue "Открыть" (Open) button** to the left of the message input field (Menu Button)
3. The Web App will open with proper authentication

**Important:** Use the Menu Button (blue button to the left of the message input field) instead of keyboard buttons to ensure proper Telegram authentication data is passed. This prevents authentication errors when using the Web App.

### 8. Testing WebApp Locally with ngrok

Since Telegram WebApp requires HTTPS, use ngrok for local testing:

```bash
# Install ngrok from https://ngrok.com

# Start ngrok in a separate terminal
ngrok http 80

# Copy the HTTPS URL (e.g., https://abc123.ngrok-free.app)
# Update .env:
WEBAPP_URL=https://abc123.ngrok-free.app
FRONTEND_URL=https://abc123.ngrok-free.app

# IMPORTANT: Also update frontend/.env:
VITE_API_URL=https://abc123.ngrok-free.app

# Rebuild frontend to apply new configuration
docker-compose build --no-cache frontend

# Restart services to apply new URLs
docker-compose up -d
```

**Important Notes:**
- All three URL variables must point to your ngrok URL: `WEBAPP_URL`, `FRONTEND_URL`, and `VITE_API_URL`
- The frontend needs `VITE_API_URL` to know where to send API requests
- Free ngrok URLs change on restart - consider a paid plan for a static domain
- After changing ngrok URL, you must rebuild the frontend container

Now the WebApp button will work! 🎉

## 🧪 Local Development

### Quick Start Commands

```bash
# View logs
docker-compose logs -f bot
docker-compose logs -f api

# Restart services after code changes
docker-compose restart bot
docker-compose restart api

# Rebuild after dependency changes
docker-compose up -d --build

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Development Without Docker

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql+asyncpg://user:pass@localhost:5432/db"
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

## 🔧 Troubleshooting

### WebApp shows "Failed to load tasks"

This usually happens when the frontend is trying to connect to the wrong API URL.

**Check the following:**

1. **Verify environment variables are set correctly:**
   ```bash
   # In .env file:
   WEBAPP_URL=https://your-ngrok-url.ngrok-free.app
   FRONTEND_URL=https://your-ngrok-url.ngrok-free.app
   
   # In frontend/.env file:
   VITE_API_URL=https://your-ngrok-url.ngrok-free.app
   ```
   All three URLs should be identical (your ngrok HTTPS URL).

2. **Check browser console for errors:**
   - Open the WebApp in Telegram
   - Open Telegram Desktop → Right click → Inspect Element → Console
   - Look for error messages with `[API Service]` or `[App]` prefix
   - Check what URL the frontend is connecting to

3. **Common issues:**
   - **401 Unauthorized**: Frontend connecting to wrong URL or missing initData
     - Solution: Verify `VITE_API_URL` is set correctly and rebuild frontend
   - **Mixed content warnings**: HTTPS site connecting to HTTP localhost
     - Solution: Use ngrok URL for all environment variables
   - **CORS errors**: Browser blocking requests
     - Solution: Ensure `FRONTEND_URL` matches the URL Telegram is using

4. **After changing environment variables:**
   ```bash
   # Must rebuild frontend to pick up new VITE_API_URL
   docker-compose build --no-cache frontend
   docker-compose up -d
   ```

5. **Verify initData is present:**
   - Check console for `[App] Telegram WebApp Debug Info`
   - initData should not be empty
   - If empty, you may be opening the app directly in browser instead of through Telegram

### WebApp works in browser but not in Telegram

- The WebApp must be opened from within Telegram to have valid `initData`
- Direct browser access will fail with 401 Unauthorized
- Always test by clicking the WebApp button in your Telegram bot

### ngrok URL changed and WebApp stopped working

Free ngrok URLs change every time you restart ngrok. You need to:

1. Update all three URLs in `.env` and `frontend/.env`
2. Rebuild frontend: `docker-compose build --no-cache frontend`
3. Restart services: `docker-compose up -d`

Consider using ngrok's paid plan for a static domain.

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