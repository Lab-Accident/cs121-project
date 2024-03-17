import mysql.connector

# ----------------------------------------------------------------------
# Functions for User Actions
# ----------------------------------------------------------------------

def add_user(conn, email, password, first_name, last_name, as_admin=False):
    """
    Creates a user in the database.

    Args:
        conn (MySQL Connection object): connection to the database
        email (str): email of the user
        password (str): password of the user
        first_name (str): first name of the user
        last_name (str): last name of the user
        as_admin (bool, optional): Whether we are making an admin. Defaults to False.

    NOTE: Not currently used in app.py
    """
    cursor = conn.cursor()
    try:
        sql = "CALL sp_add_user(%s, %s, %s, %s, %s)"
        cursor.execute(sql, (email, password, first_name, last_name, as_admin))
        conn.commit()
    except mysql.connector.Error as err:
        print("Error creating user:", err)

def delete_user(conn, user_id):
    """
    Deletes a user from the database.

    Args:
        conn (MySQL Connection object): connection to the database
        user_id (int): the user's ID

    NOTE: Not currently used in app.py
    """
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM user_info WHERE user_id = %s"
        cursor.execute(sql, (user_id,))
        conn.commit()
    except mysql.connector.Error as err:
        print("Error deleting user:", err)

def print_user_info(conn, user_id):
    """
    Prints user information.

    Args:
        conn (MySQL Connection object): connection to the database
        user_id (int): the user's ID
    """
    cursor = conn.cursor()
    try:
        sql = "SELECT first_name, last_name, join_date FROM user_info WHERE user_id = %s"
        cursor.execute(sql, (user_id,))
        result = cursor.fetchone()
        if result:
            first_name, last_name, join_date = result
            print(f"{first_name} {last_name}'s Page:")
            print(f"ID: #{user_id} | Joined: {join_date}")
        else:
            print("User not found.")
    except mysql.connector.Error as err:
        print("Error printing user info:", err)