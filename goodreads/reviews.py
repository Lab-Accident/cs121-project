import mysql.connector

# ----------------------------------------------------------------------
# Functions for Review Operations
# ----------------------------------------------------------------------
def add_review(conn, user_id, isbn, star_rating, review_text):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM review WHERE user_id = %s AND isbn = %s", (user_id, isbn))
        count = cursor.fetchone()[0]
        if count > 0:
            modify = input("You have already reviewed this book. Do you want to modify your review? (yes/no): ").strip().lower()
            if modify == "yes":
                sql = "UPDATE review SET star_rating = %s, review_text = %s WHERE user_id = %s AND isbn = %s"
                cursor.execute(sql, (star_rating, review_text, user_id, isbn))
                conn.commit()
                print("Review modified successfully!")
                return
            else:
                print("Review not modified.")
                return
        sql = "INSERT INTO review (user_id, isbn, star_rating, review_text) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (user_id, isbn, star_rating, review_text))
        conn.commit()
        print("Review added successfully!")
    except mysql.connector.Error as err:
        print("Error adding review:", err)


def delete_review(conn, user_id, isbn):
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM review WHERE user_id = %s AND isbn = %s"
        cursor.execute(sql, (user_id, isbn))
        conn.commit()
        print("Review(s) deleted successfully!")
    except mysql.connector.Error as err:
        print("Error deleting review:", err)


def modify_review(conn, user_id, isbn, star_rating, review_text):
    cursor = conn.cursor()
    try:
        sql = "UPDATE review SET star_rating = %s, review_text = %s WHERE user_id = %s AND isbn = %s"
        cursor.execute(sql, (star_rating, review_text, user_id, isbn))
        conn.commit()
        print("Review modified successfully!")
    except mysql.connector.Error:
        print("Error modifying review. Make sure you have reviewed this book before.")

def get_reviews(conn, isbn):
    cursor = conn.cursor()
    try:
        sql = "SELECT user_id, star_rating, review_text FROM review WHERE isbn = %s"
        cursor.execute(sql, (isbn,))
        results = cursor.fetchall()
        if not results:
            print("No reviews found.")
        else:
            for row in results:
                print(f"User ID: {row[0]} | Star Rating: {row[1]}\nReview: {row[2]}\n")
            print()
    except mysql.connector.Error as err:
        print("Error getting reviews:", err)



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


def add_review_ui(conn, user_id, isbn=None):
    # allow for optional isbn parameter (for individual book pages)
    if isbn is None:
        isbn = input("Enter the ISBN of the book: ")
    star_rating = input("Enter your star rating (1-5): ")
    review_text = input("Enter your review: ")
    add_review(conn, user_id, isbn, star_rating, review_text)


def delete_review_ui(conn, user_id, is_admin=False):
    if isbn is None:
        isbn = input("Enter the ISBN of the book: ")
    if is_admin:
        rev_user_id = input("Enter the user ID of the review to delete: ")
        delete_review(conn, rev_user_id, isbn)
    else:
        # can only delete your own review
        delete_review(conn, user_id, isbn)


def modify_review_ui(conn, user_id):
    isbn = input("Enter the ISBN of the book: ")
    star_rating = input("Enter the new star rating (1-5): ")
    review_text = input("Enter the new review: ")
    modify_review(conn, user_id, isbn, star_rating, review_text)
