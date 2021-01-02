#!/usr/bin/python3
import requests as req
import sys


def search(query):
    json = req.get('https://www.googleapis.com/books/v1/volumes?country=JP&q=' + str(query)).json()
    info = json['items'][0]['volumeInfo']
    return info


if __name__ == '__main__':
    query = sys.argv[1]
    print(search(query))