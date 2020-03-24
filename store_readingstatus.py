#!/usr/bin/python3
# ISBNでDBを検索して、登録があるか探す
# なければ新規作成、あればReadCountを1増やす
# 初回登録は未読として、2回目以降の登録を既読とする
# 検索キーはISBNにするけど、別にユニークなIDを振っておきたい気もする（岩○文庫の例があるので）（？）


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

BookInfo = {
            "Title": Title,
            "Author": Author,
            "Publisher": Publisher,
            "Publishded_at": Published_at, 
            "Cover": Cover,
            }

ReadingStatus = {      # 「なければ新規作成」の部分をやりたい
                "Read_at": Read_at, 
                "ReadStatus": ReadStatus, 
                "ReadCount": ReadCount, 
                } 

Data = [ISBN, BookInfo, ReadingStatus, response]

print(Title)
print(Author)
print(Publisher)
print(Published_at_yyyy + "." + Published_at_mm + "." + Published_at_dd)
print(Cover)