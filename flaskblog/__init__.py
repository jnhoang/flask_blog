from flask            import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime         import datetime
from flask_bcrypt     import Bcrypt
from flask_login      import LoginManager
import os


# Instantiate, initialize & configure App
app                                   = Flask(__name__)
app.config['SECRET_KEY']              = os.environ.get('FLASKBLOG_SECRETS_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Add app extensions
db            = SQLAlchemy(app)
bcrypt        = Bcrypt(app)
login_manager = LoginManager(app)

# extension configurations
login_manager.login_view             = 'login'
login_manager.login_message_category = 'info'

from flaskblog import routes
