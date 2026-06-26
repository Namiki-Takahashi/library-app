# app.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User

# ==================================================
# インスタンス生成
# ==================================================
app = Flask(__name__)

# ==================================================
# Flaskに対する設定
# ==================================================
app.config['SECRET_KEY'] = os.urandom(24)
base_dir = os.path.dirname(__file__)
database = 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
Migrate(app, db)

# ==================================================
# DB作成
# ==================================================
def init_db():
       
    with app.app_context():

        print(f"消去対象のテーブル: {db.metadata.tables.keys()}") 

        print('(1)テーブルを削除してから作成')
        db.drop_all()
        db.create_all()

        # データ作成
        print('(2)データ登録：実行')
        user01 = User(name='ねずみ', email='mouse@mouse.com')
        user02 = User(name='うし', email='beaf@beaf.com')
        user03 = User(name='とら', email='tiger@tiger.com')
        db.session.add_all([user01, user02, user03])
        db.session.commit()

# ==================================================
# 実行
# ==================================================
if __name__ == '__main__':
    init_db()           
