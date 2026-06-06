# School Telegram Bot System

A complete school communication system with:
- **Telegram Bot** — parents look up homework, holidays, and receive announcements
- **Web Dashboard** — teachers submit homework, admins manage holidays and send broadcasts
- **FastAPI Backend** — REST API connecting everything

---

## Project Structure

```
telegram bot/
├── backend/          ← FastAPI server + SQLite database
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── database.py
│   └── requirements.txt
├── src/              ← Telegram bot (python-telegram-bot)
│   ├── bot_main.py   ← Bot entry point
│   ├── translations.py
│   ├── handlers/     ← Message handlers & button routing
│   │   └── bot_handlers.py
│   └── services/     ← Backend API communication helpers
│       └── api_service.py
├── dashboard/        ← Web dashboard (plain HTML/CSS/JS)
│   ├── index.html
│   ├── style.css
│   └── app.js
├── .env.example      ← Copy to .env and fill in values
└── README.md
```

---

## Quick Start

### 1. Set up environment variables

```bash
copy .env.example .env
```

Edit `.env` and fill in:
- `TELEGRAM_BOT_TOKEN` — get this from [@BotFather](https://t.me/BotFather) on Telegram
- `API_SECRET_KEY` — any long random string (e.g. run `python -c "import secrets; print(secrets.token_hex(32))"`)
- `ADMIN_USERNAME` / `ADMIN_PASSWORD` — your dashboard login credentials

### 2. Start the Backend & Bot
By default, the backend server will automatically run the bot thread. Make sure `RUN_BOT=true` is set in your `.env` file.

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`  
Interactive API docs: `http://localhost:8000/docs`

### 3. Start the Telegram Bot Manually (Alternative)
If you want to run the bot separately from the backend (make sure `RUN_BOT=false` in your `.env`):

Open a second terminal:

```bash
# From project root
pip install python-telegram-bot httpx python-dotenv
python src/bot_main.py
```

### 4. Open the Dashboard

Open `dashboard/index.html` directly in your browser.  
Log in with the credentials you set in `.env`.

---

## User Roles

| Role    | Can do                                                        |
|---------|---------------------------------------------------------------|
| Admin   | Everything: classes, homework, holidays, broadcasts, history  |
| Teacher | Submit and delete homework, view holidays                     |

> To add teacher accounts, extend the `USERS` dict in `backend/auth.py` or add a users table.

---

## Scenarios Covered

| Scenario                        | How it works                                                                 |
|---------------------------------|------------------------------------------------------------------------------|
| Teacher submits homework        | Dashboard → Homework tab → fill form → Submit                                |
| Parent retrieves homework       | Bot → Homework button → type class code → instant reply                      |
| Parent checks holidays          | Bot → Upcoming Holidays button → formatted list                              |
| Admin broadcasts announcement   | Dashboard → Broadcast tab → write message → Send to All Subscribers          |

---

## Deploying to Production

1. **Backend**: Deploy to a VPS or cloud (Railway, Render, Fly.io). Use PostgreSQL instead of SQLite by changing `DATABASE_URL`.
2. **Bot**: Run `src/bot_main.py` as a background service (systemd, PM2, or Docker), or let it spin up automatically via the backend startup thread.
3. **Dashboard**: Host the `dashboard/` folder on any static host (Netlify, GitHub Pages, or serve via Nginx).
4. **CORS**: Update `allow_origins` in `backend/main.py` to your dashboard's domain.
5. **HTTPS**: Always use HTTPS in production. The bot token and JWT tokens must be kept secure.
