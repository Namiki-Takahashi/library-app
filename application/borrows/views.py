from flask import Blueprint, render_template, redirect, url_for
from models import db, Borrow, User, Book
from application.borrows.forms import BorrowForm
from datetime import datetime

# Blueprintの定義
borrows_blueprint = Blueprint('borrows', __name__, template_folder='templates')

# --- 一覧表示 ---
@borrows_blueprint.route('/')
def index():
    active_borrows = Borrow.query.filter(Borrow.returned_at.is_(None)).all()
    
    from application.borrows.forms import BorrowForm
    form = BorrowForm()
    
    return render_template('borrows/list.html', list_borrows=active_borrows, form=form)

# --- 新規登録 ---
@borrows_blueprint.route('/new', methods=['GET', 'POST'])
def new_borrow():
    form = BorrowForm()

    # 利用者・本のプルダウン作成
    form.user_id.choices = [(u.user_id, u.name) for u in User.query.all()]
    form.book_id.choices = [(b.book_id, f"{b.title} (在庫:{b.stock}冊)") for b in Book.query.all()]

    if form.validate_on_submit():
        user = User.query.get(form.user_id.data)
        book = Book.query.get(form.book_id.data)

        if book.stock <= 0:
            form.book_id.errors.append("在庫切れのため貸出不可")
        else:
            new_record = Borrow(user_id=user.user_id, book_id=book.book_id)
            book.stock -= 1
            
            db.session.add(new_record)
            db.session.commit()
            return redirect(url_for('borrows.index'))

    return render_template('borrows/new.html', form=form)


# --- 返却 ---
@borrows_blueprint.route('/return/<int:borrows_id>', methods=['POST'])
def return_book(borrows_id):
    borrow = Borrow.query.get(borrows_id)
    if borrow.returned_at is None: # すでに返却済みかどうか
        # 現在時刻登録
        borrow.returned_at = datetime.now()
        
        # 在庫インクリメント
        borrow.book.stock += 1
        db.session.commit()

    return redirect(url_for('borrows.index'))
