import mysql.connector

#TODO: add book to database
#TODO: delete book
#TODO: modify book
#TODO: search for book


# ----------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------
def rating_to_stars(rating):
    """
    Converts a rating (out of 5) to a string of stars.
    """
    return "★" * int(rating) + "☆" * (5 - int(rating))

# ----------------------------------------------------------------------
# Functions for Book Actions
# ----------------------------------------------------------------------

def add_new_book(conn):
    """
    Add a new book to the database.

    Args:
        conn (MySQL Connection object): connection to the database
    """
    print("Enter the details of the new book:")
    isbn = input("ISBN: ")
    title = input("Title: ")
    authors = []
    while True:
        authors.append(input("Author (if multiple, enter one at a time): "))
        repeat = input("Would you like to add another author? (y/n) ").lower()
        if repeat != "y":
            break
    all_authors = "/".join(authors)
    genres = []
    while True:
        genres.append(input("Genre (if multiple, enter one at a time): "))
        repeat = input("Would you like to add another genre? (y/n) ").lower()
        if repeat != "y":
            break
    all_genres = "/".join(genres)
    pub_year = input("Publication year: ").strip()
    publisher = input("Publisher: ").strip()
    language_code = input("Language code (eng for English): ").strip()
    num_pages = input("Number of pages: ").strip()
    synopsis = input("Enter a synopsis (optional): ").strip()
    cover_url = input("Enter the cover photo URL (optional): ").strip()
    series_name = input("Enter the series name (if available, optional): ").strip()

    cursor = conn.cursor()
    try:
        sql = "CALL add_book(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (isbn, title, publisher, pub_year,
                             language_code, num_pages, synopsis, cover_url,
                             series_name, all_authors, all_genres))
        conn.commit()
        print(f"Book (ISBN #{isbn}) added successfully!")
    except mysql.connector.Error as err:
        print("Error adding book:", err)

def delete_book(conn, isbn):
    """
    Deletes a book from the database.

    Args:
        conn (MySQL Connection object): connection to the database
        isbn (str): ISBN of the book to delete
    """
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM book WHERE isbn = %s"
        cursor.execute(sql, (isbn,))
        conn.commit()
        print(f"Book (ISBN #{isbn}) deleted successfully!")
    except mysql.connector.Error as err:
        print("Error deleting book:", err)

def search_book_by_title(conn, title):
    """
    Search for a book by title.

    Args:
        conn (MySQL Connection object): connection to the database
        title (str): the string to search for in the title
    """
    cursor = conn.cursor()
    try:
        sql = "SELECT * FROM book WHERE title LIKE %s"
        cursor.execute(sql, (f"%{title}%",))
        results = cursor.fetchall()
        print("Search Results:")
        if not results:
            print("No books found.")
        else:
            for row in results:
                print(f"ISBN: {row[0]}, Title: {row[1]}")
            print()
    except mysql.connector.Error as err:
        print("Error searching for book:", err)

def search_book_by_author(conn, author):
    """
    Search for a book by author.

    Args:
        conn (MySQL Connection object): Connection to the database
        author (str): the string to search for in author names
    """
    cursor = conn.cursor()
    try:
        sql = "SELECT isbn, title FROM book NATURAL JOIN book_author NATURAL JOIN author WHERE author_name LIKE %s"
        cursor.execute(sql, (f"%{author}%",))
        results = cursor.fetchall()

        print("Search Results:")
        if not results:
            print("No books found.")
        else:
            for row in results:
                isbn, title = row
                print(f"ISBN: {isbn}, Title: {title}")
            print()

    except mysql.connector.Error as err:
        print("Error searching for book:", err)

def get_book_summary(conn, isbn):
    """
    Print a summary of a book, including its title, author(s), genres,
    and some summary statistics.

    Args:
        conn (MySQL Connection object): Connection to the database
        isbn (str): ISBN of the book
    """
    cursor = conn.cursor()
    try:
        sql = "SELECT * FROM book WHERE isbn = %s"
        cursor.execute(sql, (isbn,))
        isbn, title, publisher, year, _, num_pages, synopsis, _, _ = cursor.fetchone()

        sql = "SELECT author_name FROM book_author NATURAL JOIN author WHERE isbn = %s"
        cursor.execute(sql, (isbn,))
        authors = cursor.fetchall()

        sql = "SELECT genre_name FROM book_genre NATURAL JOIN genre WHERE isbn = %s"
        cursor.execute(sql, (isbn,))
        genres = cursor.fetchall()

        if isbn is not None:
            print(f'{title}')
            print('-' * len(title))
            author_str = authors.join(', ')
            print(f'By {author_str}\n.')
            print(get_book_stats(conn, isbn))


            print(f'Synopsis: {synopsis}')
            genre_str = genres.join(', ')
            print(f'Genres: {genre_str}.\n')
            print(f'Published {year} by {publisher}. ISBN {isbn}')

        else:
            print("No book found.")
    except mysql.connector.Error as err:
        print("Error getting book summary:", err)

def get_book_stats(conn, isbn):
    cursor = conn.cursor()
    try:
        sql = "SELECT * FROM book_review_stats WHERE isbn = %s"
        cursor.execute(sql, (isbn,))
        isbn, avg_rating, num_ratings, num_reviews = cursor.fetchone()
        stars = rating_to_stars(avg_rating)
        print(f'{stars} {avg_rating:.2f} | {num_ratings} ratings | {num_reviews} reviews')
    except mysql.connector.Error as err:
        print("Error getting book stats:", err)


def get_book_reading_time(conn, isbn):
    cursor = conn.cursor()
    try:
        sql = "SELECT num_pages FROM book WHERE isbn = %s"
        cursor.execute(sql, (isbn,))
        num_pages = cursor.fetchone()[0]
        if num_pages is not None:
            wpm = int(input("What is your reading speed (words per minute)? Press enter if you don't know: "))
            if wpm is None:
                wpm = 200
            minutes = num_pages / wpm
            hours = minutes // 60
            minutes = minutes % 60
            print(f"It will take you: {hours}h and {minutes}m ({num_pages} pages).")
        else:
            print("No book found.")
    except mysql.connector.Error as err:
        print("Error getting book reading time:", err)