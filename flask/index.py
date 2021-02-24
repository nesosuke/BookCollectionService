#!/usr/bin/python3
import flask
from flask import render_template, request, session
import flask_login
from flask_pymongo import PyMongo, ObjectId
import functions

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


@app.route('/')
def toppage():
    return render_template('top.html')


@app.route('/mypage')
@flask_login.login_required
def mypage():
    return render_template('mypage.html')


@app.route('/book', methods=['GET'])
@flask_login.login_required
def show_bookinfo():
    query = request.args.get('q')

    if functions.isISBN(query) is False:
        return None

    res = functions.get_bookinfo_fromDB(query)
    session['isbn'] = query

    if res is None:
        res = functions.get_bookinfo_fromDB(query)

    return render_template('result.html',
                           result=res,  # dict
                           isFoundbyISBN=True)


@app.route('/record', methods=['POST'], endpoint='record')
@flask_login.login_required
def update_status():
    uid = str(flask_login.current_user.id)
    query = session['isbn']
    status = request.args.get('status')
    if functions.isISBN(query) is False:
        return None
    res = functions.update_status(uid, query, status)

    return 'done'

@app.route('/search', methods=['GET'])  # 検索ページ
def searchandresult_page():
    query = request.args.get('q')
    if query is None:
        return render_template('search.html')

    if functions.isISBN(query) is True:
        res = functions.get_bookinfo_fromDB(query)
        if res is not None:
            return flask.redirect(flask.url_for('/book?q='+query))

        else:
            return render_template('result.html',
                                   result=res,  # Nonetype
                                   )

    else:
        res = functions.search_fromNDL_byTitle(query)
        return render_template('result.html',
                               result=res,
                                 # list
                               isFoundbyISBN=False)

@app.route('/read')
@flask_login.login_required
def show_read():
    uid = str(flask_login.current_user.id)
    res =  list(mongo.db.data.find({'uid': uid, 'status': 'read'}))
    return render_template(
        'status.html',
        title="mystatus",
        result=res,
    )


if __name__ == "__main__":
    app.run(debug=True)
