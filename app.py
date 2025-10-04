import secrets
import sqlite3
from flask import Flask
from flask import abort, flash,  make_response, redirect, render_template, request, session
import markupsafe
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

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

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
    classes = books.get_classes(book_id)
    comments = books.get_comments(book_id)
    images = books.get_images(book_id)
    return render_template("show_book.html", book=book, classes=classes, comments=comments, images=images)

@app.route("/image/<int:image_id>")
def show_image(image_id):
    image = books.get_image(image_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/png")
    return response

@app.route("/new_book")
def new_book():
    require_login()
    classes = books.get_all_classes()
    return render_template("new_book.html", classes=classes)

@app.route("/create_book", methods=["POST"])
def create_book():
    require_login()
    check_csrf()

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

    all_classes = books.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

    book_id = books.add_book(title, description, rating, user_id, author, classes)

    return redirect("/book/" + str(book_id))

@app.route("/create_comment", methods=["POST"])
def create_comment():
    require_login()
    check_csrf()

    comment = request.form["comment"]
    book_id = request.form["book_id"]
    book = books.get_book(book_id)
    if not book:
        abort(403)
    user_id = session["user_id"]

    books.add_comment(book_id, user_id, comment)

    return redirect("/book/" + str(book_id))

@app.route("/edit_book/<int:book_id>")
def edit_book(book_id):
    require_login()
    book = books.get_book(book_id)
    if not book:
        abort(404)
    if book["user_id"] != session["user_id"]:
        abort(403)

    all_classes = books.get_all_classes()
    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""
    for entry in books.get_classes(book_id):
        classes[entry["title"]] = entry["value"]

    return render_template("edit_book.html", book=book, classes=classes, all_classes=all_classes)

@app.route("/images/<int:book_id>")
def edit_images(book_id):
    require_login()
    book = books.get_book(book_id)
    if not book:
        abort(404)
    if book["user_id"] != session["user_id"]:
        abort(403)

    images = books.get_images(book_id)

    return render_template("images.html", book=book, images=images)

@app.route("/add_image", methods=["POST"])
def add_image():
    require_login()
    check_csrf()

    book_id = request.form["book_id"]
    book = books.get_book(book_id)
    if not book:
        abort(404)
    if book["user_id"] != session["user_id"]:
        abort(403)

    file = request.files["image"]
    if not file.filename.endswith(".png"):
        flash("ERROR: invalid file format")
        return redirect("/images/" + str(book_id))

    image = file.read()
    if len(image) > 100 * 1024:
        flash("ERROR: image too large")
        return redirect("/images/" + str(book_id))

    books.add_image(book_id, image)
    return redirect("/images/" + str(book_id))

@app.route("/remove_images", methods=["POST"])
def remove_images():
    require_login()
    check_csrf()

    book_id = request.form["book_id"]
    book = books.get_book(book_id)
    if not book:
        abort(404)
    if book["user_id"] != session["user_id"]:
        abort(403)

    for image_id in request.form.getlist("image_id"):
        books.remove_image(book_id, image_id)

    return redirect("/images/" + str(book_id))

@app.route("/update_book", methods=["POST"])
def update_book():
    require_login()
    check_csrf()

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
    if len(description) > 1000:
        abort(403)
    rating = request.form["rating"]
    if not re.search("^(10|[1-9])$", rating):
        abort(403)
    author = request.form["author"]
    if not author or len(author) > 50:
        abort(403)

    all_classes = books.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

    books.update_book(book_id, title, description, rating, author, classes)

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
        check_csrf()
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
        flash("ERROR: passwords do not match")
        return redirect("/register")
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("ERROR: username is taken")
        return redirect("/register")

    return redirect("/")

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
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("ERROR: invalid username or password")
            return redirect("/login")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")