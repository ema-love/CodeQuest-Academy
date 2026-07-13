from app import create_app
from app.extensions import db
from app.seed import seed_data

app = create_app()

@app.cli.command("seed")
def seed():
    """Create sample users, missions, and achievements."""
    with app.app_context():
        db.create_all()
        seed_data()
        print("CodeQuest sample data is ready.")

if __name__ == "__main__":
    app.run(debug=True)
