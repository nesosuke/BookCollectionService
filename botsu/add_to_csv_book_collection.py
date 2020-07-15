#!/usr/bin/python3
import csv
import requests as req
 
ISBN = input()
response = req.get(
    'https://www.googleapis.com/books/v1/volumes',
    params={
        "q": "isbn=" + str(ISBN)
    })
BookInfo = dict(response.json()).get("items")[0]["volumeInfo"]
BookTitle = BookInfo["title"]
BookAuthor = BookInfo["authors"][0]

