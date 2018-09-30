from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# App Module imports


# Instantiate App
app                                   = Flask(__name__)
app.config['SECRET_KEY']              = os.environ.get('FLASKBLOG_SECRETS_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
  id         = db.Column(db.Integer, primary_key=True)
  username   = db.Column(db.String(20), unique=True,    nullable=False)
  email      = db.Column(db.String(120),  unique=True,    nullable=False)
  image_file = db.Column(db.String(20),  nullable=False, default='default.jpg')
  password   = db.Column(db.String(60),  nullable=False)
  
  posts      = db.relationship('Post', backref='author', lazy=True)

  def __repr__(self):
    return 'User(%s, %s, %s)' % (self.username, self.email, self.image_file)


class Post(db.Model):
  id          = db.Column(db.Integer    , primary_key=True)
  title       = db.Column(db.String(100), nullable=False)
  date_posted = db.Column(db.DateTime   , nullable=False, default=datetime.utcnow)
  content     = db.Column(db.Text       , nullable=False)
  user_id     = db.Column(db.Integer    , db.ForeignKey('user.id'), nullable=False)
  

  def __repr__(self):
    return 'User(%s, %s)' % (self.title, self.date_posted)

# db.create_all()

def add_users():
  user1 = User(username='justin', email='j@demo.com', password='password')
  db.session.add(user1)
  user2 = User(username='julie', email='j2@demo.com', password='password')
  db.session.add(user2)
  db.session.commit()

def query_users():
  print 'all query\n'
  print User.query.all()

  print 'first person\n'
  print User.query.first()
  print User.query.filter_by(username='justin').all()
  user = User.query.filter_by(username='justin').first()

  print 'first user'
  print user

  print user.query.get(1)

# add_users()
# query_users()

def create_post():
  post_1 = Post(title='Blog 1', content='First post content!', user_id=1)
  post_2 = Post(title='Blog 2', content='Second post content!', user_id=1)
  db.session.add(post_1)
  db.session.add(post_2)
  db.session.commit()
# create_post()


def query_post():
  post = Post.query.first()
  print post
  print post.author
  # user = User.query.first()
  # posts = user.posts

  # print posts
  # print len(posts)

# query_post()
# db.drop_all()
# db.create_all()
print User.query.all()

posts = [
  {
    'author'      : 'Sample Author',
    'title'       : 'blog post 1',
    'content'     : 'first post content',
    'date_posted' : 'April 1, 2018'
  },
  {
    'author'      : 'Sample Author',
    'title'       : 'blog post 2',
    'content'     : '2nd post content',
    'date_posted' : 'April 2, 2018'
  }
]


@app.route('/')
@app.route('/home')
def home():
  return render_template('home.html', posts=posts)


@app.route('/about')
def about():
  return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    flash('Account created for %s' % form.username.data, 'success')
    return redirect(url_for('home'))

  return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    if form.email.data == 'admin@blog.com' and form.password.data == 'password':
      flash('You have been logged in!', 'success')
      return redirect(url_for('home'))
    else:
      flash('Login unccessful. Please check username and password', 'danger')
  return render_template('login.html', title='Login', form=form)





if __name__ == '__main__':
  app.run(debug=True)
