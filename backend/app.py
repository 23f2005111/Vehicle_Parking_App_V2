from flask import Flask
from application.config import LocalDevelopementConfig
from application.database import db
from application.models import User
from application.security import jwt
from flask_cors import CORS
from application.celery_init import celery_init_app
from celery.schedules import crontab
from application.cache_config import init_cache
import os

app = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopementConfig)
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    init_cache(app)
    app.app_context().push()

    # Create tables and admin user (only if they don't exist)
    try:
        db.create_all()
        
        # Check if admin exists, if not create it
        admin = User.query.filter_by(email="admin@gmail.com").first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@gmail.com",
                password="1234",
                role="admin",
                address="Mumbai",
                pincode="400001"
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created")
    except Exception as e:
        print(f"Database setup: {e}")
    
    return app

app = create_app()

# Initialize Celery
celery = celery_init_app(app)
celery.autodiscover_tasks()

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    from application.task import monthly_report, daily_parking_reminder
    
    sender.add_periodic_task(
        crontab(minute='*/2'),
        monthly_report.s(),
    )
    
    sender.add_periodic_task(
        crontab(minute='*/2'),
        daily_parking_reminder.s(),
    )

from application.routes import *

if __name__ == "__main__":
    app.run()