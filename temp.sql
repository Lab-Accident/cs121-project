-- List books ordered by average rating
CREATE VIEW book_rating_stats AS
SELECT b.isbn, AVG(r.star_rating) AS average_rating
FROM book b
LEFT JOIN review r ON b.isbn = r.isbn
GROUP BY b.isbn;

SELECT b.title, b.isbn, COALESCE(brs.average_rating, 0) AS average_rating
FROM book b
LEFT JOIN book_rating_stats brs ON b.isbn = brs.isbn
ORDER BY average_rating DESC;

-- List books ordered by number of reviews
CREATE VIEW book_review_count AS
SELECT isbn, COUNT(*) AS review_count
FROM review
GROUP BY isbn;

SELECT b.title, b.isbn, COALESCE(brc.review_count, 0) AS review_count
FROM book b
LEFT JOIN book_review_count brc ON b.isbn = brc.isbn
ORDER BY review_count DESC;


-- Calculate the total number of pages read by a user
CREATE VIEW user_read_books AS
SELECT b.*
FROM book b
JOIN on_shelf os ON b.isbn = os.isbn
JOIN shelf s ON os.shelf_id = s.shelf_id
JOIN user_info u ON s.user_id = u.user_id
WHERE s.shelf_name = 'has read';

SELECT SUM(num_pages) AS total_pages_read
FROM user_read_books
WHERE user_id = [user_id];


-- Add a trigger to automatically add books to the "to-read" shelf
DELIMITER !
CREATE TRIGGER auto_add_to_read_shelf
AFTER INSERT ON on_shelf
FOR EACH ROW
BEGIN
    -- Check if the book is not in has read for the user
    IF NOT EXISTS (
        SELECT 1
        FROM on_shelf os
        JOIN shelf s ON os.shelf_id = s.shelf_id
        WHERE os.isbn = NEW.isbn
        AND s.user_id = NEW.user_id
        AND s.shelf_name = 'Has Read'
    ) THEN
        -- Insert the book into the to read shelf
        INSERT INTO on_shelf (isbn, shelf_id)
        SELECT NEW.isbn, shelf_id
        FROM shelf
        WHERE user_id = NEW.user_id
        AND shelf_name = 'To Read'
        LIMIT 1;
    END IF;
END !
DELIMITER ;



DELIMITER !
CREATE TRIGGER auto_delete_from_to_read_shelf
AFTER INSERT ON on_shelf
FOR EACH ROW
BEGIN
    -- Delete from the to read shelf if added to has read shelf
    DELETE FROM on_shelf
    WHERE isbn = NEW.isbn
    AND shelf_id = (
        SELECT shelf_id
        FROM shelf
        WHERE user_id = NEW.user_id
        AND shelf_name = 'To Read'
        LIMIT 1
    );
END !
DELIMITER ;