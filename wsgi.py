import os
import sys

# Add the app directory to the path
app_dir = os.path.dirname(__file__)
sys.path.insert(0, app_dir)

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
