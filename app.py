from flask import Flask, render_template, url_for, redirect, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_mongoengine import MongoEngine
from mongoengine import StringField, EmailField
from form import LoginForm

app = Flask(__name__)

bootstrap = Bootstrap()
bootstrap.init_app(app)
db = MongoEngine()
db.init_app(app)

app.config['MONGODB_SETTINGS'] = {
    'db': 'academy1',
    'host': 'ds123956.mlab.com',
    'port': 25016,
    'username': 'william',
    'password': 'academy'
}

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "THISISSECRET"

class User(db.Document):
    username = StringField()
    email  = StringField()
    password = StringField()

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/signup', methods = ['GET','POST'])
def signup():
    form = LoginForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email=form.email.data, password = form.email.data)
        user.save()
        return redirect(url_for('signup'))
    return render_template('signup.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        return redirect(url_for('login'))
    return render_template('login.html', form=form, name=session.get('username'))

@app.route('/<user>')
def get_user(user):
    temp = User.objects(username=user).first()
    return render_template('userInfo', currentUser=temp)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)

#Check
