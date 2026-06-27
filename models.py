# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class User(db.Model):
    __tablename__ = 'users'
    
    # 利用者ID
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 利用者名
    name = db.Column(db.String(200), nullable=False)
    # メール
    email = db.Column(db.String(200), nullable=False)  

    # ユーザーの貸出履歴取得用
    borrows = db.relationship('Borrow', backref='user', lazy=True)

    # 表示用
    def __str__(self):
        return f'利用者ID：{self.user_id} 利用者名：{self.name} メール：{self.email}'
    

class Book(db.Model):
    __tablename__ = 'books'
    
    # 本ID
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # タイトル
    title = db.Column(db.String(200), nullable=False)
    # 著者
    author = db.Column(db.String(200), nullable=False)  
    # ジャンル
    genre = db.Column(db.String(200), nullable=False) 
    # 在庫冊数
    stock = db.Column(db.Integer, nullable=False) 

    # 本の貸出履歴取得用
    borrows = db.relationship('Borrow', backref='book', lazy=True)

    # 表示用
    def __str__(self):
        return f'本ID：{self.book_id} タイトル：{self.title} 著者：{self.author} ジャンル：{self.genre} 在庫冊数：{self.stock}'
    


class Borrow(db.Model):
    __tablename__ = 'borrows'
    
    # 貸出ID
    borrows_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # 利用者ID
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    # 本ID
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    
    # 貸出日
    borrowed_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    
    # 返却日
    returned_at = db.Column(db.DateTime, nullable=True)

    def __str__(self):
        status = "返却済" if self.returned_at else "貸出中"
        return f'貸出ID：{self.borrows_id} 状態：{status}'
    