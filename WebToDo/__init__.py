from flask import Flask,render_template,redirect,url_for,request,flash,session
import sys
#from dbconnect.dbconnect import connection
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, SubmitField, TextField, PasswordField, StringField, validators
from passlib.hash import sha256_crypt
#from MySQLdb import escape_string as thwart
import mysql.connector
from wtforms.validators import DataRequired
import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])

def connection():
    conn = mysql.connector.connect(host="localhost",
                           user = "root",
                           passwd = "$$Shiva123",
                           db = "sample")
    c = conn.cursor()

    return c, conn

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

'''
@app.route('/login/', methods=["GET","POST"])
def login_page():

    error = ''
    try:
    
        if request.method == "POST":
        
            attempted_username = request.form['username']
            attempted_password = request.form['password']

            #flash(attempted_username)
            #flash(attempted_password)

            if attempted_username == "admin" and attempted_password == "password":
                return redirect(url_for('index'))
                
            else:
                error = "Invalid credentials. Try Again."

        return render_template("login.html",title='Log in', error = error)

    except Exception as e:
        #flash(e)
        return render_template("login.html",title='Log in', error = error)
'''
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm()

        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            x = c.execute("SELECT * FROM users WHERE username = (%s)",
                          (username))

            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)

            else:
                c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
                          (username,password,email,"/introduction-to-python-programming/"))
                
                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('index'))

        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))
        

if __name__ == "__main__":
    app.run()