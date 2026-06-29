from flask import Blueprint, render_template, request, redirect, url_for
from models import db, User
from application.users.forms import UserForm
from datetime import datetime

# Blueprintの定義
users_blueprint = Blueprint('users', __name__, template_folder='templates')

# --- 一覧表示 ---
@users_blueprint.route('/')
def index():
    edit_id = request.args.get('edit_id', type=int)
    list_users = User.query.filter(User.deleted_at.is_(None)).all()
    form = UserForm()
    return render_template('users/list.html', 
                           list_users=list_users, 
                           edit_id=edit_id, 
                           form=form)

# --- 新規登録 ---
@users_blueprint.route('/new', methods=['GET', 'POST'])
def new_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, 
                    kana=form.kana.data,
                    email=form.email.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.index')) # Blueprint名.関数名
    return render_template('users/new.html', form=form)

# --- 削除 ---
@users_blueprint.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user.deleted_at is None: # すでに削除済みかどうか
        # 現在時刻登録
        user.deleted_at = datetime.now()

    db.session.commit()
    return redirect(url_for('users.index'))

# --- 確定ボタン ---
@users_blueprint.route('/update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    user = User.query.get(user_id)
    form = UserForm()
    if form.validate_on_submit():
        user.name = form.name.data
        user.kana = form.kana.data
        user.email = form.email.data
        db.session.commit()
        return redirect(url_for('users.index'))
    
    # バリデーションエラー時
    list_users = User.query.filter(User.deleted_at == None).all()
    return render_template('users/list.html', 
                           list_users=list_users, 
                           edit_id=user_id, 
                           form=form)