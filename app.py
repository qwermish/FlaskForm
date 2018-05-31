from flask import Flask, render_template, request, flash, url_for, session, send_file, redirect
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, IntegerField, StringField, PasswordField, validators
from forms import LoginForm, RegistrationForm
import matplotlib.pyplot as plt
from io import StringIO
from StringIO import StringIO
import os

#Configure the app as follows.
app = Flask(__name__)
#the following line is for local hosting.
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/preregage'
# the following line os for hosting on Heroku
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'keep-going'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
db = SQLAlchemy(app)

# Create our database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    age = db.Column(db.Integer)
    def __repr__(self):
        return '<User {}>'.format(self.username)

# Set "homepage" to index2.html. It includes the forms defined in forms.py
@app.route('/')
def index():
    register_form = RegistrationForm()
    login_form = LoginForm()
    return render_template('index2.html', register_form=register_form, login_form=login_form)

#What happens when you submit the registration form
@app.route('/register', methods=['POST'])
def register():
    register_form = RegistrationForm(request.form)
    login_form = LoginForm()
    
    #check for field validations and make sure username does not yet exist
    if register_form.validate_on_submit():
        if not db.session.query(User).filter(User.username == register_form.username.data).count():
            #if both conditions met, add user to database
            user = User(username=register_form.username.data, age=register_form.age.data,
                    password=register_form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('images', age=user.age))
        #if username already exist, flash following error message
        else:
            flash('Username has been taken')
    return render_template('index2.html', register_form=register_form, login_form=login_form)

#What happens when you submit the login form
@app.route('/login', methods=['POST'])
def login():
    register_form = RegistrationForm()
    login_form = LoginForm()

    #check for field validations
    if login_form.validate_on_submit():
        user = db.session.query(User).filter_by(username=login_form.username.data).first()
        if user is None or (user.password != login_form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        #if successful validation, redirect to image URL with age argument
        return redirect(url_for('images', age=user.age))
    return render_template('index2.html', register_form=register_form, login_form=login_form)

#URL for page that displays histogram
@app.route('/images/<age>')
def images(age):
    return render_template("images.html", title=age)

#URL for histogram itself. Takes current user's age as argument.
@app.route('/fig/<age>/chart.png')
def fig(age):
    #number of bins in histogram
    BinsNumber = 10
    #get ages from database
    users = db.session.query(User.age)
    #construct array of ages
    data = []
    for row in users:
        data.append(int(row[0]))
    #define histogram components
    n, bins, patches = plt.hist(data, bins=BinsNumber)
    for patch in patches: #set all patches to be blue
        patch.set_fc('b')
    plt.ylabel('Number of registered users')
    plt.xlabel('Age')
    #start by setting the user's age bin to be the rightmost bin. This will be changed if the user's age is found to fall in an earlier bin.
    mybin = BinsNumber-1
    #find bin in which variable 'age' belongs. Don't have to check rightmost bin as that is set as the default.
    for i in range(len(bins)-1):
        if ((int(age) >=bins[i]) and (int(age) < bins[i+1])):
            mybin = i
    #set patch of current user to be red
    patches[mybin].set_fc('r')

    fig = plt.gcf() #set fig to be current figure
    img = StringIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

#cache busting, in case histograms don't update properly
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    app.debug = True
    app.run()
