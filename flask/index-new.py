#!/usr/bin/python3
import flask
from flask import render_template, request, session
import flask_login
from flask_pymongo import PyMongo, ObjectId
import bookDB

app = flask.Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

app.secret_key = 'super secret string'  # Change this!
app.config["MONGO_URI"] = "mongodb://localhost:27017/bookmeter"
mongo = PyMongo(app)


class User(flask_login.UserMixin):
    id = ""

@login_manager.user_loader
def user_loader(session_id):
    userdata = mongo.db.users.find_one({'_id': ObjectId(oid=session_id)})
    if userdata is not None:
        session = User()
        session.id = userdata['_id']
    return session


def redirect(dest):
    flask.redirect(flask.url_for(dest))


def find_userdata(email, password):
    userdata = mongo.db.users.find_one_or_404(
        {'email': email, 'password': password})
    if userdata == '404':
        return None
    else:
        session = User()
        session.id = userdata['_id']
        return session


@app.route('/')
def rootpage():
    return 'home'


@app.route('/book')
def booksearch():
    data = bookDB.bookdb(request.args.get('q'))
    return render_template(
        'bookinfo.html',
        isbn=data['isbn'],
        title=data['title'],
        author=data['title'],
        publisher=data['publisher'],
        series=data['series'],
        permelink=data['permalink'],
    )


@login_manager.unauthorized_handler
def unauthorized_handler():
    return flask.redirect(flask.url_for('login'))




@app.route('/login', methods=['GET', 'POST'])
@flask_login.login_required
def login():
    if flask.request.method == 'GET':
        return render_template('login.html')

    email = flask.request.form['email']
    password = flask.request.form['password']

    if find_userdata(email, password) is not None:
        flask_login.login_user(session)
        return redirect('/home')
    else:
        return 'bad user'


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect('/')


@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
