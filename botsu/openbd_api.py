#!/usr/bin/python3
#Google BooksでAPIを叩く
import requests as req
import sys

ISBN = sys.argv[1]
response = req.get('https://api.openbd.jp/v1/get?isbn=' + str(ISBN)).json()[0]
BookInfo = response.get("summary")

Title = BookInfo.get("title")
Author = BookInfo.get("author")
Publisher = BookInfo.get("publisher")
Published_at = [0] * 3
Published_at[0] = BookInfo.get("pubdate")[0:4]
Published_at[1] = BookInfo.get("pubdate")[4:6]
Published_at[2] = BookInfo.get("pubdate")[6:8]
Cover = BookInfo.get("cover")

print(Title)
print(Author)
print(Publisher)
print(Published_at_yyyy + "." + Published_at_mm + "." + Published_at_dd)
print(Cover)