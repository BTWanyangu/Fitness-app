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

Your model file is already expected here:

```text
backend/trainova/pose_models/pose_landmarker.task
```

Environment path:

```env
MEDIAPIPE_POSE_MODEL_PATH=/app/trainova/pose_models/pose_landmarker.task
```

Check engine status after running:

```text
http://localhost:8000/api/pose/status/
```

If the model is missing or the image/video is unclear, the API still returns safe fallback coaching instead of crashing.

## Demo credentials

Seed command creates:

```text
Django Admin: http://localhost:8000/admin/
Admin username: admin
Admin password: admin12345

Demo user email: alex@example.com
Demo user password: password12345
```

## Run with Docker

From the project root:

```bash
cp .env.example .env

docker compose down -v
docker compose up --build
```

Open:

```text
Frontend: http://localhost:5173
Backend health: http://localhost:8000/api/health/
Pose status: http://localhost:8000/api/pose/status/
Django Admin: http://localhost:8000/admin/
```

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

Use this in `.env`:

```env
POSTGRES_DB=trainova
POSTGRES_USER=trainova
POSTGRES_PASSWORD=trainova
DB_NAME=trainova
DB_USER=trainova
DB_PASSWORD=trainova
DB_HOST=db
DB_PORT=5432
DJANGO_SECRET_KEY=replace-this-in-production
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DJANGO_CORS_ALLOWED_ORIGINS=http://localhost:5173
VITE_API_URL=http://localhost:8000/api
VITE_MEDIA_URL=http://localhost:8000
MEDIAPIPE_POSE_MODEL_PATH=/app/trainova/pose_models/pose_landmarker.task
```

## Small placeholders you may change

1. Replace stock image URLs with local Kenyan fitness/gym/home workout images.
2. Upload real correct-form reference images/videos in Django Admin.
3. Add more `ExerciseAngleStandard` records per exercise for better scoring.
4. Replace `DJANGO_SECRET_KEY` before any public deployment.
5. Set `DJANGO_DEBUG=False` in production.
6. Configure cloud storage for media if deploying publicly.
7. Add email/SMS verification if launching for public users.

## Main API endpoints

```text
POST /api/auth/register/
POST /api/auth/login/
GET  /api/auth/me/
PATCH /api/auth/me/
GET  /api/dashboard/
GET  /api/exercises/
POST /api/progress/
POST /api/form-submissions/
GET  /api/pose/status/
```

## Recommended admin workflow

1. Log in to Django Admin.
2. Add or edit exercises.
3. Add angle standards for each exercise using MediaPipe landmark names, for example:
   - `left_shoulder`, `left_elbow`, `left_wrist`
   - `left_hip`, `left_knee`, `left_ankle`
4. Upload correct reference media for exercises.
5. User uploads image/video from Form Analysis page.
6. API scores the upload and stores feedback in `FormSubmission`.

