from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from database import Database
from datetime import date
import bcrypt

app = Flask(__name__)
session = {}
db = Database('database.db')


@app.route("/")
@app.route("/login")
def login():
    message = ''
    if request.method == 'POST':# and 'name' in request.form and 'password' in request.form:
        username = request.form['name']
        password = request.form['password']

        # Check user and password from database
        try:
            db.connect()

            if db.verify_user(username, password):
                message = 'Logged in successfully !'
                session['loggedin'] = True
            else:
                message = 'Invalid username or password.'
                session['loggedin'] = False

            session['userid'] = username

        except sqlite3.Error as error:
            message = 'Something went wrong !'
            session['loggedin'] = False

        finally:
            db.close()

        return render_template('user.html', message=message)
    else:
        # message = 'Please enter username / password !'
        return render_template('login.html', message=message)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form:
        username = request.form['name']
        password = request.form['password']

        # Checking if user already exists
        username_check = False
        try:
            db.connect()
            username_check = db.check_user(username)
        except sqlite3.Error as error:
                message = 'Something went wrong !'
        finally:
                db.close()
        
        if username_check:
            message = 'Account already exists !'

        # TODO: Password requirements check

        elif not username or not password:
            message = 'Please fill out the form !'
        
        else:
            # Current implementation of adding users
            today = date.today()
            hashed_password, salt = hash_password(password)
            try:
                db.connect()
                db.add_user(username, hashed_password, salt, today)
                db.connection.commit()
                message = 'You have successfully registered!'

            except sqlite3.Error as error:
                message = 'Something went wrong !'

            finally:
                db.close()

        return render_template('login.html', message=message)

    elif request.method == 'POST':
        message = 'Please fill out the form !'
    return render_template('register.html', message=message)


@app.route("/user")
def user():
    return render_template("user.html")


@app.route('/setcookie', methods=['POST'])
def set_cookie():
    if request.method == 'POST':
        user = request.form['nm']

    resp = make_response(render_template('cookie.html'))
    resp.set_cookie('userID', user)

    return resp


@app.route('/getcookie')
def get_cookie():
    name = request.cookies.get('userID')
    return '<h1>Welcome to The Game, ' + name + '</h1>'

# Function to hash a password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password, salt

if __name__ == '__main__':
    app.run(debug=True)
