import mysql.connector

def find_friends_by_name(conn, name):
    cursor = conn.cursor()
    try:
        sql = "SELECT user_id, CONCAT(first_name, ' ', last_name) AS full_name, email FROM users WHERE CONCAT(first_name, ' ', last_name) LIKE %s"
        cursor.execute(sql, ('%' + name + '%',))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print("Error finding friends by name:", err)
        return []

def find_friend_by_email(conn, email):
    cursor = conn.cursor()
    try:
        sql = "SELECT user_id, CONCAT(first_name, ' ', last_name) AS full_name, email FROM users WHERE email = %s"
        cursor.execute(sql, (email,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print("Error finding friend by email:", err)
        return None

def add_friend(conn, user_id, friend_id):
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO friends (user_id, friend_id) VALUES (%s, %s)"
        cursor.execute(sql, (user_id, friend_id))
        conn.commit()
        print("Friend added successfully!")
    except mysql.connector.Error as err:
        print("Error adding friend:", err)

def delete_friend(conn, user_id, friend_id):
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM friends WHERE (user_id = %s AND friend_id = %s) OR (user_id = %s AND friend_id = %s)"
        cursor.execute(sql, (user_id, friend_id, friend_id, user_id))
        conn.commit()
        print("Friend deleted successfully!")
    except mysql.connector.Error as err:
        print("Error deleting friend:", err)


# ----------------------------------------------------------------------
def add_friend_ui(conn, user_id):
    friend_id = input("Enter the user ID of the friend to add: ")
    add_friend(conn, user_id, friend_id)


def delete_friend_ui(conn, user_id):
    friend_id = input("Enter the user ID of the friend to delete: ")
    delete_friend(conn, user_id, friend_id)


def select_friend(results):
    if not results:
        print("No friends found.")
        return None
    
    print("Select a friend:")
    for index, row in enumerate(results, start=1):
        print(f"{index}. Name: {row[1]}, Email: {row[2]}")
    
    while True:
        try:
            choice = int(input("Enter the number of the friend: "))
            if 1 <= choice <= len(results):
                return results[choice - 1][0]
            else:
                print("Invalid choice. Please enter a number within the range.")
        except ValueError:
            print("Invalid input. Please enter a number.")



def search_friends_by_name(conn, name):
    results = find_friends_by_name(conn, name)
    print("Search Results:")
    return select_friend(results)



def search_friend_by_email(conn, email):
    result = find_friend_by_email(conn, email)
    if result:
        user_id, full_name, email = result
        print(f"Friend found: User ID: {user_id}, Name: {full_name}, Email: {email}")
    else:
        print("Friend not found.")
    return result