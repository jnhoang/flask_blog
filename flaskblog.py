from flask import Flask, render_template, url_for
app = Flask(__name__)

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

if __name__ == '__main__':
  app.run(debug=True)
