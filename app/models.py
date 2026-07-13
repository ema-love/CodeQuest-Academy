from datetime import datetime
from flask_login import UserMixin
from .extensions import db, login_manager

class User(UserMixin, db.Model):
    # SQLite permits multiple NULL values in a unique index, so this permits many
    # students while ensuring only one row can have the mentor role.
    __table_args__ = (
        db.Index("one_mentor_account", "role", unique=True,
                 sqlite_where=db.text("role = 'mentor'")),
    )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="student", nullable=False)
    xp = db.Column(db.Integer, default=0)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    streak = db.Column(db.Integer, default=0)
    bio = db.Column(db.Text, default="Future software engineer on a quest!")
    contact = db.Column(db.String(120), default="")
    profile_color = db.Column(db.String(7), default="#16A34A")
    avatar = db.Column(db.String(255), default="")
    submissions = db.relationship("Submission", backref="student", lazy=True)

class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    objectives = db.Column(db.Text, default="")
    resources = db.Column(db.Text, default="")
    difficulty = db.Column(db.String(30), default="Beginner")
    estimated_time = db.Column(db.String(40), default="2–4 hours")
    day_due = db.Column(db.Integer, nullable=False)
    xp_reward = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=False)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    mission_id = db.Column(db.Integer, db.ForeignKey("mission.id"), nullable=False)
    github_url = db.Column(db.String(300), nullable=False)
    reflection = db.Column(db.Text, nullable=False)
    screenshot = db.Column(db.String(255))
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="submitted")
    is_late = db.Column(db.Boolean, default=False)
    mentor_feedback = db.Column(db.Text, default="")
    awarded_xp = db.Column(db.Integer, default=0)
    mission = db.relationship("Mission", backref="submissions")

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    icon = db.Column(db.String(50), default="<i class='fas fa-medal'></i>")
    description = db.Column(db.String(255), default="")

class UserAchievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    achievement_id = db.Column(db.Integer, db.ForeignKey("achievement.id"))
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    achievement = db.relationship("Achievement")

class BonusProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default="unlocked")
    xp_reward = db.Column(db.Integer, default=50)

@login_manager.user_loader
def load_user(user_id): return db.session.get(User, int(user_id))
