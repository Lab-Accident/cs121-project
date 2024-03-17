"""
Names: Alexandra Rolfness, Maddie Ramos
Emails: maddie@caltech.edu, arolfnes@caltech.edu

A Goodreads-like application that allows users to search for books,
add books to their reading list, and rate books.

As a user, you can:
- Create an account
- Search for books by title, author, or ISBN
- Create shelves and books to your shelves
- Rate books
- Add friends
- See your statistics (e.g. number of books read, average rating)

As an admin, you can:
- Modify any of the tables in the database
- (most notably, the books and users tables)
- View statistics about the database (e.g. number of users, number of books)
"""

import sys  # to print error messages to sys.stderr
import mysql.connector
# To get error codes from the connector, useful for user-friendly
# error-handling
import mysql.connector.errorcode as errorcode
import friends
import shelf
import books
import login
import reviews
import users

current_user_id = None

# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client. ***Set to False when done testing.***
DEBUG = True


# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn():
    """"
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.

    Parameters:
        is_admin: bool (default False)
    """
    # user_type = 'appadmin' if is_admin else 'appclient'
    # user_pwd = 'adminpw' if is_admin else 'clientpw'
    try:
        # Logging in as admin for permissions
        conn = mysql.connector.connect(
          host='localhost',
          user='appadmin',
          port='3306',
          password='adminpw',
          database='goodreads'
        )
        print('Successfully connected to the Goodreads database!')
        return conn
    except mysql.connector.Error as err:
        # Remember that this is specific to _database_ users, not
        # application users. So is probably irrelevant to a client in your
        # simulated program. Their user information would be in a users table
        # specific to your database; hence the DEBUG use.
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr.write('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr.write('Database does not exist.')
        elif DEBUG:
            sys.stderr.write(err.msg)
        else:
            sys.stderr.write('An error occurred, please contact the administrator.')
        sys.exit(1)


# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_options():
    """
    Displays top-level options for users (main menu).
    """
    print('Where would you like to go? ')
    print('  (1) - Go to your profile')
    print('  (2) - Search for books')
    print('  (q) - Quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == '1':
        user_profile_menu()
    elif ans == '2':
        user_books_menu()
    else:
        print('Invalid option. Please try again.')
        show_options()


# Another example of where we allow you to choose to support admin vs.
# client features  in the same program, or
# separate the two as different app_client.py and app_admin.py programs
# using the same database.
def show_admin_options():
    """
    Displays top-level options for admin users.
    """
    print('What would you like to do? ')
    print('  (1) - Edit Books')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == '1':
        admin_books_menu()

def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print('Goodbye!')
    exit()


# ----------------------------------------------------------------------
# Define Menus
# ----------------------------------------------------------------------
def friends_menu():
    """
    Displays the friends menu, allowing the user to add, remove, or view friends.
    """
    print("What would you like to do?")
    print("  (1) Add a friend")
    print("  (2) Remove a friend")
    print("  (3) Search for friends by name")
    print("  (4) Search for friends by email")
    print("  (5) View current friends")
    print("  (6) View friend's profile")
    print("  (b) Go back")
    print("  (q) Quit")
    print()
    option = input("Enter an option: ").lower()

    if option == "1":
        print("To add a friend, you need to know their user ID.")
        print("You can search for friends by name or email to find their user ID.")
        print("If you'd like to go back, enter '0' instead of a user ID.")

        friend_id = int(input("\nWhat is your friend's user ID? "))
        if friend_id != 0:
            friends.add_friend(conn, current_user_id, friend_id)
    elif option == "2":
        print("To remove a friend, you need to know their user ID.")
        print("You can search for friends by name or email to find their user ID.")
        print("If you'd like to go back, enter '0' instead of a user ID.")

        friend_id = int(input("\nWhat is your friend's user ID? "))
        if friend_id != 0:
            friends.delete_friend(conn, current_user_id, friend_id)
    elif option == "3":
        name = input("Enter the name of the friend to search for: ")
        friends.search_friends_by_name(conn, name)
    elif option == "4":
        email = input("Enter the email of the friend to search for: ")
        friends.search_friend_by_email(conn, email)
    elif option == "5":
        friends.view_friends(conn, current_user_id)
    elif option == "6":
        friend_id = input("Enter the user ID of the friend to view: ")
        user_profile_menu(friend_id)
    elif option == "b":
        user_profile_menu()
    elif option == "q":
        quit_ui()
    else:
        print("Invalid choice.")

    friends_menu()


def shelf_menu():
    """
    Displays the shelf menu, allowing the user to create, delete, or modify shelves.
    """
    print("What would you like to do?")
    print("  (1) Create a new shelf")
    print("  (2) Delete a shelf")
    print("  (3) Add a book to a shelf")
    print("  (4) Remove a book from a shelf")
    print("  (5) Display all books on a shelf")
    print("  (b) Go back")
    print("  (q) Quit")
    option = input("Enter an option: ").lower()

    if option == "1":
        shelf.create_shelf_ui(conn, current_user_id)
    elif option == "2":
        shelf.delete_shelf_ui(conn, current_user_id)
    elif option == "3":
        shelf.add_book_to_shelf_ui(conn, current_user_id)
    elif option == "4":
        shelf.delete_book_from_shelf_ui(conn, current_user_id)
    elif option == "5":
        shelf.display_shelf_ui(conn, current_user_id)


def user_profile_menu(user_id=None):
    """
    Displays the user profile menu, allowing the user to view a profile.
    If the user is the current user, they can also access their friends menu.

    Args:
        user_id (int, optional): the user ID to view, if not the current user
    """
    if user_id is None:
        user_id = current_user_id
    users.print_user_info(conn, user_id)

    print("What would you like to do?")
    print("  (1) View shelves")
    if user_id == current_user_id:
        print("  (2) Open your friends menu")
        print("  (3) Open your shelf menu")
    print("  (b) Go back")
    print("  (q) Quit")
    option = input("Enter an option: ").lower()

    if option == "1":
        shelf.view_shelves(conn, user_id)
        open_shelf = str("Would you like to open a shelf? (y/n): ").lower()
        if open_shelf == "y":
            shelf.display_shelf_ui(conn, user_id)
    elif option == "2" and user_id == current_user_id:
        friends_menu()
    elif option == "3" and user_id == current_user_id:
        shelf_menu()
    elif option == "b":
        if user_id != current_user_id:
            friends_menu()
        show_options()
    elif option == "q":
        quit_ui()
    else:
        print("Invalid choice.")

    user_profile_menu(user_id)


def book_page_menu(isbn):
    """
    Displays the book page menu, allowing the user to take actions related to
    a specific book (add to shelf, rate, read reviews, & get time estimate)

    Args:
        isbn (str): The ISBN of the book to view
    """
    print("\nWhat would you like to do?")
    print("  (1) Add to shelf")
    print("  (2) Rate book")
    print("  (3) Read reviews")
    print("  (4) Get a reading time estimate")
    print("  (b) Go back")
    print("  (q) Quit")

    option = input("Enter an option: ").lower()
    if option == "1":
        shelf.add_book_to_shelf_ui(conn, current_user_id)
    elif option == "2":
        reviews.add_review_ui(conn, current_user_id, isbn)
    elif option == "3":
        reviews.get_reviews(conn, isbn)
    elif option == "4":
        books.get_book_reading_time(conn, isbn)
    elif option == "b":
        user_books_menu()
    elif option == "q":
        quit_ui()
    else:
        print("Invalid choice.")

    book_page_menu(isbn)


def user_books_menu():
    """
    Displays the user books menu, allowing the user to search for books by title or author, and open a book's page.
    """
    print("What would you like to do?")
    print("  (1) Search for books by title")
    print("  (2) Search for books by author")
    print("  (3) Open a book's page")
    print("  (b) Go back")
    print("  (q) Quit")

    option = input("Enter an option: ").lower()
    if option == "1":
        title = input("Enter the title of the book to search for: ")
        books.search_book_by_title(conn, title)
    elif option == "2":
        author = input("Enter the author of the book to search for: ")
        books.search_book_by_author(conn, author)
    elif option == "3":
        isbn = input("Enter the ISBN of the book to open: ")
        print(books.get_book_summary(conn, isbn))
        book_page_menu(isbn)
    elif option == "b":
        show_options()
    elif option == "q":
        quit_ui()
    else:
        print("Invalid choice.")

    user_books_menu()

def admin_books_menu():
    """
    Displays the admin books menu, allowing the admin to search for books by title or author, add a book, or delete a book.
    """
    print("What would you like to do?")
    print("  (1) Search for books by title")
    print("  (2) Search for books by author")
    print("  (3) Add a book")
    print("  (4) Delete a book")
    print("  (b) Go back")
    print("  (q) Quit")

    option = input("Enter an option: ").lower()
    if option == "1":
        title = input("Enter the title of the book to search for: ")
        books.search_book_by_title(conn, title)
    elif option == "2":
        author = input("Enter the author of the book to search for: ")
        books.search_book_by_author(conn, author)
    elif option == "3":
        books.add_new_book(conn)
    elif option == "4":
        isbn = input("Enter the ISBN of the book to delete: ")
        books.delete_book(conn, isbn)
    elif option == "b":
        show_admin_options()
    elif option == "q":
        quit_ui()
    else:
        print("Invalid choice.")

    admin_books_menu()

def login_menu(as_admin=False):
    """
    Login menu which prompts the user to log in or create an account.

    Args:
        as_admin (bool, optional): Whether the user is trying to log in as
                                   an admin. Defaults to False.
    """
    print('Would you to log in or create an account?')
    print('  (1) Log in')
    print('  (2) Create an account')
    ans = input('Enter an option: ').lower()

    if ans == '1':
        user_id = login.login_loop(conn, as_admin)
        if user_id is None:
            quit_ui()
        global current_user_id
        current_user_id = user_id
        return
    elif ans == '2':
        login.create_user(conn, as_admin)
    else:
        print('Invalid option. Please try again.')

    login_menu(as_admin)

# ----------------------------------------------------------------------
# Main Program
# ----------------------------------------------------------------------
if __name__ == '__main__':

    print('Welcome to Goodreads! Are you logging in as an admin or a user?')
    print('  (1) Admin')
    print('  (2) User')
    ans = input('Enter an option: ').lower()

    conn = get_conn()
    if ans == '1':
        login_menu(as_admin=True)
        if current_user_id is not None:
            show_admin_options()
    elif ans == '2':
        login_menu()
        if current_user_id is not None:
            show_options()

