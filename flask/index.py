#!/usr/bin/python3
import flask
from flask import render_template, request, session
import flask_login
from flask_pymongo import PyMongo, ObjectId
import getinfo
import googlebookapi

app = flask.Flask(__name__)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

app.secret_key = 'super secret string'  # Change this!

app.config["MONGO_URI"] = "mongodb://localhost:27017/bookmeter"
mongo = PyMongo(app)

# Our mock database.
users = {'foo@bar.tld': {'password': 'secret'}}


class User(flask_login.UserMixin):
    email = ""

# セッション保持するやつ


@login_manager.user_loader
def user_loader(user_id):
    searched_by_email = mongo.db.users.find_one({'_id': ObjectId(oid=user_id)})
    if searched_by_email is None:
        return None

    user = User()
    user.email = searched_by_email['email']
    user.id = searched_by_email['_id']
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html')

    email = flask.request.form['email']
    password = flask.request.form['password']
    isValid = mongo.db.users.find_one({'email': email, 'password': password})
    # if flask.request.form['password'] == users[email]['password']:
    if isValid is not None:
        user = User()
        user.id = isValid['_id']
        print('isvalid', isValid['_id'])  # mongoの_id
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('index'))

    return 'Bad login'


@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    # return 'Logged out'
    return flask.redirect(flask.url_for('login'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return flask.redirect(flask.url_for('login'))


@app.route('/')
@flask_login.login_required
def index():
    return render_template(
        'search.html',
        title="ISBN search",
    )

# ISBNから書籍情報とる
# /search?isbn=1234
# ISBNがわかんない場合は？


@app.route('/search', methods=['GET'])
@flask_login.login_required
def result():
    query = request.args.get('q')
    result = getinfo.search(query)

    if result is False:
        return render_template(
            'error.html',
            query=query,
            title="bookinfo not found"
        )
    else:
        session["isbn"] = query
        session["bookinfo"] = result
        record = mongo.db.data.find_one({"isbn": session["isbn"]})
        if record is not None:
            status = record["status"]
            memo = record.get("memo", "")
        else:
            status = "unread"
            memo = ""

        return render_template(
            'success.html',
            title="search result",
            isbn=query,
            booktitle=result['title'],
            bookauthor=result['author'],
            publisher=result['publisher'],
            status=status,
            memo=memo,
        )


@app.route('/searchbygoogle', methods=['GET'])
def searchbygoogle():
    query = request.args.get('q')
    res = googlebookapi.search(query)
    booktitle = res['title']
    bookauthor = res['authors']
    if 'publisher' in res:
        publisher = res['publisher']
    else:
        publisher = "publisher is not found"

    if len(res['industryIdentifiers']) == 2:
        isbn = res['industryIdentifiers'][1]['identifier']
    else:
        isbn = "isbn is not found"

    return render_template(
        'success.html',
        title="bookinfo search",
        booktitle=booktitle,
        isbn=isbn,
        bookauthor=bookauthor,
        publisher=publisher,
    )


@app.route('/status', methods=['POST'])
@flask_login.login_required
def update_status():
    status = request.form["status"]
    memo = request.form["memo"]
    booktitle = session['bookinfo']["title"]
    bookauthor = session["bookinfo"]['author']
    publisher = session["bookinfo"]['publisher']
    record = {"isbn": session["isbn"], "status": status, "memo": memo}
    uid = str(flask_login.current_user.id)
    mongo.db.data.find_one_and_update(
        {'uid': uid, 'isbn': session["isbn"]},
        {
            "$setOnInsert":
            {
                "title": booktitle,
                "author": bookauthor,
                "publisher": publisher,
                "uid": uid
            },
            "$set":
            {
                "status": status,
                "memo": memo
            }

        },
        upsert=True
    )

    return render_template(
        'status.html',
        title="mystatus",
        json=record,
        bookinfo=session["bookinfo"],
    )


# uid のステータスを全表示する


@app.route('/mystatus', methods=['GET'])
def mystatus():
    uid = str(flask_login.current_user.id)
    name = mongo.db.users.find_one({'_id': ObjectId(oid=uid)})['email']
    isReading = list(mongo.db.data.find({'uid': uid, 'status': 'reading'}))
    hasRead = list(mongo.db.data.find({'uid': uid, 'status': 'read'}))
    return render_template(
        'mystatus.html',
        title="mystatus",
        name=name,
        isReading=isReading,
        hasRead=hasRead
    )


if __name__ == "__main__":
    app.run(debug=True)
