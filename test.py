from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME']='mongologinexample'
app.config['MONGO_URI']='mongodb://check:check@ds253587.mlab.com:53587/soda'

mongo = PyMongo(app)

bootstrap = Bootstrap()
bootstrap.init_app(app)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "THISISSECRET"

@app.route('/')
def index():
    if session['logged_in']:
        return render_template('index.html', name=session['username'])

    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists!'

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'name' : request.form['username']})

        if login_user:
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
                session['username'] = request.form['username']
                session['logged_in']=True
                return redirect(url_for('index'))

        return 'Invalid username/password combination'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    session['logged_in']=False
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)
