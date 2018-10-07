import os
from PIL        import Image
from flask      import url_for, current_app
from flask_mail import Message
from flaskblog  import mail


def save_picture(form_picture):
  # save uploaded picture filename as a hashed value (prevent photos w/ same name in db)
  random_bytes        = os.urandom(24)
  random_hex          = b64encode(random_bytes).decode('utf-8')
  filename, file_ext  = os.path.splitext(form_picture.filename)
  picture_filename    = random_hex + file_ext
  picture_path        = os.path.join(current_app.root_path, 'static/profile_pics', picture_filename)

  # resize picture to outputsize
  output_size = (125, 125)
  image       = Image.open(form_picture)
  image.thumbnail(output_size)
  image.save(picture_path)
  return picture_filename



def send_reset_email(user):
  token = user.get_reset_token()
  msg = Message(
          'Password Reset Request', 
          sender     = 'noreply@demo.com',
          recipients = [user.email])
  msg.body = 'To reset your password, visit the following link: %s \
    If you did not make this request then simply ignore this email \
    and no change is required' % url_for('users.reset_token', token=token, _external=True)
  mail.send(msg)

