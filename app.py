# app.py
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from application.users.forms import UserForm
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
# ユーザー
# ==================================================
# 一覧
@app.route('/users')
def index():
    # ユーザー一覧を取得
    list_users = User.query.all()
    return render_template('users/list.html', list_users=list_users)

# 登録処理
@app.route('/users/new', methods=['GET', 'POST'])
def new_user():
    form = UserForm(request.form)
    # POST
    if request.method == 'POST':
        # 入力取得
        name = form.name.data
        email = form.email.data
        user = User(name=name, email=email )
        # 登録
        db.session.add(user)
        db.session.commit()
        # 一覧へ
        return redirect(url_for('index'))
    # GET
    return render_template('users/new.html', form=form)

# 削除処理
@app.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('index'))


# ==================================================
# 実行
# ==================================================
if __name__ == '__main__':
    app.run()           
