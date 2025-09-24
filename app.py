import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import config
import db
import books
import re
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_books = books.get_books()
    return render_template("index.html", books=all_books)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    books = users.get_books(user_id)
    return render_template("show_user.html", user=user, books=books)

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
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if len(description) > 1000:
        abort(403)
    rating = request.form["rating"]
    if not re.search("^(10|[1-9])$", rating):
        abort(403)
    user_id = session["user_id"]
    author = request.form["author"]
    if not author or len(author) > 50:
        abort(403)

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
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    rating = request.form["rating"]
    if not re.search("^(10|[1-9])$", rating):
        abort(403)
    author = request.form["author"]
    if not author or len(author) > 50:
        abort(403)

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

    try:
        users.create_user(username, password1)
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

        user_id = users.check_login(username, password)
        if user_id:
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