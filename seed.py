import random
from datetime import datetime, timedelta
from faker import Faker
from app import app
from models import db, User, Book, Borrow

# 日本語設定
fake = Faker('ja_JP')

def generate_kana(length=3):
    """ランダムなカタカナを生成する（ふりがな用）"""
    kana_list = "アイアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワン"
    return "".join(random.choices(kana_list, k=length))

def seed_data(num_users=15, num_books=20, num_borrows=25):
    with app.app_context():
        print("既存データを削除中...")
        # 外部キー制約があるため Borrow から先に削除
        db.session.query(Borrow).delete()
        db.session.query(User).delete()
        db.session.query(Book).delete()
        db.session.commit()

        print("ユーザーを生成中...")
        users = []
        for _ in range(num_users):
            last_name = fake.last_name()
            first_name = fake.first_name()
            
            # カタカナをランダム生成して「ふりがな」っぽくする
            kana_text = f"{generate_kana()} {generate_kana()}"
            
            # 10%の確率で削除済みユーザーにする
            del_date = fake.date_time_between(start_date='-1M', end_date='now') if random.random() < 0.1 else None

            user = User(
                name=f"{last_name} {first_name}",
                kana=kana_text,
                email=fake.unique.email(),
                created_at=fake.date_time_between(start_date='-1y', end_date='now'),
                deleted_at=del_date
            )
            db.session.add(user)
            users.append(user)

        print("本を生成中...")
        books = []
        genres = ['文学', 'ミステリー', 'SF', 'ビジネス', '歴史', '漫画', '技術書', '料理', '絵本']
        
        for _ in range(num_books):
            # 日本語らしいタイトル（単語を組み合わせたりキャッチコピーを使う）
            if random.random() > 0.5:
                title = f"{fake.word()}の{fake.word()}"
            else:
                title = fake.catch_phrase()
            
            if len(title) > 20: title = title[:20] # 長すぎ防止
            
            # 10%の確率で削除済みの本（絶版など）にする
            del_date = fake.date_time_between(start_date='-1M', end_date='now') if random.random() < 0.1 else None

            book = Book(
                title=title,
                kana=generate_kana(10),
                author=fake.name(),
                genre=random.choice(genres),
                stock=random.randint(1, 10),
                created_at=fake.date_time_between(start_date='-1y', end_date='now'),
                deleted_at=del_date
            )
            db.session.add(book)
            books.append(book)

        # IDを確定させるために一度コミット
        db.session.commit()

        print("貸出履歴を生成中...")
        # 削除されていないユーザーと本から選択（整合性を保つため）
        active_users = [u for u in users if u.deleted_at is None]
        active_books = [b for b in books if b.deleted_at is None]

        if active_users and active_books:
            for _ in range(num_borrows):
                target_user = random.choice(active_users)
                target_book = random.choice(active_books)
                
                # 貸出日：過去60日以内
                borrow_date = fake.date_time_between(start_date='-60d', end_date='now')
                
                # 70%の確率で返却済みとする
                if random.random() < 0.7:
                    return_date = borrow_date + timedelta(days=random.randint(1, 14))
                    if return_date > datetime.now(): return_date = None
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