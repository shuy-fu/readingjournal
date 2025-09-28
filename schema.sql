CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    rating INTEGER,
    user_id INTEGER REFERENCES users,
    author TEXT
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    book_id INTEGER REFERENCES books,
    user_id INTEGER REFERENCES users,
    comment TEXT
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE book_classes (
    id INTEGER PRIMARY KEY,
    book_id INTEGER REFERENCES books,
    title TEXT,
    value TEXT
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    book_id INTEGER REFERENCES books,
    image BLOB
);