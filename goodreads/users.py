import mysql.connector

def add_user(conn, email, password, first_name, last_name, as_admin=False):
    """
    Creates a user in the database.

    Args:
        as_admin (bool, optional): Whether we are making an admin. Defaults to False.
    """
    cursor = conn.cursor()
    try:
        sql = "CALL sp_add_user(%s, %s, %s, %s, %s)"
        cursor.execute(sql, (email, password, first_name, last_name, as_admin))
        conn.commit()
    except mysql.connector.Error as err:
        print("Error creating user:", err)

def delete_user(conn, user_id):
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM user_info WHERE user_id = %s"
        cursor.execute(sql, (user_id,))
        conn.commit()
    except mysql.connector.Error as err:
        print("Error deleting user:", err)

def print_user_info(conn, user_id):
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