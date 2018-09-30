from flask import Flask, render_template, url_for, flash, redirect
import os
from forms import RegistrationForm, LoginForm
# App imports


# Instantiate App
app                      = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASKBLOG_SECRETS_KEY')

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
