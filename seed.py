# seed.py
import random
from faker import Faker
from app import app
from models import db, User, Book

# 日本語のフェイクデータを生成する設定
fake = Faker('ja_JP')

def seed_data(num_users=50, num_books=50):
    with app.app_context():

        # 既存データを全削除
        User.query.delete()
        Book.query.delete()
        db.session.commit()


        print("データを生成中...")

        # 1. ユーザーデータの作成
        for _ in range(num_users):
            user = User(
                name=fake.name(),
                email=fake.unique.email()
            )
            db.session.add(user)

        # 2. 本データの作成
        genres = ['文学', 'ミステリー', 'SF', 'ビジネス', '歴史', '漫画', '技術書']
        for _ in range(num_books):
            book = Book(
                title=fake.catch_phrase(), # それっぽいキャッチコピーをタイトルに流用
                author=fake.name(),
                genre=random.choice(genres),
                stock=random.randint(0, 10)
            )
            db.session.add(book)

        # データベースに反映
        db.session.commit()
        print(f"完了しました！（ユーザー:{num_users}件、本:{num_books}件）")

if __name__ == '__main__':
    seed_data(1000, 1000) # 好きな件数を指定