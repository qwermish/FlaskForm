from flask import Flask, render_template, request, flash, url_for, session, send_file, redirect
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, IntegerField, StringField, PasswordField, validators
from forms import LoginForm, RegistrationForm
import matplotlib.pyplot as plt
from io import StringIO
from StringIO import StringIO
import os
#from flask_heroku import Heroku

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/preregage'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'keep-going'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
#heroku = Heroku(app)
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

# Set "homepage" to index2.html
@app.route('/')
def index():
    register_form = RegistrationForm()
    login_form = LoginForm()
    return render_template('index2.html', register_form=register_form, login_form=login_form)

@app.route('/register', methods=['POST'])
def register():
    register_form = RegistrationForm(request.form)
    login_form = LoginForm()

    if register_form.validate_on_submit() and not db.session.query(User).filter(User.username == register_form.username.data).count():
        user = User(username=register_form.username.data, age=register_form.age.data,
                    password=register_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('images', age=user.age))
    return render_template('index2.html', register_form=register_form, login_form=login_form)

@app.route('/login', methods=['POST'])
def login():
    register_form = RegistrationForm()
    login_form = LoginForm()

    if request.method=="POST" and login_form.validate_on_submit():
        print 'validated'
        user = db.session.query(User).filter_by(username=login_form.username.data).first()
        print user
        if user is None or (user.password != login_form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        #if successful validation, redirect to image URL with age argument
        return redirect(url_for('images', age=user.age))
    return render_template('index2.html', register_form=register_form, login_form=login_form)

@app.route('/images/<age>')
def images(age):
    return render_template("images.html", title=age)

@app.route('/fig/<age>/chart.png')
def fig(age):
    #number of bins in histogram
    BinsNumber = 10
    users = db.session.query(User.age)
    data = []
    for row in users:
        data.append(int(row[0]))
    n, bins, patches = plt.hist(data, bins=BinsNumber)
    for patch in patches: #set all patches to be blue
        patch.set_fc('b')
    plt.ylabel('Number of registered users')
    plt.xlabel('Age')
    mybin = BinsNumber-1
    #find bin in which variable 'age' belongs
    for i in range(len(bins)-1):
        if ((int(age) >=bins[i]) and (int(age) < bins[i+1])):
            mybin = i
    #set patch of current user to be red
    patches[mybin].set_fc('r')
    fig = plt.gcf() #fig is set to current figure
    img = StringIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

#cache busting
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    app.debug = True
    app.run()
