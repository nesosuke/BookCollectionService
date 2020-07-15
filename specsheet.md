## v0.0.1案

- `convert.py`
    入力がISBN10ならISBN13に変換、ISBN13はそのままにする
- `getinfo.py`
    ISBN13から書籍情報の取得(api.openbd.jpを利用)
- `addcount.py`
    isbnを引数として`record ={'isbn': count}`の辞書にあれば `count += 1`、なければ作成
- `getcount.py`
    isbnを引数として辞書`record`からcount数の表示


## やりたいこと

1. 記録部分
ISBN入力[^1]
→書籍情報取得 ... `openbd.py`でできてる
    - `isbn`: ISBN13
    - `title`: 書名
    - `author`: 作者、
    - `record_date` 記録日、
    - `status`: 読了ステータス、
    - `memo`: メモ欄 をDBに格納

必要そう: SQL


2. 検索機能
    - ISBN、書名、作者、ステータス、記録日でのソート・検索
必要そう: SQL

3. 表示部分
ブラウザで表示
必要そう: HTML,CSS

[^1]: 派生機能iOSアプリで1次元バーコード読み取り → ISBN取得 やりたい