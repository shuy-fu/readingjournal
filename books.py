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

    sql = "INSERT INTO book_classes (book_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [book_id, title, value])

    return book_id

def add_comment(book_id, user_id, comment):
    sql = """INSERT INTO comments (book_id, user_id, comment)
            VALUES (?, ?, ?)"""
    db.execute(sql, [book_id, user_id, comment])

def get_comments(book_id):
    sql = """SELECT comments.comment, users.id user_id, users.username
            FROM comments, users
            WHERE comments.book_id = ? AND comments.user_id = users.id
            ORDER BY comments.id DESC"""
    return db.query(sql, [book_id])

def get_images(book_id):
    sql = "SELECT id FROM images WHERE book_id = ?"
    return db.query(sql, [book_id])

def add_image(book_id, image):
    sql ="INSERT INTO images (book_id, image) VALUES (?, ?)"
    db.execute(sql, [book_id, image])

def get_image(image_id):
    sql = "SELECT image FROM images WHERE id = ?"
    result = db.query(sql, [image_id])
    return result[0][0] if result else None

def remove_image(book_id, image_id):
    sql = "DELETE FROM images WHERE id = ? AND book_id = ?"
    db.execute(sql, [image_id, book_id])

def get_classes(book_id):
    sql = "SELECT title, value FROM book_classes WHERE book_id = ?"
    return db.query(sql, [book_id])

def get_books():
    sql = """SELECT books.id, books.title, users.id user_id, users.username
            FROM books, users
            WHERE books.user_id = users.id
            ORDER BY books.id DESC"""
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
    sql = "DELETE FROM comments WHERE book_id = ?"
    db.execute(sql, [book_id])
    sql = "DELETE FROM images WHERE book_id = ?"
    db.execute(sql, [book_id])
    sql = "DELETE FROM book_classes WHERE book_id = ?"
    db.execute(sql, [book_id])
    sql = "DELETE FROM books WHERE id = ?"
    db.execute(sql, [book_id])

def find_books(query):
    sql = """ SELECT id, title
              FROM books
              WHERE title LIKE ? OR description LIKE ? OR author LIKE ?
              ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like, like])