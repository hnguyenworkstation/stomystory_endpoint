# gunicorn wsgi:application -b localhost:8000 &
import os
from app import create_app

application = app = create_app(os.getenv('APP_CONFIG') or 'default')
