-- SQL Routines
DROP PROCEDURE IF EXISTS add_authors;
DROP PROCEDURE IF EXISTS add_genres;
DROP PROCEDURE IF EXISTS add_book;
DROP FUNCTION IF EXISTS calculate_reading_time;
DROP TRIGGER IF EXISTS auto_add_to_has_read_shelf;

-- Functions

-- Function to calculate the expected reading time of a book
DELIMITER !
CREATE FUNCTION calculate_reading_time(
    num_pages INT,
    -- Reading speed in words per minute
    wpm INT
) RETURNS INT DETERMINISTIC
BEGIN
    DECLARE avg_words_per_page INT DEFAULT 250;
    IF wpm IS NULL THEN
        SET wpm = 200;
    END IF;

    RETURN CEIL((num_pages * avg_words_per_page) / wpm);
END !
DELIMITER ;

-- Procedures to add authors and genres to the database given a delimited string
DELIMITER !
CREATE PROCEDURE add_authors(
    author_names TEXT,
    isbn CHAR(13)
)
BEGIN
    DECLARE curr_author_name VARCHAR(255);
    DECLARE curr_pos INT DEFAULT 1;
    DECLARE sep_pos INT;
    DECLARE curr_id INT;
    DECLARE len INT;

    SET len = LENGTH(author_names);

    WHILE curr_pos < len DO
        -- Locate the next / in the string
        SET sep_pos = LOCATE('/', author_names, curr_pos);
        -- If there is no /, set sep_pos to the end of the string
        IF sep_pos = 0 THEN
            SET sep_pos = len + 1;
        END IF;

        SET curr_author_name = SUBSTRING(author_names, curr_pos, sep_pos - curr_pos);

        # Insert the author if it doesn't exist
        IF NOT EXISTS (SELECT * FROM author WHERE author_name = curr_author_name) THEN
            INSERT INTO author (author_name) VALUES (curr_author_name);
            SET curr_id = LAST_INSERT_ID();
        ELSE
            SELECT author_id INTO curr_id FROM author
                WHERE author_name = curr_author_name;
        END IF;

        INSERT INTO book_author (isbn, author_id) VALUES (isbn, curr_id);

        SET curr_pos = sep_pos + 1;
    END WHILE;
END !
DELIMITER ;

DELIMITER !
CREATE PROCEDURE add_genres(
    genre_names TEXT,
    isbn CHAR(13)
)
BEGIN
    DECLARE curr_genre_name VARCHAR(50);
    DECLARE curr_pos INT DEFAULT 1;
    DECLARE sep_pos INT;
    DECLARE len INT;

    SET len = LENGTH(genre_names);

    WHILE curr_pos < len DO
        SET sep_pos = LOCATE('/', genre_names, curr_pos);
        IF sep_pos = 0 THEN
            SET sep_pos = len + 1;
        END IF;

        SET curr_genre_name = SUBSTRING(genre_names, curr_pos, sep_pos - curr_pos);

        # Insert the genre if it doesn't exist
        IF NOT EXISTS (SELECT * FROM genre WHERE genre_name = curr_genre_name) THEN
            INSERT INTO genre (genre_name) VALUES (curr_genre_name);
        END IF;

        INSERT INTO book_genre (isbn, genre_name) VALUES (isbn, curr_genre_name);

        SET curr_pos = sep_pos + 1;
    END WHILE;
END !
DELIMITER ;

-- Procedure to add a new book
DELIMITER !
CREATE PROCEDURE add_book(
    isbn CHAR(13),
    title VARCHAR(255),
    publisher VARCHAR(100),
    year_published YEAR,
    language_code CHAR(3),
    num_pages INT,
    synopsis TEXT,
    cover_photo_url VARCHAR(255),
    series_name VARCHAR(255),
    -- The authors and genres are passed as /-separated strings
    author_names TEXT,
    genre_names TEXT
)
BEGIN
    -- Insert the book
    INSERT INTO
        book (isbn, title, publisher, year_published, synopsis, language_code,
              num_pages, cover_photo_url, series_name)
        VALUES (isbn, title, publisher, year_published, synopsis, language_code,
                num_pages, cover_photo_url, series_name);

    -- Insert the authors
    CALL add_authors(author_names, isbn);

    -- Insert the genres
    CALL add_genres(genre_names, isbn);
END !
DELIMITER ;

-- Triggers

-- Add a trigger to add a book to "Has Read" after a user reviews it
-- If a user is reviewing a book, it should mean they have read it
DELIMITER !
CREATE TRIGGER auto_add_to_has_read_shelf
AFTER INSERT ON review
FOR EACH ROW
BEGIN
    -- Check if the book is not in has read for the user
    IF NOT EXISTS (
        SELECT 1
        FROM on_shelf NATURAL JOIN shelf
        WHERE isbn = NEW.isbn
        AND user_id = NEW.user_id
        AND shelf_name = 'Has Read'
    ) THEN
        -- Insert the book into the has read shelf
        INSERT INTO on_shelf (isbn, shelf_id)
        SELECT NEW.isbn, shelf_id
        FROM shelf
        WHERE user_id = NEW.user_id
        AND shelf_name = 'Has Read'
        LIMIT 1;
    END IF;
END !
DELIMITER ;