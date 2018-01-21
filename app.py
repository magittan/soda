from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap
import google.cloud
import googlemaps
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
    if session.get('logged_in') and session.get('lat_long'):
        print session['lat_long']['lat']
        print session['lat_long']['lng']
        return render_template('loggedIndex.html', name=session['username'], lat = session['lat_long']['lat'], lng =session['lat_long']['lng'])

    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass , 'address' : request.form['address'], 'zipcode' : request.form['zipcode'], 'city' : request.form['city']})
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

                address = login_user['address']
                city = login_user['city']
                zipcode = login_user['zipcode']
                totalQuery = "%s, %s, %s" % (address, city, zipcode)
                gmaps = googlemaps.Client(key='AIzaSyBpTKOfOdXY27Plw6m0OnhAixPIB7mD9xQ')
                session['lat_long'] = gmaps.geocode(totalQuery)[0]['geometry']['location']

                return redirect(url_for('index'))

        return 'Invalid username/password combination'
    return render_template('login.html')

@app.route('/registerPatient', methods=['GET', 'POST'])
def registerPatient():
    if session.get('logged_in'):
        if request.method == 'POST':
            patients = mongo.db.patients
            patients.insert({'hospital' : session['username'], 'name' : request.form['name'], 'height' : request.form['height'], \
            'weight' : request.form['weight'], 'age' : request.form['age'], 'bloodtype' : request.form['bloodtype'], 'gender': request.form['gender'], \
            'birthdate' : request.form['birthdate'], 'polyuria' : request.form['polyuria'], 'urine' : request.form['urine'], 'kidneyDisease' : request.form['kidneyDisease'], 'seizures' : request.form['seizures'], 'palpitations' : request.form['palpitations'], \
             'smoking' : request.form['smoking'], 'insomnia' : request.form['insomnia'], 'blurredVision' : request.form['blurredVision'], 'HIVHepa' : request.form['HIVHepa'], 'eyes' :request.form['eyes'], 'patientLungs' : request.form['patientLungs'], })
            return render_template('registerPatient.html', success = "Success!!")

    return render_template('registerPatient.html')

@app.route('/patients')
#waits for a post request in order to get an image
def patients():
    return render_template('patients.html')

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
