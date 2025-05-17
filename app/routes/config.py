import os
from datetime import timedelta

class Config:
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key_not_for_production')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt_dev_key_not_for_production')
    
    # JWT Configuration
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    
    # Password Reset Token Configuration
    PASSWORD_RESET_EXPIRES = timedelta(hours=24)