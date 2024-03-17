-- Goodreads Database Setup
CREATE DATABASE IF NOT EXISTS goodreads;
USE goodreads;

-- Clean up tables if they already exist.
DROP VIEW IF EXISTS book_review_stats;
DROP TABLE IF EXISTS book_genre;
DROP TABLE IF EXISTS review;
DROP TABLE IF EXISTS on_shelf;
DROP TABLE IF EXISTS shelf;
DROP TABLE IF EXISTS friend;
DROP TABLE IF EXISTS genre;
DROP TABLE IF EXISTS book_author;
DROP TABLE IF EXISTS author;
DROP TABLE IF EXISTS user_info;
DROP TABLE IF EXISTS book;

-- Represents a user, uniquely identified by their user_id.
CREATE TABLE user_info (
    -- Unique identifier for a user.
    user_id INT AUTO_INCREMENT,
    -- First name, required.
    first_name VARCHAR(30) NOT NULL,
    -- Last name, optional; NULL if not provided.
    last_name VARCHAR(30),
    -- Email address, required and unique.
    email VARCHAR(320) NOT NULL UNIQUE,
    -- Password salt, will be 8 characters all the time.
    salt CHAR(8) NOT NULL,
    -- Using SHA-2 with 256-bit hashes; hash is a hex string.
    password_hash BINARY(64) NOT NULL,
    -- Admin status, default to false
    is_admin BOOLEAN DEFAULT FALSE,
    -- Date the user joined, default time when added
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id)
);

-- Represents a book, uniquely identified by its ISBN.
CREATE TABLE book (
    -- International Standard Book Number (ISBN).
    isbn CHAR(13),
    title VARCHAR(255) NOT NULL,
    -- Book publisher, e.g. "Penguin Books"; NULL if unknown/self-published.
    publisher VARCHAR(100),
    -- Year the book was published; NULL if unknown.
    year_published YEAR,
    -- Book summary; NULL if not available.
    synopsis TEXT,
    -- Language code, e.g. "eng" for English.
    language_code CHAR(3),
    num_pages INT,
    -- URL of the book's cover photo
    cover_photo_url VARCHAR(255),
    -- The series the book is a part of, if any; NULL if not part of a series.
    series_name VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (isbn)
);

-- Represents an author of a book.
CREATE TABLE author (
    author_id INT AUTO_INCREMENT,
    author_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (author_id)
);

-- Represents a many-to-many relationship between books and authors.
CREATE TABLE book_author (
    isbn CHAR(13),
    author_id INT,
    PRIMARY KEY (isbn, author_id),
    FOREIGN KEY (isbn) REFERENCES book(isbn) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES author(author_id) ON DELETE CASCADE
);

-- Represents a genre of a book.
CREATE TABLE genre (
    genre_name VARCHAR(50) UNIQUE,
    PRIMARY KEY (genre_name)
);

-- Represents a many-to-many relationship between books and genres.
CREATE TABLE book_genre (
    isbn CHAR(13),
    genre_name VARCHAR(50),
    PRIMARY KEY (isbn, genre_name),
    FOREIGN KEY (isbn) REFERENCES book(isbn) ON DELETE CASCADE,
    FOREIGN KEY (genre_name) REFERENCES genre(genre_name) ON DELETE CASCADE
);

-- Represents a friend relationship between two users.
-- A friendship between A & B is represented by (A, B) and (B, A).
CREATE TABLE friend (
    user_id INT,
    friend_id INT,
    FOREIGN KEY (user_id) REFERENCES user_info(user_id) ON DELETE CASCADE,
    FOREIGN KEY (friend_id) REFERENCES user_info(user_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, friend_id),
    CHECK (user_id != friend_id)
);

-- Represents a shelf of books for a user.
CREATE TABLE shelf (
    -- Unique identifier for a shelf.
    shelf_id INT AUTO_INCREMENT,
    user_id INT,
    shelf_name VARCHAR(255) NOT NULL,
    is_private BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (shelf_id),
    FOREIGN KEY (user_id) REFERENCES user_info(user_id) ON DELETE CASCADE,
    -- ensure shelf name is unique for each user
    UNIQUE (user_id, shelf_name)
);

-- Represents a book on a shelf.
CREATE TABLE on_shelf (
    -- International Standard Book Numbers (ISBNs) uniquely identify books.
    isbn CHAR(13),
    shelf_id INT,
    PRIMARY KEY (isbn, shelf_id),
    FOREIGN KEY (isbn) REFERENCES book(isbn) ON DELETE CASCADE,
    FOREIGN KEY (shelf_id) REFERENCES shelf(shelf_id) ON DELETE CASCADE,
    -- ensure a book is only on a shelf once
    UNIQUE (isbn, shelf_id)
);

-- Represents a review of a book by a user.
CREATE TABLE review (
    -- Unique identifier for a review.
    review_id INT AUTO_INCREMENT,
    user_id INT,
    isbn CHAR(13),
    star_rating DECIMAL(2, 1) NOT NULL,
    -- The review text; NULL if none.
    review_text TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- A user can only review a book once.
    UNIQUE (user_id, isbn),
    PRIMARY KEY (review_id),
    FOREIGN KEY (user_id) REFERENCES user_info(user_id) ON DELETE CASCADE,
    FOREIGN KEY (isbn) REFERENCES book(isbn) ON DELETE CASCADE
);


-- Add indexes
CREATE INDEX idx_email ON user_info(email);

-- Create book statistics VIEW
CREATE VIEW book_review_stats AS
SELECT isbn, AVG(star_rating) AS average_rating,
    COUNT(*) AS num_ratings, COUNT(review_text) AS num_reviews
FROM review
GROUP BY isbn;

/* CREATE INDEX idx_author ON books(author); */

-- CREATE INDEX idx_isbn ON reviews(isbn);
-- CREATE INDEX idx_isbn ON on_shelf(isbn);
-- CREATE INDEX idx_isbn ON book_genres(isbn);
-- CREATE INDEX idx_isbn ON book_authors(isbn);

