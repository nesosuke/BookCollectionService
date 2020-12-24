#!/usr/bin/python3
from flask import Flask, render_template, request

app = Flask(__name__)

import getinfo

@app.route('/')
def index():
    return render_template(
        'index.html',
        title = "ISBN search",
        )

@app.route('/search', methods = ['GET'])
def result():
    query = request.args.get('isbn')
    result = getinfo.search(query)

    if result is "Error":
        error = "ERR: Bookinfo not found"
        title = error
        bookauthor = error
        publisher = error
    else:    
        title= result['title']
        bookauthor = result['author']
        publisher = result['publisher']
    return render_template(
        'search.html',
        title="search result",
        booktitle=title,
        bookauthor=bookauthor,
        publisher=publisher,
    )

if __name__ == "__main__":
    app.run(debug=True)


