import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import books

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_books = books.get_books()
    return render_template("index.html", books=all_books)

@app.route("/find_book")
def find_book():
    query = request.args.get("query")
    if query:
        results = books.find_books(query)
    else:
        query = ""
        results = []
    return render_template("find_book.html", query=query, results=results)

@app.route("/book/<int:book_id>")
def show_book(book_id):
    book = books.get_book(book_id)
    if not book:
        abort(404)
    return render_template("show_book.html", book=book)

@app.route("/new_book")
def new_book():
    require_login()
    return render_template("new_book.html")

@app.route("/create_book", methods=["POST"])
def create_book():
    require_login()

    title = request.form["title"]
    description = request.form["description"]
    rating = request.form["rating"]
    user_id = session["user_id"]
    author = request.form["author"]

    books.add_book(title, description, rating, user_id, author)

    return redirect("/")

@app.route("/edit_book/<int:book_id>")
def edit_book(book_id):
    require_login()
    book = books.get_book(book_id)
    if not book:
        abort(404)
    if book["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_book.html", book=book)

@app.route("/update_book", methods=["POST"])
def update_book():
    require_login()
    book_id = request.form["book_id"]
    book = books.get_book(book_id)
    if not book:
        abort(404)
    if book["user_id"] != session["user_id"]:
        abort(403)

    title = request.form["title"]
    description = request.form["description"]
    rating = request.form["rating"]
    author = request.form["author"]

    books.update_book(book_id, title, description, rating, author)

    return redirect("/book/" + str(book_id))

@app.route("/remove_book/<int:book_id>", methods=["GET", "POST"])
def remove_book(book_id):
    require_login()
    book = books.get_book(book_id)
    if not book:
        abort(404)
    if book["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_book.html", book=book)
    if request.method == "POST":
        if "remove" in request.form:
            books.remove_book(book_id)
            return redirect("/")
        else:
            return redirect("/book/" + str(book_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "ERROR: passwords do not match"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "ERROR: username is taken"

    return "Account created"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "ERROR: invalid username or password"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")