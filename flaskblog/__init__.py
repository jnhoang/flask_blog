from flask            import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime         import datetime
import os


# Instantiate/Initialize App
app                                   = Flask(__name__)
app.config['SECRET_KEY']              = os.environ.get('FLASKBLOG_SECRETS_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from flaskblog import routes

if __name__ == '__main__':
  app.run(debug=True)
