#!/usr/bin/python3
import requests as req
import sys

# ISBN -> 書籍情報の取得(openbd.jp)
ISBN = sys.argv[1]
response = req.get('https://api.openbd.jp/v1/get?isbn=' + str(ISBN)).json()[0]
BookInfo = response.get("summary")

print(BookInfo)

# record.txtからISBNで検索
#db_path = data/record.txt
#with open(db_path) as f:
