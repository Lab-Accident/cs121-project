import mysql.connector


# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------
# Note: There's a distinction between database users (admin and client)
# and application users (e.g. members registered to a store). You can
# choose how to implement these depending on whether you have app.py or
# app-client.py vs. app-admin.py (in which case you don't need to
# support any prompt functionality to conditionally login to the sql database)

class User:
    def __init__(self, user_id, is_admin=False):
        self.user_id = user_id
        self.is_admin = is_admin

current_user = None

def login(conn, email, password):
    cursor = conn.cursor()
    try:
        sql = "SELECT user_id, first_name, last_name, email, is_admin FROM users WHERE email = %s AND password = %s"
        cursor.execute(sql, (email, password))
        user_data = cursor.fetchone()
        if user_data:
            return User(*user_data)
        else:
            print("Invalid email or password.")
            return None
    except mysql.connector.Error as err:
        print("Error logging in:", err)
        return None

def logout():
    global current_user
    current_user = None