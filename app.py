# app.py
import os
from flask import Flask, render_template, request, redirect, url_for
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
# Flaskに対する設定
# ==================================================
# 一覧
@app.route('/')
def index():
    # ユーザー一覧を取得
    list_users = User.query.all()
    return render_template('users/list.html', list_users=list_users)

@app.route('/new', methods=['GET', 'POST'])
def new_user():
    # POST
    if request.method == 'POST':
        # 入力取得
        name = request.form['name']
        email = request.form['email']
        user = User(name = name, email = email )
        # 登録
        db.session.add(user)
        db.session.commit()
        # 一覧へ
        return redirect(url_for('new_user'))
    # GET
    return render_template('users/new.html')


# ==================================================
# 実行
# ==================================================
if __name__ == '__main__':
    app.run()           
