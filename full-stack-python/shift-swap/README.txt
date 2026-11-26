SHIFT SWAP BOARD: starter files
Avro Academy · Full-Stack Python: Build a Web App with Flask

Staff post shifts they can't work, and teammates take them with one click.
Each folder is the app at the end of one part of the course, so you can
compare your code or jump ahead if you get stuck.

  step-1-hello       Module 2  Your first routes
  step-2-templates   Module 2  Jinja templates, a shared layout and CSS
  step-3-forms       Module 3  A form, checking input, flash messages
  step-4-database    Module 4  Saving shifts in SQLite (init-db command)
  step-5-users       Module 5  Sign up, log in, owner-only delete, taking shifts
  step-6-final       Modules 6-8  CSRF tokens, safe redirects, JSON API,
                     JavaScript fetch and 17 automated tests

GET STARTED (Module 1, "Setting up")
  1. Open this shift-swap folder in VS Code and open a terminal.
  2. Make a virtual environment and turn it on:
       Windows:      py -m venv .venv      then  .venv\Scripts\activate
       Mac / Linux:  python3 -m venv .venv then  source .venv/bin/activate
  3. pip install -r requirements.txt
  4. cd step-1-hello
     flask --app app run --debug
  5. Open http://127.0.0.1:5000   (Ctrl + C stops the server)

STEPS 4, 5 AND 6 USE A DATABASE
  Run this once in the step's folder before you start it (and again whenever
  schema.sql changes. It deletes everything in the database):
       flask --app app init-db

RUN THE TESTS (Module 8)
  cd step-6-final
  pip install -r requirements.txt
  python -m pytest          -> 17 passed

Never use the dev SECRET_KEY or debug mode on a real public website.
