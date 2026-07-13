from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .extensions import db
from .models import Submission, Mission, User
bp=Blueprint("mentor",__name__,url_prefix="/mentor")
def only_mentor(): return current_user.role=="mentor"
@bp.route("/")
@login_required
def dashboard():
    if not only_mentor(): return redirect(url_for("main.dashboard"))
    subs=Submission.query.order_by(Submission.submitted_at.desc()).all(); total=Mission.query.count(); approved=Submission.query.filter_by(status="approved").count()
    return render_template("mentor.html", submissions=subs,total=total,approved=approved,student=User.query.filter_by(role="student").first())
@bp.route("/review/<int:submission_id>",methods=["POST"])
@login_required
def review(submission_id):
    if not only_mentor(): return redirect(url_for("main.dashboard"))
    sub=db.get_or_404(Submission,submission_id); action=request.form["action"]; sub.mentor_feedback=request.form.get("feedback","")
    if action=="approve" and sub.status!="approved":
        sub.status="approved"; reward=sub.mission.xp_reward + (25 if not sub.is_late else 0); sub.awarded_xp += reward; sub.student.xp += reward
        from .main import award_achievement
        # award_achievement depends on current user, so save first and grant via direct records below
        from .models import Achievement, UserAchievement
        ach=Achievement.query.filter_by(title="First Approved Project").first()
        if ach and not UserAchievement.query.filter_by(user_id=sub.student.id,achievement_id=ach.id).first(): db.session.add(UserAchievement(user_id=sub.student.id,achievement_id=ach.id))
        flash(f"Approved {sub.mission.title} and awarded {reward} XP.","success")
    elif action=="reject": sub.status="rejected"; flash("Submission returned for improvements.","success")
    db.session.commit(); return redirect(url_for("mentor.dashboard"))
