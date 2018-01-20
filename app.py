# from flask import Flask, render_template, url_for, redirect, session
# from flask_bootstrap import Bootstrap
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from flask_mongoengine import MongoEngine
# from mongoengine import StringField, EmailField
# from form import LoginForm
#
# app = Flask(__name__)
#
# bootstrap = Bootstrap()
# bootstrap.init_app(app)
# db = MongoEngine()
# db.init_app(app)
#
# app.config['MONGODB_SETTINGS'] = {
#     'db': 'soda',
#     'host': 'ds253587.mlab.com',
#     'port': 53587,
#     'username': 'check',
#     'password': 'check'
# }
#
# app.config['DEBUG'] = True
# app.config['SECRET_KEY'] = "THISISSECRET"
#
# class User(db.Document):
#     username = StringField()
#     email  = StringField()
#     password = StringField()
#
# @app.route('/')
# def index():
#   return render_template('index.html')
#
# @app.route('/signup', methods = ['GET','POST'])
# def signup():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User(username = form.username.data, email=form.email.data, password = form.email.data)
#         user.save()
#         return redirect(url_for('signup'))
#     return render_template('signup.html', form = form)
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         session['username'] = form.username.data
#         return redirect(url_for('login'))
#     return render_template('login.html', form=form, name=session.get('username'))
#
# @app.route('/<user>')
# def get_user(user):
#     temp = User.objects(username=user).first()
#     return render_template('userInfo', currentUser=temp)
#
# @app.route('/about')
# def about():
#     return render_template('about.html')
#
# if __name__ == '__main__':
#     app.run('0.0.0.0',debug=True)
#
# #Check

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
