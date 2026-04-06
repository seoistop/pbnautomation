# PBN Automation Toolkit

This project automates backlink insertion on WordPress sites using Flatsome UX Blocks.

## Overview

- **Frontend**: Static dashboard (vanilla JS) deployable to GitHub Pages
- **Backend**: FastAPI application deployable to Railway
- **Database**: SQLite by default (can be swapped for Postgres when deploying)

## Features

- Manage PBN site credentials (domain, username, application password, UX Block/Post ID)
- Queue backlink tasks (URL + anchor)
- Trigger WordPress REST API calls that append HTML snippets to the configured UX Block (footer)
- View activity log/status per task

## Structure

```
pbn_automation/
  frontend/
    index.html
    assets/
      app.js
      styles.css
  backend/
    app/
      main.py
      config.py
      database.py
      models.py
      schemas.py
      routers/
        sites.py
        tasks.py
      services/
        wordpress.py
        google_sheet.py
    requirements.txt
    .env.example
  README.md
  .gitignore
```

## Running locally

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

Use any static server (or open `index.html` directly). For development:
```bash
cd frontend
python -m http.server 5173
```
Then open `http://localhost:5173` and configure API URL in `frontend/assets/app.js` (default `http://localhost:8000`).

## Deployment

1. Push this repo to GitHub.
2. **Frontend**: enable GitHub Pages for the `frontend` folder (or build pipeline of your choice).
3. **Backend**: create a Python service on Railway pointing to `backend/`, set environment variables per `.env.example`, and run migrations if you switch to Postgres.
4. Update the frontend `API_BASE_URL` to point at the Railway domain.

## Notes

- Application Passwords should be generated per site at `/wp-admin/profile.php` and stored securely. The backend encrypts them at rest using Fernet.
- Google Sheet sync is optional; provide `GOOGLE_SERVICE_ACCOUNT_JSON` + `GOOGLE_SHEET_ID` envs if you want to auto-import.
- For production, consider a job queue (e.g., RQ/BullMQ) if you process hundreds of sites concurrently.
