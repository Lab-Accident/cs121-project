import pandas as pd
import random
import numpy as np
from faker import Faker
import hashlib
import secrets

fake = Faker()

'''
=====================================
CREATING BOOK.CSV
    isbn CHAR(13)
    title VARCHAR(255)
    publisher VARCHAR(50)
    year_published YEAR
    synopsis TEXT
    language_code CHAR(3)
    num_pages INT
    cover_photo_url VARCHAR(255)
    series_name VARCHAR(255)
=====================================
'''
PERCENT_SERIES = 0.2
PERCENT_REVIEW = 0.6

books_df = pd.read_csv("uncleaned_books.csv")

imported_columns = ['isbn', 'author', 'title', 'publisher', 'year_published', 'language_code', 'num_pages']
books_df = books_df[imported_columns]
books_df = books_df[books_df['isbn'].astype(str).str.len() == 13]
books_df = books_df.dropna()
books_df = books_df.reset_index(drop=True)

# books_df['year_published'] = pd.to_datetime(books_df['year_published'], errors='coerce').dt.year
books_df['synopsis'] = [fake.paragraph(nb_sentences=5, variable_nb_sentences=True) for _ in range(len(books_df))]
books_df['cover_photo'] = [fake.url() for _ in range(len(books_df))]


series_books_mapping = {}
for _ in range(int(len(books_df) * PERCENT_SERIES)):
    series_name = fake.sentence(nb_words=3)[:-1].title()
    num_books_in_series = random.randint(2, 10)
    book_indices = np.random.choice(books_df.index, num_books_in_series, replace=False)
    series_books_mapping[series_name] = book_indices

books_df['series_name'] = None
for series_name, book_indices in series_books_mapping.items():
    books_df.loc[book_indices, 'series_name'] = series_name


'''
=====================================
CREATING BOOK_AUTHOR.CSV
    isbn CHAR(13)
    author_id INT

CREATING AUTHOR.CSV;
    author_id INT
    author_name VARCHAR(255)
=====================================
'''
author_list = []
for index, row in books_df.iterrows():
    authors = row['author'].split('/')
    for author in authors:
        author_list.append(author.strip())

authors_df_init = pd.DataFrame(author_list, columns=['author_name']).drop_duplicates()
authors_df = authors_df_init.reset_index(drop=True)

book_authors_df = pd.DataFrame(columns=['isbn', 'author_id'])
for i in range(len(books_df)):
    authors = books_df.at[i, 'author'].split('/')
    isbn = books_df.at[i, 'isbn']
    for author in authors:
        new_row = pd.DataFrame({'isbn': [isbn], 'author_id': authors_df.index[authors_df['author_name'] == author][0] + 1})
        book_authors_df = pd.concat([book_authors_df, new_row], ignore_index=True)

book_authors_df.drop_duplicates(inplace=True)  # drop duplicate book authors
books_df.drop(columns=['author'], inplace=True)


'''
=====================================
CREATING USER_INFO.CSV
    user_id INT
    first_name VARCHAR(30)
    last_name VARCHAR(30)
    email VARCHAR(320)
    salt CHAR(8)
    password_has BINARY(64)
    join_date TIMESTAMP
=====================================
'''
NUMBER_USERS = 500

def make_salt(length):
    safe_characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_+=[]{}|;:.<>?'
    salt = ''.join(secrets.choice(safe_characters) for _ in range(length))
    return salt

def generate_password_hash(password, salt):
    concatenated = salt + password
    hashed_password = hashlib.sha256(concatenated.encode()).hexdigest()
    return hashed_password

def generate_email(first, last, domain):
    first = first.lower()
    last = last.lower()
    number = str(random.randint(0, 999))[0:random.randint(0, 3)]
    email_formats = {
        1: f"{first}.{last}",
        2: f"{first[0]}{last}",
        3: f"{first}_{last}",
        4: f"{first}{last[0]}{number}",
        5: f"{first}{last}"[:random.randint(5, 15)],
        6: f"{first[0]}{last}"[:random.randint(5, 15)],
        7: f"{first}{last}",
        8: f"{first[0]}{last}{number}",
        9: f"{last}.{first}",
        10: f"{first}{fake.word().lower()}{number}",
        11: f"{first[0]}{last}{fake.word().lower()}",
        12: f"{fake.word().lower()}{fake.word().lower()}{number}"
    }
    email_format = email_formats[random.randint(1, 12)]

    return f"{email_format}@{domain}"

users_data = []
for _ in range(NUMBER_USERS):
    first_name = fake.first_name()
    last_name = fake.last_name()
    domain = random.choice(["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com"])
    email = generate_email(first_name, last_name, domain)
    while users_data and len(users_data) > 2 and email in users_data[2]:
        email = generate_email(first_name, last_name, domain)
    salt = make_salt(8)
    password = fake.password()
    password_hash = generate_password_hash(password, salt)
    join_date = fake.date_time_this_decade()
    users_data.append((first_name, last_name, email, salt, password_hash, join_date))

users_df = pd.DataFrame(users_data, columns=['first_name', 'last_name', 'email', 'salt', 'password_hash', 'join_date'])


'''
=====================================
CREATING FRIEND.CSV
    user_id INT
    friend_id INT
=====================================
'''
MAX_FRIENDS = 50

friend_tuples = set()
for i in range(1, NUMBER_USERS + 1):
    num_friends = random.randint(0, MAX_FRIENDS)
    friends = random.sample(range(1, NUMBER_USERS + 1), num_friends)
    for friend in friends:
        if friend != i:
            friend_tuples.add((i, friend))
            friend_tuples.add((friend, i))

friends_df = pd.DataFrame(friend_tuples, columns=['user_id', 'friend_id'])


'''
=====================================
CREATING REVIEW.CSV
    review_id INT
    user_id INT
    isbn VARCHAR(13)
    star_rating DECIMAL(2, 1)
    review_text TEXT
    review_date TIMESTAMP
=====================================
'''
reviews_df = pd.DataFrame(columns=['user_id', 'isbn', 'star_rating', 'review_text', 'review_date'])
for user_id in range(1, 1 + len(users_df)):
    num_reviews = random.randint(0, 10)
    for _ in range(num_reviews):
        isbn = random.choice(books_df['isbn'])
        star_rating = round(random.uniform(0.5, 5.0), 1)
        p_review = random.random()
        if p_review < PERCENT_REVIEW:
            review_text = None
        else:
            review_text = fake.paragraph(nb_sentences=6, variable_nb_sentences=True)
        review_date = fake.date_time_this_decade()
        new_row = pd.DataFrame({'user_id': [user_id], 'isbn': [isbn],
                                'star_rating': [star_rating],
                                'review_text': [review_text],
                                'review_date': [review_date]})
        reviews_df = pd.concat([reviews_df, new_row], ignore_index=True)


'''
=====================================
CREATING SHELF.CSV
    shelf_id INT
    user_id INT
    shelf_name VARCHAR(255)
    is_private BOOLEAN
=====================================
'''
shelves_df = pd.DataFrame(columns=['user_id', 'shelf_name', 'is_private'])

for user_id in range(1, 1 + len(users_df)):
    default_shelves = ["Favorites", "Has Read", "Wants to Read", "Currently Reading"]
    for shelf_name in default_shelves:
        is_private = random.choice([0, 1])
        new_row = pd.DataFrame({'user_id': [user_id], 'shelf_name': [shelf_name], 'is_private': [is_private]})
        shelves_df = pd.concat([shelves_df, new_row], ignore_index=True)

    num_shelves = random.randint(0, 5)
    for _ in range(num_shelves):
        shelf_name = fake.sentence(nb_words=5)[:-1].title()
        is_private = random.choice([0, 1])
        new_row = pd.DataFrame({'user_id': [user_id], 'shelf_name': [shelf_name], 'is_private': [is_private]})
        shelves_df = pd.concat([shelves_df, new_row], ignore_index=True)


'''
=====================================
CREATING ON_SHELF.CSV
    isbn VARCHAR(13)
    shelf_id INT
=====================================
'''
MEAN_BOOKS = 10

on_shelf_df = pd.DataFrame(columns=['isbn', 'shelf_id'])

for shelf_id in range(1, 1 + len(shelves_df)):
    num_books = max(0, min(int(np.random.normal(MEAN_BOOKS, 3)), len(books_df)))
    for isbn in random.sample(list(books_df['isbn']), num_books):
        new_row = pd.DataFrame({'isbn': [isbn], 'shelf_id': [shelf_id]})
        on_shelf_df = pd.concat([on_shelf_df, new_row], ignore_index=True)


'''
=====================================
CREATING GENRES.CSV
    genre name VARCHAR(50)
=====================================
'''
genres = ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", "Mystery",
          "Thriller", "Romance", "Western", "Dystopian", "Historical Fiction",
          "Horror", "Memoir", "Biography", "Self-Help", "Cooking", "Art", "Travel",
          "Religion", "Science", "History", "Math", "Poetry", "Philosophy",
          "Business", "Economics", "Psychology", "Sociology", "Political Science",
          "Education", "Technology", "Health", "Fitness", "Sports", "Nature",
          "Animals", "Crafts", "Hobbies", "Music", "Film", "Theatre", "Television",
          "Gaming", "Comics", "Graphic Novels", "Manga", "Children's", "Young Adult",
          "Adult", "Elderly", "LGBTQ+", "Feminism"]
genres_df = pd.DataFrame(genres, columns=['genre_name'])


'''
=====================================
CREATING BOOK_GENRES.CSV
    isbn VARCHAR(13)
    shelf_id INT
=====================================
'''

book_genres_data = []
for isbn in books_df['isbn']:
    num_genres = random.randint(1, 5)
    selected_genres = random.sample(genres, num_genres)
    for genre in selected_genres:
        book_genres_data.append((isbn, genre))

book_genres_df = pd.DataFrame(book_genres_data, columns=['isbn', 'genre_name'])


'''
=====================================
SAVING TO CSV
=====================================
'''
books_df.to_csv("gen_csvs/book.csv", index=False)
authors_df.to_csv("gen_csvs/author.csv", index=False)
book_authors_df.to_csv("gen_csvs/book_author.csv", index=False)
users_df.to_csv("gen_csvs/user_info.csv", index=False)
friends_df.to_csv("gen_csvs/friend.csv", index=False)
reviews_df.to_csv("gen_csvs/review.csv", index=False)
shelves_df.to_csv("gen_csvs/shelf.csv", index=False)
on_shelf_df.to_csv("gen_csvs/on_shelf.csv", index=False)
genres_df.to_csv("gen_csvs/genre.csv", index=False)
book_genres_df.to_csv("gen_csvs/book_genre.csv", index=False)