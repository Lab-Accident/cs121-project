"""
Shelf-related functions for the Goodreads database.
"""

import mysql.connector

default_shelves = ["Favorites", "Has Read", "Wants to Read", "Currently Reading"]

# ----------------------------------------------------------------------
# Functions for Shelf Actions
# ----------------------------------------------------------------------
def view_shelves(conn, user_id):
    """
    Prints the user's shelves.

    Args:
        conn (MySQL Connection object): connection to the database
        user_id (int): the user's ID
    """
    cursor = conn.cursor()
    try:
        sql = "SELECT shelf_id, shelf_name FROM shelf WHERE user_id = %s"
        cursor.execute(sql, (user_id,))
        results = cursor.fetchall()
        if not results:
            print("No shelves found.")
        else:
            for row in results:
                shelf_id, shelf_name = row
                print(f"Shelf ID: {shelf_id} | Shelf Name: {shelf_name}")
            print()
    except mysql.connector.Error as err:
        print("Error getting user shelves:", err)


def create_shelf(conn, user_id, shelf_name, is_private=False):
    """
    Create a new shelf for a user.

    Args:
        conn (MySQL Connection object): connection to the database
        user_id (int): the user's ID
        shelf_name (str): the name of the new shelf
        is_private (bool, optional): if the shelf is private; defaults to False
    """
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO shelf (user_id, shelf_name, is_private) VALUES (%s, %s, %s)"
        cursor.execute(sql, (user_id, shelf_name, is_private))
        conn.commit()
        print("Shelf created successfully!")
    except mysql.connector.Error as err:
        print("Error creating shelf:", err)


def delete_shelf(conn, user_id, shelf_id):
    """
    Deletes a shelf from the database.

    Args:
        conn (MySQL Connection object): connection to the database
        user_id (int): the user's ID
        shelf_id (int): the shelf's ID
    """
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM shelf WHERE user_id = %s AND shelf_id = %s"
        cursor.execute(sql, (user_id, shelf_id))
        conn.commit()

        print("Shelf deleted successfully!")
    except mysql.connector.Error as err:
        print("Error deleting shelf:", err)


def add_book_to_shelf(conn, isbn, user_id, shelf_id):
    """
    Adds a book to a shelf.

    Args:
        cconn (MySQL Connection object): connection to the database
        isbn (str): the ISBN of the book to add
        user_id (int): the user's ID
        shelf_id (int): the shelf's ID
    """
    cursor = conn.cursor()
    try:
        # check the shelf belongs to the user
        sql = "SELECT * FROM shelf WHERE user_id = %s AND shelf_id = %s"
        cursor.execute(sql, (user_id, shelf_id))
        if not cursor.fetchone():
            print("Double-check this shelf belongs to you.")
            return

        # add the book to the shelf
        sql = "INSERT INTO on_shelf (isbn, shelf_id) VALUES (%s, %s)"
        cursor.execute(sql, (isbn, shelf_id))
        conn.commit()

        print("Book added to shelf successfully!")
    except mysql.connector.Error as err:
        print("Error adding book to shelf:", err)


def delete_book_from_shelf(conn, isbn, user_id, shelf_id):
    """
    Removes a book from a shelf.

    Args:
        conn (MySQL Connection object): connection to the database
        isbn (str): the ISBN of the book to remove
        user_id (int): the user's ID
        shelf_id (int): the shelf's ID
    """
    cursor = conn.cursor()
    try:
        # check the shelf belongs to the user
        sql = "SELECT * FROM shelf WHERE user_id = %s AND shelf_id = %s"
        cursor.execute(sql, (user_id, shelf_id))
        if not cursor.fetchone():
            print("Double-check this shelf belongs to you.")
            return

        # remove the book from the shelf
        sql = "DELETE FROM on_shelf WHERE isbn = %s AND shelf_id = %s"
        cursor.execute(sql, (isbn, shelf_id))
        conn.commit()
        print("Book removed from shelf successfully!")
    except mysql.connector.Error as err:
        print("Error removing book from shelf:", err)


def display_shelf(conn, shelf_id):
    """
    Displays the books on a shelf.

    Args:
        conn (MySQL Connection object): connection to the database
        shelf_id (int): the shelf's ID
    """
    cursor = conn.cursor()
    try:
        # get the books on the shelf
        sql = "SELECT isbn, title FROM on_shelf NATURAL JOIN book WHERE shelf_id = %s"
        cursor.execute(sql, (shelf_id,))
        results = cursor.fetchall()
        if not results:
            print("No books found on this shelf.")
        else:
            print("Books on this shelf:")
            for row in results:
                print(f"ISBN: {row[0]} | Title: {row[1]}")
    except mysql.connector.Error as err:
        print("Error displaying shelf:", err)


# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def create_shelf_ui(conn, user_id):
    """
    Prompts a user to create a new shelf.

    Args:
        conn (MySQL Connection object): connection to the database
        user_id (int): the user's ID
    """
    shelf_name = input("Enter the name of the new shelf: ")
    is_private = input("Is the shelf private? (y/n): ").lower() == "y"
    create_shelf(conn, user_id, shelf_name, is_private)


def delete_shelf_ui(conn, user_id):
    """
    Prompts a user to delete a shelf.

    Args:
        conn (MySQL Connection object): connection to the database
        user_id (int): the user's ID
    """
    cursor = conn.cursor()
    try:
        shelf_id = input("Enter the id of the shelf to delete: ")

        # check the shelf exists
        sql = "SELECT shelf_name FROM shelf WHERE user_id = %s AND shelf_id = %s"
        cursor.execute(sql, (user_id, shelf_id))
        shelf_name = cursor.fetchone()
        if not shelf_name:
            print("Double-check the shelf ID.")
            return

        # check the shelf is not a default shelf
        if shelf_name[0] in default_shelves:
            print("You cannot delete a default shelf.")
            return

        delete_shelf(conn, user_id, shelf_id)
    except mysql.connector.Error as err:
        print("Error deleting shelf:", err)


def add_book_to_shelf_ui(conn, user_id, isbn=None):
    """
    Prompts a user to add a book to a shelf.

    Args:
        conn (MySQL Connection object): connection to the database
        user_id (int): the user's ID
        isbn (str, optional): the ISBN of the book to add, if already known
    """
    if not isbn:
        isbn = input("Enter the ISBN of the book to add: ")
    print("\nHere are your shelves:")
    view_shelves(conn, user_id)
    print()
    shelf_name = input("Enter the ID of the shelf to add the book to: ")
    add_book_to_shelf(conn, isbn, user_id, shelf_name)


def delete_book_from_shelf_ui(conn, user_id):
    """
    Prompts a user to remove a book from a shelf.

    Args:
        conn (MySQL Connection object): connection to the database
        user_id (int): the user's ID
    """
    print("\nHere are your shelves:")
    view_shelves(conn, user_id)
    print()
    shelf_id = input("Enter the id of the shelf to remove the book from: ")

    print("\nHere are the books on that shelf:")
    display_shelf(conn, shelf_id)
    print()

    isbn = input("Enter the ISBN of the book to remove: ")
    delete_book_from_shelf(conn, isbn, user_id, shelf_id)


def display_shelf_ui(conn):
    """
    Prompts a user to choose a shelf to display.

    Args:
        conn (MySQL Connection object): connection to the database
        user_id (int): the user's ID
    """
    shelf_id = input("Enter the id of the shelf to display: ")
    display_shelf(conn, shelf_id)
