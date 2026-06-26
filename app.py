import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# ==================================================
# インスタンス生成
# ==================================================
app = Flask(__name__)

# ==================================================
# Flaskに対する設定
# ==================================================
import os
# 乱数を設定
app.config['SECRET_KEY'] = os.urandom(24)
base_dir = os.path.dirname(__file__)
database = 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ★db変数を使用してSQLAlchemyを操作できる
db = SQLAlchemy(app)
# ★「flask_migrate」を使用できる様にする
Migrate(app, db)

#==================================================
# モデル
#==================================================
# 課題
class Task(db.Model):
    # テーブル名
    __tablename__ = 'tasks'
    
    # 課題ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 内容
    content = db.Column(db.String(200), nullable=False)

    # ▼▼▼ リスト7.4で追加 ▼▼▼
    # 完了フラグ
    is_completed = db.Column(db.Boolean, default=False)  

    # 表示用
    def __str__(self):
        return f'課題ID：{self.id} 内容：{self.content} 完了フラグ：{self.is_completed}'
    # ▲▲▲ リスト7.4で追加 ▲▲▲
   
    # ▼▼▼ リスト7.3で追加 ▼▼▼
# ==================================================
# CRUD操作
# ==================================================
# 登録
def insert():
    with app.app_context():
        print('========== 3件登録 ==========')
        # データ作成
        print('（１）データ登録：実行')
        task01 = Task(content='風呂掃除')
        task02 = Task(content='洗濯')
        task03 = Task(content='買い物')
        db.session.add_all([task01, task02, task03])
        db.session.commit()

# ==================================================
# 実行
# ==================================================
if __name__ == '__main__':
    insert()               # データ登録
# ▲▲▲ リスト7.3で追加 ▲▲▲