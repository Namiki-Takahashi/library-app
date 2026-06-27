# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class User(db.Model):
    # テーブル名
    __tablename__ = 'users'
    
    # 利用者ID
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 利用者名
    name = db.Column(db.String(200), nullable=False)
    # メール
    email = db.Column(db.String(200), nullable=False)  

    # 表示用
    def __str__(self):
        return f'利用者ID：{self.user_id} 利用者名：{self.name} メール：{self.email}'
    

class Book(db.Model):
    # テーブル名
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

    # 表示用
    def __str__(self):
        return f'本ID：{self.book_id} タイトル：{self.title} 著者：{self.author} ジャンル：{self.genre} 在庫冊数：{self.stock}'