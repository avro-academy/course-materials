SHIFT SWAP
Avro Academy · Docker Basics: Containers for Your Apps

Shift Swap is a small web app where staff at Corner Café post shifts they
can't work, and teammates take them. It's Python (Flask) with logins, a
database and a small JSON API at /api/shifts. Over the course you put it in
Docker, step by step.

FOLDERS
  start               The app with no Docker files yet. Copy this folder
                      somewhere easy, rename it shift-swap, and work in it.
  step-1-dockerfile   The finished files after Module 2 (Dockerfile, .dockerignore)
  step-2-data         ...after Module 3 (the database in /data, for a volume)
  step-3-production   ...after Module 4 (gunicorn, non-root user, health check)
  step-4-compose      ...after Module 5 (Docker Compose with PostgreSQL)

If you get stuck, compare your files with the matching step folder.

YOU NEED
  Docker Desktop (docker.com/products/docker-desktop), free for personal use
  and learning. You don't need Python on your computer: it runs in Docker.

QUICK START (Module 2, in your shift-swap folder)
  docker build -t shift-swap .
  docker run -d --name shift-swap -p 5000:5000 shift-swap
  docker exec shift-swap flask --app app init-db
  Open http://localhost:5000
  (On a Mac, AirPlay Receiver uses port 5000: use -p 5050:5000 and open
  http://localhost:5050 instead.)

WITH COMPOSE (Module 5, step-4-compose)
  Copy .env.example to .env and change both values to long random strings.
  docker compose up -d --build
  docker compose run --rm web flask --app app init-db
  docker compose down       (your data stays in the db-data volume)

RUN THE TESTS (17 tests, using SQLite)
  docker run --rm shift-swap python -m pytest

FILES IN THE APP
  app.py              the Flask app: pages, logins, the /api/shifts API
  schema.sql          the tables (users and shifts) for SQLite
  templates/, static/ the pages, styles and the little bit of JavaScript
  tests/              the tests
  requirements.txt    the Python packages
  db.py, schema-postgres.sql   (step-4-compose) PostgreSQL support

Never put a real .env file, or a real password, in an image or on GitHub.
