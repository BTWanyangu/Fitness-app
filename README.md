# Trainova — Production-ready full-stack fitness coaching app

Trainova is a free, Kenya-ready fitness web application with a Django REST backend, PostgreSQL database, React + TypeScript + Tailwind frontend, JWT auth, admin-managed exercises/reference media, progress tracking, and a MediaPipe-ready pose scoring engine.

## What is inside

### Frontend
- React + TypeScript + Tailwind CSS
- Component-based architecture: landing, layout, dashboard, forms, auth, and UI components are split cleanly
- Responsive landing page with green/orange brand styling, sticky header, rich sections, and footer
- Public navigation without a login wall for demo browsing
- Auth page for sign in / sign up
- Dashboard, exercises, form analysis, progress, profile, and admin entry pages
- API interceptor automatically attaches JWT access token

### Backend
- Django 5 + Django REST Framework
- PostgreSQL via Docker Compose
- JWT authentication with SimpleJWT
- User registration/login/profile endpoints
- Fitness profile fields: age, gender, location, height, weight, target weight, goal, training level, weekly target, equipment, injury notes, readiness
- Exercise library, workout plans, workout sessions, recommendations, progress metrics
- Django Admin control panel for users, exercises, angle standards, reference images/videos, user uploads, progress and recommendations
- MediaPipe Pose Landmarker scoring engine with safe fallback mode

## Pose scoring engine

The engine supports:
1. Upload user image/video.
2. Extract representative frame from video or use uploaded image.
3. Detect body landmarks using MediaPipe Pose Landmarker.
4. Evaluate configured angle standards per exercise.
5. Compare user pose against admin-approved reference media when reference landmarks exist.
6. Return score, feedback, angle results, detected landmarks, and overlay coordinates.




## Run with Docker


docker compose down -v
docker compose up --build

Docker notes:
- The Postgres container is **not exposed on localhost:5432**, so it will not conflict with your local PostgreSQL.
- Backend waits for DB health before running migrations and seed data.
- Uploaded media is persisted in Docker volume `media_data`.

## Run manually

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_initial_data
python manage.py runserver 0.0.0.0:8000
```

For manual local Postgres, set `DB_HOST=localhost` in `.env`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Environment


