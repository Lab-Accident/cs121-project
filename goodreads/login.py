"""
Login and authentication functionality for the Goodreads database.
"""

import mysql.connector


def authentication(conn, as_admin=False):
    """
    Authenticates a user based on their email and password.

    Args:
        as_admin (bool, optional): Whether the user is an admin. Defaults to False.

    Returns:
        int: The user_id of the user who is successfully authenticated (or None)
    """
    cursor = conn.cursor()

    email = input('What is your email? ')
    password = input('What is your password? ')
    # don't let users use admin functionality unless they are an admin
    try:
        sql = "SELECT authenticate(%s, %s)"
        cursor.execute(sql, (email, password))
        auth = cursor.fetchone()[0]
        if auth != 1:
            print("Invalid email or password.")
            return None

        sql = "SELECT user_id, is_admin FROM user_info WHERE email = %s"
        cursor.execute(sql, (email,))
        response = cursor.fetchone()
        # Admins can sign in as users, but not the other way around
        if response[1] != 1 and as_admin:
            print("You are trying to sign in as an admin.")
            return None
        else:
            print("Welcome!")
            return response[0] # user_id
    except mysql.connector.Error as err:
        print("Error logging in:", err)
        return None


def login_loop(conn, as_admin=False):
    """
    Loops through the login process until the user successfully logs in or fails.

    Args:
        as_admin (bool, optional): Whether the user is an admin. Defaults to False.
    """
    global current_user_id
    num_tries = 0
    while num_tries < 3:
        user_id = authentication(conn, as_admin)
        if user_id is not None:
            print()  # blank line for spacing
            return user_id
        num_tries += 1
        print(f'You have {3 - num_tries} tries left.')
    print('You have failed to log in too many times. Goodbye.')
    return None


def create_user(conn, as_admin=False):
    """
    Creates a user in the database.

    Args:
        as_admin (bool, optional): Whether we are making an admin. Defaults to False.
    """
    print('Please enter the following information to create an account:')
    email = input('Email: ')
    password = input('Password: ')
    first_name = input('First name: ')
    last_name = input('Last name: ')
    cursor = conn.cursor()
    try:
        sql = "CALL sp_add_user(%s, %s, %s, %s, %s)"
        cursor.execute(sql, (email, password, first_name, last_name, as_admin))
        conn.commit()
        print("User created successfully! Log in with your new account.")
    except mysql.connector.Error as err:
        print("Error creating user:", err)
    print()