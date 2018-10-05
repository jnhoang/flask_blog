from flask_wtf          import  FlaskForm
from flask_wtf.file     import FileField, FileAllowed
from flask_login        import current_user
from wtforms            import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models   import User


class RegistrationForm(FlaskForm):
  username          = StringField('Username'          , validators = [DataRequired(), Length(min=2, max=20)])
  email             = StringField('Email'             , validators = [DataRequired(), Email()])
  password          = PasswordField('Password'        , validators = [DataRequired()])
  confirm_password  = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
  submit            = SubmitField('Sign Up')

  def validate_username(self, username):
    user          = User.query.filter_by(username=username.data).first()
    error_message = 'That username is taken. Please choose a different one.'
    if user: raise ValidationError(error_message)

  def validate_email(self, email):
    user          = User.query.filter_by(email=email.data).first()
    error_message = 'That email is taken. Please choose a different one.'
    if user: raise ValidationError(error_message)


class UpdateAccountForm(FlaskForm):
  username          = StringField('Username' , validators = [DataRequired(), Length(min=2, max=20)])
  email             = StringField('Email'    , validators = [DataRequired(), Email()])
  picture           = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
  submit            = SubmitField('Update')

  def validate_username(self, username):
    username_changed = username.data != current_user.username
    if username_changed:
      user          = User.query.filter_by(username=username.data).first()
      error_message = 'That username is taken. Please choose a different one.'
      if user: raise ValidationError(error_message)

  def validate_email(self, email):
    emailed_changed = email.data != current_user.email
    if emailed_changed:
      user          = User.query.filter_by(email=email.data).first()
      error_message = 'That email is taken. Please choose a different one.'
      if user: raise ValidationError(error_message)


class LoginForm(FlaskForm):
  email    = StringField('Email'      , validators = [DataRequired(), Email()])
  password = PasswordField('Password' , validators = [DataRequired()])
  remember = BooleanField('Remember Me')
  submit   = SubmitField('Login')



class PostForm(FlaskForm):
  title   = StringField('Title', validators=[DataRequired()])
  content = TextAreaField('Content', validators=[DataRequired()])
  submit  = SubmitField('Post')

