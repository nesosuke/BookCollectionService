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


def find_userdata(email, password):
    userdata = mongo.db.users.find_one({'email': email, 'password': password})
    return userdata


@app.route('/')
def toppage():
    return render_template('top.html')


@app.route('/search')
def search(): #書籍情報検索画面
    q = request.args.get('q')
    if q is None:
        return render_template('search.html')

    if bookDB.isISBN(q) is True:
        return flask.redirect(flask.url_for('book', q=q))
    else:
        pass

    # NDLで書名から検索する  ## 毎回NDL叩いてるのお行儀悪すぎワロタ
    res = bookDB.searchNDL(q, stringsearch=True, count=50)  # list
    result = []
    for i in range(len(res)):
        isbn = res[i].find('dc:identifier')
        if isbn is not None:
            isbn = isbn.text
            if bookDB.isISBN(isbn) is True:
                # print(isbn)
                bookDB.bookdb_update(isbn, skipsearch=True)
                result.append(bookDB.bookdb(isbn))
    return render_template(
        'result.html',
        result=result,
    )


@app.route('/book', endpoint='book')
def bookinfo(): #書籍情報を検索して表示する関数
    isbn = request.args.get('q')
    if isbn is None:
        return 'none'
    else:
        info = bookDB.bookdb(isbn)
        if info is not None:
            return render_template(
                'bookinfo.html',
                isbn=info['isbn'],
                title=info['title'],
                author=info['author'],
                publisher=info['publisher'],
                series=info['series'],
                volume=info['volume'],
                permalink=info['permalink'],
            )
        else:
            return 'bookinfo not found'


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
        # return 'success'
        return flask.redirect(flask.url_for('mypage'))
    else:
        return 'bad user'


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return render_template('top.html')


@app.route('/mypage')
@flask_login.login_required
def mypage():
    return render_template('mypage.html')


if __name__ == "__main__":
    app.run(debug=True)
