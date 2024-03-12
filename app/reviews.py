import mysql.connector

# ----------------------------------------------------------------------
# Functions for Review Operations
# ----------------------------------------------------------------------
def add_review(conn, user_id, isbn, star_rating, review_text):
    #TODO: double check the book doesn't already have a review by the user
    #TODO: if it does, ask if they want to modify the review

    cursor = conn.cursor()
    try:
        sql = "INSERT INTO reviews (user_id, isbn, star_rating, review_text) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (user_id, isbn, star_rating, review_text))
        conn.commit()
        print("Review added successfully!")
    except mysql.connector.Error as err:
        print("Error adding review:", err)


def delete_review(conn, user_id, isbn, is_admin=False):
    cursor = conn.cursor()
    try:
        if is_admin:
            # For admin users, delete any review
            # TODO: change to specific which review, not all reviews for a book
            sql = "DELETE FROM reviews WHERE isbn = %s"
            cursor.execute(sql, (isbn,))
        else:
            # For normal users, delete only their own review
            sql = "DELETE FROM reviews WHERE user_id = %s AND isbn = %s"
            cursor.execute(sql, (user_id, isbn))
        conn.commit()
        print("Review(s) deleted successfully!")
    except mysql.connector.Error as err:
        print("Error deleting review:", err)


def modify_review(conn, user_id, isbn, star_rating, review_text):
    cursor = conn.cursor()
    try:
        sql = "UPDATE reviews SET star_rating = %s, review_text = %s WHERE user_id = %s AND isbn = %s"
        cursor.execute(sql, (star_rating, review_text, user_id, isbn))
        conn.commit()
        print("Review modified successfully!")
    except mysql.connector.Error as err:
        print("Error modifying review:", err)



# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_review_options():
    print("What would you like to do?")
    print("  (1) Add a review")
    print("  (2) Delete a review")
    print("  (3) Modify a review")
    print()
    option = input("Enter your choice (1-3): ")
    if option == "1":
        add_review_ui()
    elif option == "2":
        delete_review_ui()
    elif option == "3":
        modify_review_ui()
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")


def add_review_ui(user_id):
    isbn = input("Enter the ISBN of the book: ")
    star_rating = input("Enter the star rating (1-5): ")
    review_text = input("Enter your review: ")
    add_review(user_id, isbn, star_rating, review_text)


def delete_review_ui(user_id):
    isbn = input("Enter the ISBN of the book: ")
    delete_review(user_id, isbn)


def modify_review_ui(user_id):
    isbn = input("Enter the ISBN of the book: ")
    star_rating = input("Enter the new star rating (1-5): ")
    review_text = input("Enter the new review: ")
    modify_review(user_id, isbn, star_rating, review_text)
