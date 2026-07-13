import os
from flask import Flask
from .extensions import db, login_manager, migrate

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(os.path.join(app.root_path, "static", "uploads"), exist_ok=True)
    
    # Database path
    db_path = os.path.join(app.instance_path, "codequest.db")
    
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-change-me"),
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        MAX_STUDENTS=2,
        ALLOWED_STUDENT_EMAILS=[
            "arinola.olayiwola@gmail.com",
            "niniolayiwola12@gmail.com"
        ],
        UPLOAD_FOLDER=os.path.join(app.root_path, "static", "uploads"),
    )
    db.init_app(app); login_manager.init_app(app); migrate.init_app(app, db)
    from .auth import bp as auth_bp
    from .main import bp as main_bp
    from .mentor import bp as mentor_bp
    app.register_blueprint(auth_bp); app.register_blueprint(main_bp); app.register_blueprint(mentor_bp)
    with app.app_context(): db.create_all()
    return app
