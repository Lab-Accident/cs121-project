"""
Review-related functions for the Goodreads database.
"""

import mysql.connector

# ----------------------------------------------------------------------
# Functions for Review Operations
# ----------------------------------------------------------------------

def add_review(conn, user_id, isbn, star_rating, review_text):
    """
    Add a review to the database.

    Args:
        conn (MySQL Connection object): connection to the database
        user_id (int): the user's ID
        isbn (str): the ISBN of the book to review
        star_rating (float): the star rating (1-5)
        review_text (str): the review text
    """
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM review WHERE user_id = %s AND isbn = %s", (user_id, isbn))
        count = cursor.fetchone()[0]
        if count > 0:
            modify = input("You have already reviewed this book. Do you want to modify your review? (y/n): ").strip().lower()
            if modify == "y":
                sql = "UPDATE review SET star_rating = %s, review_text = %s WHERE user_id = %s AND isbn = %s"
                cursor.execute(sql, (star_rating, review_text, user_id, isbn))
                conn.commit()
                print("Review modified successfully!")
                return
            else:
                print("Review not modified.")
                return
        sql = "INSERT INTO review (user_id, isbn, star_rating, review_text) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (user_id, isbn, star_rating, review_text))
        conn.commit()
        print("Review added successfully!")
    except mysql.connector.Error as err:
        print("Error adding review:", err)


def delete_review(conn, user_id, isbn):
    """
    Deletes a review from the database.

    Args:
        conn (MySQL Connection object): connection to the database
        user_id (int): the user's ID
        isbn (str): the ISBN of the book to review
    """
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM review WHERE user_id = %s AND isbn = %s"
        cursor.execute(sql, (user_id, isbn))
        conn.commit()
        print("Review(s) deleted successfully!")
    except mysql.connector.Error as err:
        print("Error deleting review:", err)


def modify_review(conn, user_id, isbn, star_rating, review_text):
    """
    Modifies a review in the database.

    Args:
        conn (MySQL Connection object): connection to the database
        user_id (int): the user's ID
        isbn (str): the ISBN of the book to review
        star_rating (float): the star rating (1-5)
        review_text (str): the review text
    """
    cursor = conn.cursor()
    try:
        sql = "UPDATE review SET star_rating = %s, review_text = %s WHERE user_id = %s AND isbn = %s"
        cursor.execute(sql, (star_rating, review_text, user_id, isbn))
        conn.commit()
        print("Review modified successfully!")
    except mysql.connector.Error:
        print("Error modifying review. Make sure you have reviewed this book before.")

def get_reviews(conn, isbn):
    """
    Get all reviews for a book.

    Args:
        conn (MySQL Connection object): connection to the database
        isbn (str): the ISBN of the book
    """
    cursor = conn.cursor()
    try:
        sql = "SELECT user_id, star_rating, review_text FROM review WHERE isbn = %s"
        cursor.execute(sql, (isbn,))
        results = cursor.fetchall()
        if not results:
            print("No reviews found.")
        else:
            for row in results:
                print(f"User ID: {row[0]} | Star Rating: {row[1]}\nReview: {row[2]}\n")
            print()
    except mysql.connector.Error as err:
        print("Error getting reviews:", err)


# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------

def add_review_ui(conn, user_id, isbn=None):
    """
    UI for adding a review.

    Args:
        conn (MySQL Connection object): connection to the database
        user_id (int): the user's ID
        isbn (str, optional): the ISBN of the book; defaults to None
    """
    # allow for optional isbn parameter (for individual book pages)
    if isbn is None:
        isbn = input("Enter the ISBN of the book: ")
    star_rating = input("Enter your star rating (1-5): ")
    review_text = input("Enter your review: ")
    add_review(conn, user_id, isbn, star_rating, review_text)


def delete_review_ui(conn, user_id, is_admin=False):
    """
    UI for deleting a review.

    Args:
        conn (MySQL Connection object): connection to the database
        user_id (int): the user's ID
        is_admin (bool, optional): if the user is an admin; defaults to False.
    """
    if isbn is None:
        isbn = input("Enter the ISBN of the book: ")
    if is_admin:
        rev_user_id = input("Enter the user ID of the review to delete: ")
        delete_review(conn, rev_user_id, isbn)
    else:
        # can only delete your own review
        delete_review(conn, user_id, isbn)


def modify_review_ui(conn, user_id):
    """
    UI for modifying a review.

    Args:
        conn (MySQL Connection object): connection to the database
        user_id (int): the user's ID
    """
    isbn = input("Enter the ISBN of the book: ")
    star_rating = input("Enter the new star rating (1-5): ")
    review_text = input("Enter the new review: ")
    modify_review(conn, user_id, isbn, star_rating, review_text)
