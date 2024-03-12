-- Goodreads Database Setup

-- Clean up tables if they already exist.
DROP TABLE IF EXISTS book_genres;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS on_shelf;
DROP TABLE IF EXISTS shelves;
DROP TABLE IF EXISTS friends;
DROP TABLE IF EXISTS genre;
DROP TABLE IF EXISTS book_authors;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS books;

-- Represents a user, uniquely identified by their user_id.
CREATE TABLE users (
    -- Unique identifier for a user.
    user_id INT AUTO_INCREMENT,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30),
    email VARCHAR(320) NOT NULL UNIQUE,
    password VARCHAR(30) NOT NULL,
    -- Date the user joined, default time when added
    join_date TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (user_id)
);

-- Represents a book, uniquely identified by its ISBN.
CREATE TABLE books (
    isbn CHAR(13) NOT NULL,
    title VARCHAR(255) NOT NULL,
    publisher VARCHAR(50),
    year_published YEAR,
    synopsis TEXT,
    -- Language code, e.g. "eng" for English.
    language_code CHAR(3),
    num_pages INT,
    cover_photo_url VARCHAR(255),
    -- The series the book is a part of, if any.
    series_name VARCHAR(255), default NULL,
    PRIMARY KEY (isbn)
);

-- Represents a many-to-many relationship between books and authors.
CREATE TABLE book_authors (
    isbn CHAR(13) NOT NULL,
    author_id INT NOT NULL,
    PRIMARY KEY (isbn, author_id),
    FOREIGN KEY (isbn) REFERENCES books(isbn) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE CASCADE
);

-- Represents an author of a book.
CREATE TABLE authors (
    author_id INT AUTO_INCREMENT,
    author_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (author_id)
);

CREATE TABLE genre (
    genre_name VARCHAR(50) UNIQUE,
    PRIMARY KEY (genre_name)
);

-- Represents a friend relationship between two users.
-- A friendship between A & B is represented by (A, B) and (B, A).
CREATE TABLE friends (
    user_id INT NOT NULL,
    friend_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (friend_id) REFERENCES users(user_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, friend_id),
    CHECK (user_id != friend_id)
);

-- Represents a shelf of books for a user.
CREATE TABLE shelves (
    -- Unique identifier for a shelf.
    shelf_id INT AUTO_INCREMENT,
    user_id INT NOT NULL,
    shelf_name VARCHAR(255) NOT NULL,
    is_private BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (shelf_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Represents a book on a shelf.
CREATE TABLE on_shelf (
    -- International Standard Book Numbers (ISBNs) uniquely identify books.
    isbn VARCHAR(13) NOT NULL,
    shelf_id INT NOT NULL,
    PRIMARY KEY (isbn, shelf_id),
    FOREIGN KEY (isbn) REFERENCES books(isbn) ON DELETE CASCADE,
    FOREIGN KEY (shelf_id) REFERENCES shelves(shelf_id) ON DELETE CASCADE
);

CREATE TABLE book_genres (
    isbn VARCHAR(13) NOT NULL,
    genre_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (isbn, genre_name),
    FOREIGN KEY (isbn) REFERENCES books(isbn) ON DELETE CASCADE,
    FOREIGN KEY (genre_name) REFERENCES genre(genre_name) ON DELETE CASCADE
);

-- Represents a review of a book by a user.
CREATE TABLE reviews (
    -- Unique identifier for a review.
    review_id INT AUTO_INCREMENT,
    user_id INT NOT NULL,
    isbn VARCHAR(13) NOT NULL,
    star_rating DECIMAL(2, 1) NOT NULL,
    review_text TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, isbn),
    PRIMARY KEY (review_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (isbn) REFERENCES books(isbn) ON DELETE CASCADE
);


-- Add indexes
CREATE INDEX idx_author ON books(author); 

-- CREATE INDEX idx_isbn ON reviews(isbn);
-- CREATE INDEX idx_isbn ON on_shelf(isbn);
-- CREATE INDEX idx_isbn ON book_genres(isbn);
-- CREATE INDEX idx_isbn ON book_authors(isbn);

