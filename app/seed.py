import os
from werkzeug.security import generate_password_hash
from .extensions import db
from .models import User, Mission, Achievement

MISSIONS = [
("Task Manager", "Build a tidy task manager that makes daily work feel conquerable.", "Add Task|Delete Task|Complete Task|View Tasks", 3, 100),
("Quiz Game", "Create an interactive quiz with questions, scoring, and a finish screen.", "Question bank|Score tracker|Results screen", 5, 100),
("Number Guessing Game", "Make a game where players find a secret number with helpful hints.", "Random number|Hints|Play again", 7, 100),
("Restaurant Ordering System", "Build a menu and ordering experience for a fictional restaurant.", "Menu display|Cart|Order total", 10, 150),
("Student Grade Calculator", "Turn scores into useful grade summaries and averages.", "Score input|Average|Letter grade", 14, 150),
("Portfolio Website", "Publish a personal developer portfolio that presents your best work.", "About section|Project cards|Contact section", 21, 300),]
ACHIEVEMENTS = [("First Commit", "<i class='fas fa-floppy-disk'></i>", "Made your first move."),("First Repository", "<i class='fas fa-box'></i>", "Shared a project repository."),("First README", "<i class='fas fa-book'></i>", "Documented your work."),("First Approved Project", "<i class='fas fa-circle-check'></i>", "Earned mentor approval."),("Five Day Streak", "<i class='fas fa-fire'></i>", "Showed up five days in a row."),("Portfolio Complete", "<i class='fas fa-palette'></i>", "Built a portfolio."),("CodeQuest Graduate", "<i class='fas fa-graduation-cap'></i>", "Completed the full quest.")]
def seed_data():
    # Students create their own accounts. The mentor is provisioned once through
    # environment variables, so the public registration form can never create one.
    mentor_email = os.environ.get("MENTOR_EMAIL", "mentor@codequest.local").lower()
    if not User.query.filter_by(role="mentor").first():
        db.session.add(User(name=os.environ.get("MENTOR_NAME", "Mentor"), email=mentor_email,
                            password_hash=generate_password_hash(os.environ.get("MENTOR_PASSWORD", "mentor123"), method="pbkdf2:sha256"), role="mentor"))
    if not Mission.query.first():
        for i, (title, desc, objs, day, xp) in enumerate(MISSIONS, 1): db.session.add(Mission(title=title,description=desc,objectives=objs,resources="MDN Web Docs|freeCodeCamp|Python Docs",difficulty="Beginner" if i<4 else "Intermediate",estimated_time="2–4 hours" if i<4 else "4–6 hours",day_due=day,xp_reward=xp,position=i))
    if not Achievement.query.first():
        for title, icon, desc in ACHIEVEMENTS: db.session.add(Achievement(title=title,icon=icon,description=desc))
    db.session.commit()
