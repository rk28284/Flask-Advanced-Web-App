import os

class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # Use SQLite for simplicity
    UPLOAD_FOLDER = 'static/uploads/profile_pics'
