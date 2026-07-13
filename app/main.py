import os, random
from datetime import datetime, timedelta
from urllib.parse import urlparse
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .extensions import db
from .models import Mission, Submission, Achievement, UserAchievement, BonusProject, User
bp = Blueprint("main", __name__)
RANKS = [(0,"Beginner Developer","<i class='fas fa-seedling'></i>"),(100,"Junior Coder","<i class='fas fa-keyboard'></i>"),(250,"Python Explorer","<i class='fab fa-python'></i>"),(450,"Software Apprentice","<i class='fas fa-flask'></i>"),(700,"Junior Software Engineer","<i class='fas fa-gear'></i>"),(900,"Portfolio Builder","<i class='fas fa-building'></i>"),(1000,"CodeQuest Graduate","<i class='fas fa-graduation-cap'></i>")]
BONUSES = ["Calculator","Password Generator","Dice Roller","Hangman","Expense Tracker","Typing Speed Test","Rock Paper Scissors Game","Coin Flip Simulator","ASCII Art Generator","To-Do List with File Saving"]
def rank(xp): return max((r for r in RANKS if xp >= r[0]), key=lambda r:r[0])
def due_for(mission):
    """Deadlines are anchored to the student's first day in the academy."""
    return current_user.joined_at + timedelta(days=mission.day_due)
def approved_ids(): return {s.mission_id for s in Submission.query.filter_by(user_id=current_user.id,status="approved").all()}
def unlocked(m): return m.position == 1 or (m.position-1) in approved_ids()
def award_achievement(title):
    ach = Achievement.query.filter_by(title=title).first()
    if ach and not UserAchievement.query.filter_by(user_id=current_user.id,achievement_id=ach.id).first():
        db.session.add(UserAchievement(user_id=current_user.id,achievement_id=ach.id)); flash(f"Achievement earned: {ach.icon} {title}!", "success")

@bp.route("/")
def index(): return redirect(url_for("main.dashboard") if current_user.is_authenticated else url_for("auth.login"))

@bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == "mentor": return redirect(url_for("mentor.dashboard"))
    missions = Mission.query.order_by(Mission.position).all(); subs = {s.mission_id:s for s in Submission.query.filter_by(user_id=current_user.id).all()}
    current = next((m for m in missions if m.id not in approved_ids()), missions[-1])
    completed = len(approved_ids()); next_rank = next((r for r in RANKS if r[0] > current_user.xp), RANKS[-1])
    achievements = UserAchievement.query.filter_by(user_id=current_user.id).order_by(UserAchievement.earned_at.desc()).all()
    return render_template("dashboard.html", missions=missions, submissions=subs, current=current, completed=completed, rank=rank(current_user.xp), next_rank=next_rank, achievements=achievements, due=due_for(current), unlocked=unlocked)

@bp.route("/missions")
@login_required
def missions():
    subs={s.mission_id:s for s in Submission.query.filter_by(user_id=current_user.id).all()}
    return render_template("missions.html", missions=Mission.query.order_by(Mission.position).all(), submissions=subs, unlocked=unlocked)

@bp.route("/missions/<int:mission_id>", methods=["GET","POST"])
@login_required
def mission(mission_id):
    mission = db.get_or_404(Mission, mission_id)
    if not unlocked(mission): flash("Complete the previous approved mission to unlock this quest.", "error"); return redirect(url_for("main.missions"))
    submission=Submission.query.filter_by(user_id=current_user.id,mission_id=mission.id).first()
    if request.method == "POST":
        url=request.form["github_url"].strip()
        if not urlparse(url).scheme or "github.com" not in url: flash("Please enter a valid GitHub repository URL.", "error"); return redirect(request.url)
        filename=None; upload=request.files.get("screenshot")
        if upload and upload.filename:
            filename=f"{current_user.id}_{mission.id}_{secure_filename(upload.filename)}"; upload.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
        if not submission:
            submission=Submission(user_id=current_user.id,mission_id=mission.id,github_url=url,reflection=request.form["reflection"],screenshot=filename,is_late=datetime.utcnow() > due_for(mission),awarded_xp=10)
            current_user.xp += 10; award_achievement("First Commit"); award_achievement("First Repository"); award_achievement("First README")
        else:
            submission.github_url=url; submission.reflection=request.form["reflection"]; submission.screenshot=filename or submission.screenshot; submission.status="submitted"
        db.session.commit(); flash("Mission submitted! Your mentor will review it soon.", "success"); return redirect(url_for("main.dashboard"))
    return render_template("mission.html", mission=mission, submission=submission, due=due_for(mission))

@bp.route("/bonus", methods=["GET","POST"])
@login_required
def bonus():
    eligible=any(s.status=="approved" and not s.is_late for s in Submission.query.filter_by(user_id=current_user.id).all())
    bonus=BonusProject.query.filter_by(user_id=current_user.id).order_by(BonusProject.id.desc()).first()
    if request.method=="POST" and eligible and request.form.get("won")=="true":
        if not bonus: bonus=BonusProject(user_id=current_user.id,title=random.choice(BONUSES)); db.session.add(bonus); db.session.commit(); flash(f"Bonus unlocked: {bonus.title}!", "success")
    return render_template("bonus.html", eligible=eligible, bonus=bonus)

@bp.route("/portfolio", methods=["GET","POST"])
@login_required
def portfolio():
    if request.method=="POST":
        current_user.bio=request.form["bio"]; current_user.contact=request.form["contact"]; current_user.profile_color=request.form["profile_color"]; db.session.commit(); flash("Portfolio style saved.", "success")
    projects=Submission.query.filter_by(user_id=current_user.id,status="approved").all()
    return render_template("portfolio.html", projects=projects, editable=True)

@bp.route("/portfolio/<int:user_id>")
def public_portfolio(user_id):
    user=db.get_or_404(User,user_id); projects=Submission.query.filter_by(user_id=user_id,status="approved").all()
    return render_template("portfolio.html", projects=projects, profile=user, editable=False)

@bp.route("/graduation")
@login_required
def graduation():
    done=len(approved_ids()) == 6
    if done: award_achievement("Portfolio Complete"); award_achievement("CodeQuest Graduate"); db.session.commit()
    return render_template("graduation.html", done=done, rank=rank(current_user.xp), projects=Submission.query.filter_by(user_id=current_user.id,status="approved").all())
