#!/usr/bin/python3
import sqlite3 as sql
import bookapi as info

# データベースに接続する
conn = sqlite3.connect('book.db')
c = conn.cursor()

# テーブルの作成
c.execute('''CREATE TABLE book(isbn, title, author, record_date, status, memo)''')

# データの挿入
c.execute("INSERT INTO users VALUES (1, '煌木 太郎', '2001-01-01')")

# 挿入した結果を保存
conn.commit()

# データベースへの接続を終了
conn.close()