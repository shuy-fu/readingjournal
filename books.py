import db

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes

def add_book(title, description, rating, user_id, author, classes):
    sql = """INSERT INTO books (title, description, rating, user_id, author)
            VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, description, rating, user_id, author])

    book_id = db.last_insert_id()

    all_classes = get_all_classes()

    sql = "INSERT INTO book_classes (book_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [book_id, title, value])

def get_classes(book_id):
    sql = "SELECT title, value FROM book_classes WHERE book_id = ?"
    return db.query(sql, [book_id])

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
    result = db.query(sql, [book_id])
    return result[0] if result else None

def update_book(book_id, title, description, rating, author, classes):
    sql = """UPDATE books SET title = ?,
                            description = ?,
                            rating = ?,
                            author = ?
                        WHERE id = ?"""
    db.execute(sql, [title, description, rating, author, book_id])

    sql = "DELETE FROM book_classes WHERE book_id = ?"
    db.execute(sql, [book_id])
    sql = "INSERT INTO book_classes (book_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [book_id, title, value])

def remove_book(book_id):
    sql = "DELETE FROM books WHERE id = ?"
    db.execute(sql, [book_id])

def find_books(query):
    sql = """ SELECT id, title
              FROM books
              WHERE title LIKE ? OR description LIKE ? OR author LIKE ?
              ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like, like])