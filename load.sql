-- This script will load CSV data to fill the Goodreads DB tables

-- Make sure this file is in the same directory as the CSV files and
-- setup.sql. Then run the following in the mysql> prompt (assuming
-- you have a goodreads DB created with CREATE DATABASE goodreads;):
-- USE DATABASE goodreads;
-- source setup.sql; (make sure no warnings appear)
-- source load.sql; (make sure there are 0 skipped/warnings)

LOAD DATA LOCAL INFILE 'users.csv' INTO TABLE users
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'friends.csv' INTO TABLE friends
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'reviews.csv' INTO TABLE reviews
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'shelves.csv' INTO TABLE shelves
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'on_shelf.csv' INTO TABLE on_shelf
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'books.csv' INTO TABLE books
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'genres.csv' INTO TABLE genre
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'book_genres.csv' INTO TABLE book_genres
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
