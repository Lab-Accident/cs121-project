import mysql.connector

def create_shelf(conn, user_id, shelf_name, is_private=False):
    #TODO: double check the there isn't a shelf with the same name

    cursor = conn.cursor()
    try:
        sql = "INSERT INTO shelves (user_id, shelf_name, is_private) VALUES (%s, %s, %s)"
        cursor.execute(sql, (user_id, shelf_name, is_private))
        conn.commit()
        print("Shelf created successfully!")
    except mysql.connector.Error as err:
        print("Error creating shelf:", err)


def delete_shelf(conn, user_id, shelf_name):
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM shelves WHERE user_id = %s AND shelf_name = %s"
        cursor.execute(sql, (user_id, shelf_name))
        conn.commit()
        print("Shelf deleted successfully!")
    except mysql.connector.Error as err:
        print("Error deleting shelf:", err)

def add_book_to_shelf(conn, isbn, shelf_name): #TODO: check user_id
    #TODO: double check the book isn't already on the shelf

    cursor = conn.cursor()
    try:
        sql = "INSERT INTO shelf_books (isbn, shelf_name) VALUES (%s, %s)"
        cursor.execute(sql, (isbn, shelf_name))
        conn.commit()
        print("Book added to shelf successfully!")
    except mysql.connector.Error as err:
        print("Error adding book to shelf:", err)

def delete_book_from_shelf(conn, isbn, user_id, shelf_name): #TODO: check user_id
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM shelf_books WHERE isbn = %s AND shelf_name = %s"
        cursor.execute(sql, (isbn, shelf_name))
        conn.commit()
        print("Book removed from shelf successfully!")
    except mysql.connector.Error as err:
        print("Error removing book from shelf:", err)


# ----------------------------------------------------------------------
def create_shelf_ui(conn, user_id):
    shelf_name = input("Enter the name of the new shelf: ")
    is_private = input("Is the shelf private? (yes/no): ").lower() == "yes"
    create_shelf(conn, user_id, shelf_name, is_private)

def delete_shelf_ui(conn, user_id):
    shelf_name = input("Enter the name of the shelf to delete: ")
    delete_shelf(conn, user_id, shelf_name)

def add_book_to_shelf_ui(conn, user_id): #TODO: add by book name
    isbn = input("Enter the ISBN of the book to add: ")
    shelf_name = input("Enter the name of the shelf to add the book to: ")
    add_book_to_shelf(conn, isbn, user_id, shelf_name)

def delete_book_from_shelf_ui(conn, user_id): #TODO: add by book name
    isbn = input("Enter the ISBN of the book to remove: ")
    shelf_name = input("Enter the name of the shelf to remove the book from: ")
    delete_book_from_shelf(conn, isbn, user_id, shelf_name)