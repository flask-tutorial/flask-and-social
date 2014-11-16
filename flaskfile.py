# ====================================================================================
# Example Flask Web App 
# ====================================================================================
# originially from https://github.com/flask-tutorial/flask-and-social

# all the imports
import urllib, json, os, facebook
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_appconfig.env import from_envvars
#from flask.ext.heroku import Heroku

app = Flask(__name__)
#heroku = Heroku(app)


if os.environ.get('HEROKU') is not None:
  import logging
  stream_handler = logging.StreamHandler()
  app.logger.addHandler(stream_handler)
  app.logger.setLevel(logging.INFO)
  app.logger.info('flask-and-social startup')

# this will read in variables from config.py
from_envvars(app.config, prefix='MY_')


# ====================================================================================
# setup and teardown for each HTTP request
# ====================================================================================
# the @ sign here means that app.before_request is a "decorator" for the function 
# defined in the next line. http://legacy.python.org/dev/peps/pep-0318/#current-syntax
# but you don't have to understand that to use it
#
# in a flask app, putting @app.before_request before a function means
# that this function will be called before a request is routed, and app.teardown_request
# is called after everything is finished.  
# So this is a good place to connect/disconnect to the database
@app.before_request
def before_request():
  g.dir = os.path.dirname(os.path.abspath(__file__))
  #g.db  = sqlite3.connect(g.dir + '/' + app.config['DATABASE'])
  g.facebook_user = facebook.get_user_from_cookie(request.cookies, app.config['FACEBOOK_APP_ID'], app.config['FACEBOOK_APP_SECRET'])
  app.logger.error('facebook user' + repr(g.facebook_user))


@app.teardown_request
def teardown_request(exception):
  pass
  #db = getattr(g, 'db', None)
  #if db is not None:
  #  db.close()

# ====================================================================================
# routes - these map URLs to your python functions
# ====================================================================================
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_entry():
  if not session.get('logged_in'):
    abort(401)
  flash('New entry was successfully posted')
  return redirect(url_for('table'))

@app.route('/form', methods=['GET', 'POST'])
def form():
  if not session.get('logged_in'):
    abort(401)
  errors = []
  if request.method == 'POST':
    mood = int( request.form.get('mood') )
    if not mood in [1,2,3,4,5]:
      errors.append( 'please choose a mood' )

    if len(errors) == 0:
      #g.db.execute('insert into mood (uid, mood, lat, long) values (?, ?, ?, ?)', 
      #             [session['uid'], mood, request.form.get('lat'), request.form.get('long')])
      #g.db.commit()
      flash('Your entry "' + str(mood) + '" was not saved to the database - because we currently have no database')
      return redirect( url_for('index') )
  return render_template('form.html', error=", ".join(errors))

@app.route('/connections')
def connections():
  if not session.get('logged_in'):
    abort(401)
  #cur = g.db.execute('select * from user where uid=?', [ session['uid'] ])
  connections = [] # cur.fetchall()
  return render_template('connections.html', connections=connections, facebook_user = g.facebook_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME']:
      error = 'Invalid username'
    elif request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid password'
    else:
      session['logged_in'] = True
      session['uid'] = 1
      session['username'] = request.form['username']
      flash('You were logged in as ' + session['username'])
      return redirect( url_for('index') )
  return render_template('login.html', error=error)

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('index'))

# ====================================================================================
@app.errorhandler(401)
def page_not_found(e):
  return render_template('401.html'), 404

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

# ====================================================================================
if __name__ == '__main__':
  app.run()
# ====================================================================================
