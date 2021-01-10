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

# ログインセッション管理
@login_manager.user_loader
def user_loader(session_id):
    userdata = mongo.db.users.find_one({'_id': ObjectId(oid=session_id)})
    if userdata is not None:
        user = User()
        user.id = userdata['_id']
    return user


def redirect(dest):
    flask.redirect(flask.url_for(dest))


def find_userdata(email, password):
    userdata = mongo.db.users.find_one({'email': email, 'password': password})
    return userdata


@app.route('/')
def rootpage():
    return 'top'


@app.route('/book')
def booksearch():
    isbn = request.args.get('q')
    if isbn is None:
        return 'none'
    else:
        data = bookDB.bookdb(isbn)
        if data is not None:
            return render_template(
                'bookinfo.html',
                isbn=data['isbn'],
                title=data['title'],
                author=data['author'],
                publisher=data['publisher'],
                series=data['series'],
                volume=data['volume'],
                permalink=data['permalink'],
            )
        else:
            return 'data is none'


@app.route('/book/update', methods=['GET'])
def update():
    q = request.args.get('q')
    if q is None:
        return 'q is none'
    else:
        data = bookDB.bookdb_update(q)
        if data is not None:
            data = bookDB.bookdb(q)
            return 'done'
        else:
            return 'data is none'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return flask.redirect(flask.url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html')

    email = flask.request.form['email']
    password = flask.request.form['password']

    userdata = find_userdata(email, password)
    if userdata is not None:
        user = User()
        user.id = userdata['_id']
        flask_login.login_user(user)
        return 'success'
    else:
        return 'bad user'


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return render_template('home.html')


@app.route('/home')
@flask_login.login_required
def home():
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)
