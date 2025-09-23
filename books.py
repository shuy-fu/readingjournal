import db

def add_book(title, description, rating, user_id, author):
    sql = """INSERT INTO books (title, description, rating, user_id, author)
            VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, description, rating, user_id, author])

def get_books():
    sql = "SELECT id, title FROM books ORDER BY id DESC"
    return db.query(sql)

def get_book(book_id):
    sql = """SELECT books.id,
                    books.title,
                    books.author,
                    books.description,
                    books.rating,
                    users.id user_id,
                    users.username
            FROM books, users
            WHERE books.user_id = users.id AND
                books.id = ?"""
    return db.query(sql, [book_id])[0]

def update_book(book_id, title, description, rating, author):
    sql = """UPDATE books SET title = ?,
                            description = ?,
                            rating = ?,
                            author = ?
                        WHERE id = ?"""
    db.execute(sql, [title, description, rating, author, book_id])