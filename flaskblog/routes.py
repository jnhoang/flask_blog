from flask        import render_template, url_for, flash, redirect, request
from flask_login  import login_user, current_user, logout_user, login_required

# module imports
from flaskblog        import app, db, bcrypt
from flaskblog.forms  import RegistrationForm, LoginForm
from flaskblog.models import User, Post

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

@app.route('/get_user')
def get_user():
  print '\n\n\n'
  print User.query.first()
  return redirect(url_for('home'))


@app.route('/')
@app.route('/home')
def home():
  return render_template('home.html', posts=posts)


@app.route('/about')
def about():
  return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = RegistrationForm()
  if form.validate_on_submit():
    # form validation
    
    # enter user to db
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user            = User(
                        username = form.username.data,
                        email    = form.email.data,
                        password = hashed_password)
    db.session.add(user)
    db.session.commit()
    
    # success
    flash('Account created for %s, you are now able to log in' % form.username.data, 'success')
    return redirect(url_for('login'))

  return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = LoginForm()
  
  # TBD - divide into a POST route
  if form.validate_on_submit():
    user             = User.query.filter_by(email=form.email.data).first()
    correct_password = bcrypt.check_password_hash(user.password, form.password.data)
    if user and correct_password: 
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('home'))
    else:
      flash('Login unsuccessful. Please check email and password', 'danger')
      return render_template('login.html', title='Login', form=form)
  
  # TBD - divide this out to a GET route
  return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
  return render_template('account.html', title='Account')
