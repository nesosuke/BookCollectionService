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
        title = "ERR: Bookinfo not found"
    else:    
        title= result['title']

    return render_template(
        'search.html',
        title="search result",
        booktitle=title,
    )

if __name__ == "__main__":
    app.run(debug=True)


