from flask            import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime         import datetime
from flask_bcrypt     import Bcrypt
from flask_login      import LoginManager
from flask_mail       import Mail

from flaskblog.config import Config


# add app extensions
db            = SQLAlchemy()
bcrypt        = Bcrypt()
login_manager = LoginManager()

# extension configurations
login_manager.login_view             = 'users.login'
login_manager.login_message_category = 'info'

# mail config
mail = Mail()


# instantiate, initialize & configure App
def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(Config)

  # pass app var to app extensions
  # done this way so that extensions are not bound to the app object
  # no specific app state stored on the extension object
  # so that one extension object can be used for multiple apps
  db.init_app(app)
  bcrypt.init_app(app)
  login_manager.init_app(app)
  mail.init_app(app)

  # register blueprints
  from flaskblog.main.routes  import main
  from flaskblog.users.routes import users
  from flaskblog.posts.routes import posts

  app.register_blueprint(main)
  app.register_blueprint(users)
  app.register_blueprint(posts)

  return app
