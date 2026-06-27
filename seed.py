import random
from datetime import datetime, timedelta
from faker import Faker
from app import app
from models import db, User, Book, Borrow

# 日本語設定
fake = Faker('ja_JP')

def seed_data(num_users=10, num_books=10, num_borrows=10):
    with app.app_context():
        print("既存データを削除中...")
        db.session.query(Borrow).delete()
        db.session.query(User).delete()
        db.session.query(Book).delete()
        db.session.commit()

        print("ユーザーと本を生成中...")
        # 1. ユーザー作成
        users = []
        for _ in range(num_users):
            user = User(name=fake.name(), email=fake.unique.email())
            db.session.add(user)
            users.append(user)

        # 2. 本作成
        books = []
        genres = ['文学', 'ミステリー', 'SF', 'ビジネス', '歴史', '漫画', '技術書']
        for _ in range(num_books):
            book = Book(
                title=fake.catch_phrase(),
                author=fake.name(),
                genre=random.choice(genres),
                stock=random.randint(1, 10)
            )
            db.session.add(book)
            books.append(book)

        # IDを確定させるために一度コミット
        db.session.commit()

        print("貸出履歴を生成中...")
        # 3. 貸出履歴作成
        for _ in range(num_borrows):
            target_user = random.choice(users)
            target_book = random.choice(books)
            
            # 貸出日：過去60日以内のランダムな日時
            borrow_date = fake.date_time_between(start_date='-60d', end_date='now')
            
            # 返却日の設定（70%の確率で返却済み、30%は貸出中とする）
            if random.random() < 0.7:
                # 返却日は貸出日の1〜14日後
                return_date = borrow_date + timedelta(days=random.randint(1, 14))
                # 未来の日付にならないよう調整
                if return_date > datetime.now():
                    return_date = None
            else:
                return_date = None

            borrow = Borrow(
                user_id=target_user.user_id,
                book_id=target_book.book_id,
                borrowed_at=borrow_date,
                returned_at=return_date
            )
            db.session.add(borrow)

        db.session.commit()
        print(f"完了！ (ユーザー:{num_users}件, 本:{num_books}件, 貸出履歴:{num_borrows}件)")

if __name__ == '__main__':
    seed_data()