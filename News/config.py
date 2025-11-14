import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/news_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    TEMPLATES_AUTO_RELOAD = True
    SECRET_KEY = '1A45fG-39kLpZ_7bHjM_6QxY-2cDvP_9eSjT-8uAwE'
    
    UPLOAD_FOLDER = 'static/imgs'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}