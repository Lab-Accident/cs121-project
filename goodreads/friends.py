import mysql.connector


def find_friends_by_name(conn, name):
    """
    Find friends by name.
    """
    cursor = conn.cursor()
    try:
        sql = "SELECT user_id, CONCAT(first_name, ' ', last_name) AS full_name, email FROM user_info WHERE CONCAT(first_name, ' ', last_name) LIKE %s"
        cursor.execute(sql, ('%' + name + '%',))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print("Error finding friends by name:", err)
        return []


def find_friend_by_email(conn, email):
    """
    Find a friend by email (must match exactly).
    """
    cursor = conn.cursor()
    try:
        sql = "SELECT user_id, CONCAT(first_name, ' ', last_name) AS full_name, email FROM user_info WHERE email = %s"
        cursor.execute(sql, (email,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print("Error finding friend by email:", err)
        return None


def add_friend(conn, user_id, friend_id):
    """
    Add another user to your friends list.
    """
    cursor = conn.cursor()
    try:
        sql1 = "INSERT INTO friend (user_id, friend_id) VALUES (%s, %s);"
        cursor.execute(sql1, (user_id, friend_id))
        sql2 = "INSERT INTO friend (user_id, friend_id) VALUES (%s, %s);"
        cursor.execute(sql2, (friend_id, user_id))
        conn.commit()
        print(f"You are now friends with user #{friend_id}.")
    except mysql.connector.Error:
        print("Failed to add friend. Confirm that you have the correct user ID.")


def delete_friend(conn, user_id, friend_id):
    """
    Remove a user from your friends list.
    """
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM friend WHERE (user_id = %s AND friend_id = %s) OR (user_id = %s AND friend_id = %s)"
        cursor.execute(sql, (user_id, friend_id, friend_id, user_id))
        conn.commit()
        print(f"You are no longer friends with user #{friend_id}.")

    except mysql.connector.Error:
        print("Failed to delete friend. Confirm that you have the correct user ID.")


def view_friends(conn, user_id):
    """
    List all of your friends.
    """
    cursor = conn.cursor()
    try:
        sql = "SELECT user_id, CONCAT(first_name, ' ', last_name) AS name, email FROM user_info WHERE user_id IN (SELECT friend_id FROM friend WHERE user_id = %s)"
        cursor.execute(sql, (user_id,))
        results = cursor.fetchall()
        print("Your friends:")
        for row in results:
            print(f"ID: #{row[0]}, Name: {row[1]}, Email: {row[2]}")
    except mysql.connector.Error as err:
        print("Error viewing friends:", err)


def search_friends_by_name(conn, name):
    """
    Get search results for friends by name.
    """
    results = find_friends_by_name(conn, name)
    print("Search Results:")
    if not results:
        print("No friends found.")
    else:
        for row in results:
            print(f"ID: #{row[0]}, Name: {row[1]}, Email: {row[2]}")
        print()


def search_friend_by_email(conn, email):
    """
    Get search results for a friend by email.
    """
    result = find_friend_by_email(conn, email)
    if result:
        user_id, full_name, email = result
        print(f"User found | ID: #{user_id}, Name: {full_name}, Email: {email}\n")
    else:
        print("No users were found with that email.")
