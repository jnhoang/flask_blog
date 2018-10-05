import os
from  base64      import b64encode
from PIL          import Image
from flask        import render_template, url_for, flash, redirect, request
from flask_login  import login_user, current_user, logout_user, login_required

# module imports
from flaskblog        import app, db, bcrypt
from flaskblog.forms  import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post



@app.route('/get_user')
def get_user():
  print '\n\n\n'
  print User.query.first()
  return redirect(url_for('home'))


@app.route('/')
@app.route('/home')
def home():
  posts = Post.query.all()
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


def save_picture(form_picture):
  # save uploaded picture filename as a hashed value (prevent photos w/ same name in db)
  random_bytes        = os.urandom(24)
  random_hex          = b64encode(random_bytes).decode('utf-8')
  filename, file_ext  = os.path.splitext(form_picture.filename)
  picture_filename    = random_hex + file_ext
  picture_path        = os.path.join(app.root_path, 'static/profile_pics', picture_filename)

  # resize picture to outputsize
  output_size = (125, 125)
  image       = Image.open(form_picture)
  image.thumbnail(output_size)
  image.save(picture_path)
  return picture_filename


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
  form = UpdateAccountForm()
  
  # this if block is for POST method
  if form.validate_on_submit():
    if form.picture.data:
      picture_file            = save_picture(form.picture.data)
      current_user.image_file = picture_file
    
    current_user.username = form.username.data
    current_user.email    = form.email.data
    db.session.commit()

    flash('your account has been updated!', 'success')
    return redirect(url_for('account'))
  
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data    = current_user.email

  image_file = url_for('static', filename='profile_pics/%s' % current_user.image_file)
  return render_template(
          'account.html', 
          title      = 'Account',
          image_file = image_file,
          form       = form)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
  form = PostForm()
  if form.validate_on_submit():
    post = Post(title=form.title.data, content=form.content.data, author=current_user)
    db.session.add(post)
    db.session.commit()
    flash('Your post has been created', 'success')
    return redirect(url_for('home'))
  return render_template('create_post.html', title= 'New Post', form=form)




