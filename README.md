# CodeQuest Academy

A 21-day, project-based learning quest for one student, with mentor review, XP, ranks, achievements, and a generated portfolio.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
MENTOR_NAME="Your Name" MENTOR_EMAIL="you@example.com" MENTOR_PASSWORD="choose-a-password" flask --app run.py seed
flask --app run.py run --debug
```

Open `http://127.0.0.1:5000`.

The seed command provisions exactly one mentor account. The login screen allows exactly two student accounts to be created; it never offers a mentor-registration option.

## Database migrations

The app creates its SQLite schema automatically for a quick start. For managed schema changes use:

```bash
flask --app run.py db init
flask --app run.py db migrate -m "schema update"
flask --app run.py db upgrade
```

Uploaded screenshots are stored in `app/static/uploads/` and the SQLite database is `instance/codequest.db`.
