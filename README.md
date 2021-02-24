# 環境
DB: mongoDB  
フレームワーク: Python Flask

# 機能
- 文献情報は自前DBに格納
    - 'bookdb'
    - なければNDLから引っ張ってくる
    - タイトルでの検索(要ElasticSearch)
- NDL検索(自前DBになければ)
    - ISBNから検索
    - タイトルから検索
        - 検索結果からISBNを取得して自前DBに格納する
        - 検索結果を再利用できるように該当以外も格納しておく
- 文献情報とは別のDBに読了情報を格納
    - 'statusdb'
    - ステータスはread/reading/unread/wish
- マルチユーザー対応
    - Flaskログイン管理の勉強のため
    - ログイン必須
    - 登録機能はなくてもいい
- できたらAPI(?)にも対応したい

# 挙動について
- /
    - toppage
- /login
- /logout
- /book?q=ISBN  
    - ISBNから文献情報を返す
    - できればこの画面で読了状態を確認･更新したい
        - /book?q=(ISBN)&status=(read)  (POST)など
- /search  
    - タイトルで検索する画面  
    - ISBNがわからないとき用
    - 特定できたら /bookにリダイレクトさせる
- /my
    - /read, /reading, /unread, /wish
    - 読了状態の一覧を表示する

# 構造
bookmeter/
|- app
|  |- app.py
|  |- modules.py
|  |- templates/
|  -- static/

# 見た目について
HTML/CSSわからん．
