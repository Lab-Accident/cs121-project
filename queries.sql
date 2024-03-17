-- Book Queries

-- Get all books written by a given author
-- For this example, we'll use the author "J.K. Rowling"
SELECT title, publisher, year_published
FROM book NATURAL JOIN book_author NATURAL JOIN author
WHERE author_name = 'J.K. Rowling';

-- Search for books by title
-- For this example, we'll search for books with "Harry Potter" in the title
SELECT title, publisher, year_published
FROM book
WHERE title LIKE 'Harry Potter%';

-- Search for recent releases in a given genre
-- For this example, we'll search for fantasy books published in 2010 or later
-- (The dataset is somewhat small and outdated, so using 2010 as the cutoff)
SELECT title, publisher, year_published
FROM book NATURAL JOIN book_genre
WHERE genre_name = 'Fantasy' AND year_published >= 2010;

-- Get all books on a user's 'Currently Reading' shelf
-- (We would have equivalent queries for other default shelves, like 'Read')
-- For this example, we'll use the user with user_id 1
SELECT title, publisher, year_published
FROM book NATURAL JOIN on_shelf NATURAL JOIN shelf
WHERE user_id = 1 AND shelf_name = 'Currently Reading';

-- Get all non-default shelves for a user
SELECT shelf_name FROM shelf
WHERE user_id = 3
AND shelf_name NOT IN
    ('Favorites', 'Has Read', 'Currently Reading', 'Wants to Read');

-- Friends

-- Show all friends of a user
-- For this example, we'll use the user with user_id 1
SELECT CONCAT(first_name, ' ', last_name) AS name, email
FROM user_info JOIN friend ON friend_id = user_info.user_id
WHERE friend.user_id = 1;

-- Search for other users by name
SELECT user_id, CONCAT(first_name, ' ', last_name) AS name, email
FROM user_info
WHERE CONCAT(first_name, ' ', last_name) LIKE 'Madison%';

-- Search for other users by email
SELECT user_id, CONCAT(first_name, ' ', last_name) AS name, email
FROM user_info
WHERE email LIKE 'maddie@caltech.edu';

-- Reviews

-- Get the review statistics for books matching a given title
SELECT title, AVG(star_rating) AS avg_rating,
    COUNT(*) AS num_ratings, COUNT(review_text) AS num_reviews
FROM review NATURAL LEFT JOIN book
WHERE title LIKE 'Harry Potter%'
GROUP BY title;

-- Get a user's review statistics across all books
SELECT user_id, COUNT(*) AS num_reviews,
    AVG(star_rating) AS avg_rating,
    COUNT(review_text) AS num_text_reviews
FROM review
WHERE user_id = 2;

-- Shelves

-- Get all books on a user's 'Favorites' shelf
SELECT title, publisher, year_published
FROM book NATURAL JOIN on_shelf NATURAL JOIN shelf
WHERE user_id = 1 AND shelf_name = 'Favorites';

-- Get a user's # books for 'Has Read', 'Currently Reading', and 'Wants to Read'
SELECT shelf_name, COUNT(*) AS num_books
FROM shelf NATURAL JOIN on_shelf
WHERE shelf_name IN ('Has Read', 'Currently Reading', 'Wants to Read')
AND user_id = 1
GROUP BY shelf_name;

-- Get a random book from a user's 'Wants to Read' shelf
-- This seemed like a fun feature
SELECT title, publisher, year_published
FROM book NATURAL JOIN on_shelf NATURAL JOIN shelf
WHERE user_id = 1 AND shelf_name = 'Wants to Read'
ORDER BY RAND() LIMIT 1;

-- Search all shelves the user has access to for a book
-- For this example, we'll use the user with user_id 1 and search for shelves
-- with "Time" in the name
SELECT shelf_name, is_private
FROM shelf
WHERE (user_id = 1 OR is_private = FALSE)
AND shelf_name LIKE '%Time%';