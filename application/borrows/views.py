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
    if form.validate_on_submit():
        # 名前からUserレコード取得
        user = User.query.filter_by(name=form.name.data).first()
        # タイトルからBookレコード取得
        book = Book.query.filter_by(title=form.book.data).first()

        # 3. 存在チェック
        if not user:
            form.name.errors.append("指定された利用者は存在しません。")
        elif not book:
            form.book.errors.append("指定された本は存在しません。")
        elif book.stock <= 0: # 在庫チェック
            form.book.errors.append("この本は在庫切れです。")
        else:
            # 貸出レコード作成
            new_borrow_record = Borrow(user_id=user.user_id, book_id=book.book_id)
            # 在庫デクリメント
            book.stock -= 1
            
            db.session.add(new_borrow_record)
            db.session.commit()
            return redirect(url_for('borrows.index'))
    # エラー時
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
