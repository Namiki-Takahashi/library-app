# app.py
import os
from flask import Flask, render_template
from flask_migrate import Migrate
# models.pyからdb読込
from models import db 
# views.pyからBlueprint読込
from application.users.views import users_blueprint

# ==================================================
# インスタンス生成
# ==================================================
app = Flask(__name__)


# ==================================================
# Flaskに対する設定
# ==================================================

# WTFormsを使うために必要
app.config['SECRET_KEY'] = os.urandom(24)

# データベースの保存場所設定
base_dir = os.path.dirname(__file__)
database = 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# dbとappを紐付け
db.init_app(app)
Migrate(app, db)


# ==================================================
# Blueprintの登録
# ==================================================
from application.users.views import users_blueprint
app.register_blueprint(users_blueprint, url_prefix='/users')


# ==================================================
# ルーティング
# ==================================================
@app.route('/')
def show_home():
    return render_template('index.html')


# ==================================================
# 実行
# ==================================================
if __name__ == '__main__':
    app.run()  
