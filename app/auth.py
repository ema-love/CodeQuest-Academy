from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from .extensions import db
from .models import User
bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated: return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"].lower()).first()
        if user and check_password_hash(user.password_hash, request.form["password"]):
            login_user(user); return redirect(url_for("mentor.dashboard") if user.role == "mentor" else url_for("main.dashboard"))
        flash("Those login details don't match our records.", "error")
    student_slots = current_app.config["MAX_STUDENTS"] - User.query.filter_by(role="student").count()
    return render_template("login.html", student_slots=max(0, student_slots))

@bp.route("/register", methods=["POST"])
def register():
    email = request.form["email"].lower()
    password = request.form["password"]
    allowed_emails = [e.lower() for e in current_app.config["ALLOWED_STUDENT_EMAILS"]]
    
    if email not in allowed_emails:
        flash("That email is not authorized to register. Contact your mentor.", "error")
    elif password != "quest1234":
        flash("Invalid registration password. Please contact your mentor.", "error")
    elif User.query.filter_by(role="student").count() >= current_app.config["MAX_STUDENTS"]:
        flash("The academy already has its two student accounts. Ask the mentor for help.", "error")
    elif User.query.filter_by(email=email).first(): 
        flash("That email already has an account.", "error")
    else:
        db.session.add(User(name=request.form["name"],email=email,password_hash=generate_password_hash(password, method="pbkdf2:sha256")))
        db.session.commit(); flash("Your quest has begun! Log in to continue.", "success")
    return redirect(url_for("auth.login"))

@bp.route("/logout")
def logout(): logout_user(); return redirect(url_for("auth.login"))
