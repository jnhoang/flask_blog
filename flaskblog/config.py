import os


class Config:
  SECRET_KEY              = os.environ.get('FLASKBLOG_SECRETS_KEY')
  SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
  
  # mail configuration
  MAIL_SERVER   = 'smtp.googlemail.com'
  MAIL_PORT     = '587'
  MAIL_USE_TLS  = True
  MAIL_USERNAME = os.environ.get('FLASKBLOG_USER')
  MAIL_PASSWORD = os.environ.get('FLASKBLOG_PASSWORD')
