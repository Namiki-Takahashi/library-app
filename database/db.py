import os
import sqlite3

# ==================================================
# DBファイル作成
# ==================================================
base_dir = os.path.dirname(__file__)
database = os.path.join(base_dir, 'data.sqlite')

# ==================================================
# SQL
# ==================================================
# 接続
conn = sqlite3.connect(database)
print('▼▼▼▼▼▼▼▼▼▼ コネクションの接続 ▼▼▼▼▼▼▼▼▼▼')
print()
# カーソル
cur = conn.cursor()
# テーブル削除SQL
drop_sql = """
    DROP TABLE IF EXISTS users;
"""
cur.execute(drop_sql)
print('（１）対象テーブルがあれば削除')
# テーブル作成SQL
create_sql = """
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name STRING UNIQUE NOT NULL, 
        email STRING UNIQUE NOT NULL)
    """
cur.execute(create_sql)
print('（２）テーブル作成')
# データ登録SQL
insert_sql = """
    INSERT INTO users (name, email) VALUES (?, ?)
    """
insert_data_list = [
    ('あいうえお', "aiueo@hoge.com"), ('ABCDEF', "a-bc.def@hoge.com"), ('壱弐参四伍六七八', "1234-5678@hoge.com")
]
cur.executemany(insert_sql, insert_data_list)
conn.commit()
print('（３）データ登録：実行')
# データ参照（全件）SQL
select_all_sql = """
    SELECT * FROM users
    """
cur.execute(select_all_sql)
print('（４）---------- 全件取得：実行 ----------')
data = cur.fetchall()
print(data)

# 閉じる
conn.close()
print()
print('▲▲▲▲▲▲▲▲▲▲ コネクションを閉じる ▲▲▲▲▲▲▲▲▲▲')
