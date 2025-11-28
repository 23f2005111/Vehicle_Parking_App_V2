from flask import Flask
from application.config import LocalDevelopementConfig
from application.database import db
from application.models import User
from application.security import jwt
from flask_cors import CORS
from application.celery_init import celery_init_app
from celery.schedules import crontab
from application.cache_config import init_cache  # importing cache initialization function

app = None

def create_app():
    app = Flask(__name__)  # Create Flask application instance
    app.config.from_object(LocalDevelopementConfig) # Load configuration from LocalDevelopementConfig class
    db.init_app(app) # db config
    jwt.init_app(app)  # jwt config
    CORS(app)  # cors enable
    # initialize cache with app (connects Redis cache to Flask)
    init_cache(app)  # initialise cache 
    app.app_context().push()   # push application context 
    
    return app  

app = create_app()



# initialize Celery with Flask app (for background tasks)
celery = celery_init_app(app)

# auto-discover tasks from task.py file
celery.autodiscover_tasks()

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute='*/2'),   # Run every 2 minutes
        monthly_report.s(),      # call monthly_report task
    )

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute='*/2'),          # run every 2 minutes (testing)
        daily_parking_reminder.s(),     # call daily_parking_reminder task
    )


from application.routes import *

if __name__ == "__main__":
    # Commented out initial database setup
    # Only run once to create tables and add admin user
    # db.create_all()
    # db.session.add(User(username="admin", email="admin@admin.com", password="1234", role = "admin"))
    # db.session.commit()

    # Start Flask development server
    app.run()