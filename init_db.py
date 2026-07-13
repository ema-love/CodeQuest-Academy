#!/usr/bin/env python
"""
Initialize database for CodeQuest Academy
Run this after deploying to production to set up initial data
"""

import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.extensions import db
from app.seed import seed_data

if __name__ == "__main__":
    print("🎮 CodeQuest Academy - Database Initialization")
    print("-" * 50)
    
    app = create_app()
    
    with app.app_context():
        print("✓ Creating database tables...")
        db.create_all()
        
        print("✓ Seeding initial data...")
        seed_data()
        
        print("\n✅ Database initialized successfully!")
        print("\n📧 Test Credentials:")
        print("   Student Email 1: arinola.olayiwola@gmail.com")
        print("   Student Email 2: niniolayiwola12@gmail.com")
        print("   Student Password: quest1234")
        print(f"\n👨‍🏫 Mentor Email: {os.environ.get('MENTOR_EMAIL', 'mentor@codequest.local')}")
        print("   (Set MENTOR_PASSWORD in environment variables)")
        print("\n🚀 Your app is ready to go!")
