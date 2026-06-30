from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Book, Borrow
from application.books.forms import BookForm
from datetime import datetime

# Blueprintの定義
books_blueprint = Blueprint('books', __name__, template_folder='templates')

# --- 一覧表示 ---
@books_blueprint.route('/')
def index():
    edit_id = request.args.get('edit_id', type=int)
    list_books = Book.query.filter(Book.deleted_at.is_(None)).all()
    form = BookForm()
    return render_template('books/list.html', 
                           list_books=list_books, 
                           edit_id=edit_id, 
                           form=form)

# --- 新規登録 ---
@books_blueprint.route('/new', methods=['GET', 'POST'])
def new_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data, 
                    kana=form.kana.data,
                    genre=form.genre.data,
                    author=form.author.data,
                    stock=form.stock.data)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('books.index')) # Blueprint名.関数名
    return render_template('books/new.html', form=form)

# --- 削除 ---
@books_blueprint.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):

    
    borrowing = Borrow.query.filter_by(
        book_id=book_id,
        returned_at=None
    ).first()

    if borrowing:
        return redirect(url_for('books.index'))


    book = Book.query.get(book_id)
    if book.deleted_at is None: # すでに削除済みかどうか
        # 現在時刻登録
        book.deleted_at = datetime.now()
    db.session.commit()
    return redirect(url_for('books.index'))

# --- 確定ボタン ---
@books_blueprint.route('/update/<int:book_id>', methods=['POST'])
def update_book(book_id):
    book = Book.query.get(book_id)
    form = BookForm()
    if form.validate_on_submit():
        book.title = form.title.data
        book.kana = form.kana.data
        book.genre = form.genre.data
        book.author = form.author.data
        book.stock = form.stock.data
        db.session.commit()
        return redirect(url_for('books.index'))
    
    # バリデーションエラー時
    list_books = Book.query.filter(Book.deleted_at == None).all()
    return render_template('books/list.html', 
                           list_books=list_books, 
                           edit_id=book_id, 
                           form=form)