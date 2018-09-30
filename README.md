# Flaskblog


# Tutorial from 
* 


## Part 3

Below is the section in the video where Corey demos creating and querying users & posts via the Python interpretor.

```# db.create_all()

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
print User.query.all()```
