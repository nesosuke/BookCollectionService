#!/usr/bin/python3
from flask import Flask, render_template, request

app = Flask(__name__)

import getinfo

@app.route('/')
def index():
    return render_template(
        'search.html',
        title = "ISBN search",
        )

@app.route('/search', methods = ['GET'])
def result():
    query = request.args.get('isbn')
    result = getinfo.search(query)

    if result is False:
        return render_template(
            'error.html',
            query = query
        )
    else:    
        return render_template(
            'success.html',
            title="search result",
            isbn = query,
            booktitle= result['title'],
            bookauthor = result['author'],
            publisher = result['publisher'],
        )

if __name__ == "__main__":
    app.run(debug=True)