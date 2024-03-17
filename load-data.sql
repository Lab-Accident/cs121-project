-- This script will load CSV data to fill the Goodreads DB tables

-- Make sure this file is in the same directory as the CSV files and
-- setup.sql. Then run the following in the mysql> prompt (assuming
-- you have a goodreads DB created with CREATE DATABASE goodreads;):
-- USE DATABASE goodreads;
-- source setup.sql; (make sure no warnings appear)
-- source load.sql; (make sure there are 0 skipped/warnings)

LOAD DATA LOCAL INFILE 'gen_csvs/user_info.csv' INTO TABLE user_info
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS
(first_name, last_name, email, salt, password_hash, join_date);

LOAD DATA LOCAL INFILE 'gen_csvs/friend.csv' INTO TABLE friend
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

-- Need to load books first because of foreign key constraints
LOAD DATA LOCAL INFILE 'gen_csvs/book.csv' INTO TABLE book
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS
(isbn,title,publisher,year_published,language_code,num_pages,synopsis,cover_photo_url,series_name);

LOAD DATA LOCAL INFILE 'gen_csvs/review.csv' INTO TABLE review
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS
(user_id,isbn,star_rating,@text,review_date)
SET review_text = NULLIF(@text,'');

LOAD DATA LOCAL INFILE 'gen_csvs/shelf.csv' INTO TABLE shelf
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS
(user_id,shelf_name,is_private);

LOAD DATA LOCAL INFILE 'gen_csvs/on_shelf.csv' INTO TABLE on_shelf
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'gen_csvs/genre.csv' INTO TABLE genre
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS
(genre_name);

LOAD DATA LOCAL INFILE 'gen_csvs/book_genre.csv' INTO TABLE book_genre
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'gen_csvs/author.csv' INTO TABLE author
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS
(author_name);

LOAD DATA LOCAL INFILE 'gen_csvs/book_author.csv' INTO TABLE book_author
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
