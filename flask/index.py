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


@login_manager.user_loader  # ログインセッション管理
def user_loader(session_id):
    userdata = mongo.db.users.find_one({'_id': ObjectId(oid=session_id)})
    if userdata is not None:
        user = User()
        user.id = userdata['_id']
    return user


@login_manager.unauthorized_handler  # 未ログイン状態のリダイレクト
def unauthorized_handler():
    return flask.redirect(flask.url_for('login'))


def find_userdata(email, password):  # ユーザーデータ検索
    userdata = mongo.db.users.find_one({'email': email, 'password': password})
    return userdata


@app.route('/login', methods=['GET', 'POST'])  # ログイン処理
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
        # return 'success'
        return flask.redirect(flask.url_for('mypage'))
    else:
        return 'bad user'


@app.route('/logout')  # ログアウト処理
def logout():
    flask_login.logout_user()
    return render_template('top.html')


@app.route('/mypage')
@flask_login.login_required
def return_mypage():
    return render_template('mypage.html')


if __name__ == "__main__":
    app.run(debug=True)
