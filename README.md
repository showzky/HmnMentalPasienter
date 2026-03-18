# Mental Pasienter

This project has:
- a Vue 3 + Vite frontend in the repository root
- a Flask backend in [Backend/app.py](c:\Users\andre\Documents\LinuxBackup\Website\mental-pasienter\Backend\app.py)
- a local development setup that can use a local MySQL database
- a production setup that can later use Render for the backend, Vercel for the frontend, and Supabase for Postgres

## Local Development

Frontend env:
- copy `.env.development.example` to `.env.development`
- set `VITE_API_URL` to `http://localhost:5000/api`
- set `VITE_SOCKET_URL` to `http://localhost:5000`

Backend env:
- copy `Backend/.env.backend.development.example` to `Backend/.env.backend.development`
- set `DATABASE_URI` to your local MySQL connection string
- keep local-only secrets in this file

Local startup:
1. Start your local MySQL database.
2. Start the Flask backend from `Backend/`.
3. Start the Vite frontend from the repository root.

## Production Shape

Frontend:
- deploy the Vite app to Vercel
- set Vercel env vars based on `.env.production.example`
- keep `.env.production` separate from `.env.development`
- this repo includes [vercel.json](c:\Users\andre\Documents\LinuxBackup\Website\mental-pasienter\vercel.json) so Vue Router routes rewrite to `index.html`

Backend:
- deploy Flask to Render
- set Render env vars based on `Backend/.env.backend.production.example`
- set `DATABASE_URI` to your hosted database connection string
- for Supabase, use the pooled Postgres connection string in production
- set `FLASK_ENV=production` in Render so the backend loads production configuration paths consistently
- this repo includes [render.yaml](c:\Users\andre\Documents\LinuxBackup\Website\mental-pasienter\render.yaml) with a Python web service blueprint
- the Render start command uses Gunicorn with Eventlet for Flask-SocketIO support

Database:
- local development can stay on local MySQL
- production can move to Supabase using a pooled Postgres connection string

## Notes

- Real env files are meant to stay local and should not be committed.
- The backend now requires `DATABASE_URI` to be provided through environment configuration.
- The backend dependencies now include both `mysql-connector-python` for local MySQL development and `psycopg[binary]` for hosted Postgres/Supabase.

## Deploy Checklist

Vercel:
1. Import the repository.
2. Keep the frontend root at the repository root.
3. Set `VITE_API_URL` to your Render backend URL with `/api` appended.
4. Set `VITE_SOCKET_URL` to your Render backend URL without `/api`.

Render:
1. Create a Blueprint deploy from [render.yaml](c:\Users\andre\Documents\LinuxBackup\Website\mental-pasienter\render.yaml) or create a web service manually from `Backend/`.
2. Set `DATABASE_URI` to the Supabase session pooler URI.
3. Set `JWT_SECRET_KEY` and your mail-related environment variables.
4. Deploy and confirm the service starts on Render's assigned `PORT`.
