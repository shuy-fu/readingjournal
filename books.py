import db

def add_book(title, description, rating, user_id, author):
    sql = """INSERT INTO books (title, description, rating, user_id, author)
            VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, description, rating, user_id, author])