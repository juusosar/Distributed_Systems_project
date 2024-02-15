from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
session = {}


@app.route("/")
@app.route("/login")
def login():
    message = ''
    if request.method == 'POST':# and 'name' in request.form and 'password' in request.form:
        username = request.form['name']
        password = request.form['password']

        # TODO: Check user and password from database

        session['loggedin'] = True
        session['userid'] = username
        message = 'Logged in successfully !'
        return render_template('user.html',
                               message=message)
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
        account = True

        # TODO: Upload username and password to database

        if account:
            message = 'Account already exists !'

        elif not username or not password:
            message = 'Please fill out the form !'

        message = 'You have successfully registered!'
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


if __name__ == '__main__':
    app.run(debug=True)
