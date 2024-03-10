import pandas as pd
import random
import numpy as np
from faker import Faker

fake = Faker()


'''
=====================================
CREATING BOOKS.CSV
    isbn VARCHAR(13)
    author VARCHAR(255)
    title VARCHAR(255)
    publisher VARCHAR(50)
    year_published YEAR
    synopsis TEXT
    language_code CHAR(3)
    num_pages INT
    cover_photo BLOB
    series_name VARCHAR(255)
=====================================
'''
PERCENT_SERIES = 0.2

books_df = pd.read_csv("books.csv")
'''
imported data has columns for: 
isbn, author, title, publisher, year_published, language_code, num_pages
'''

books_df['year_published'] = pd.to_datetime(books_df['year_published'], errors='coerce').dt.year
books_df['synopsis'] = [fake.paragraph(nb_sentences=5, variable_nb_sentences=True) for _ in range(len(books_df))]
books_df['author'] = books_df['author'].str.split('/').str[0]
books_df['cover_photo'] = [fake.binary(length=1000) for _ in range(len(books_df))]

series_books_mapping = {} 
for _ in range(int(len(books_df) * PERCENT_SERIES)):
    series_name = fake.sentence(nb_words=3)
    num_books_in_series = random.randint(2, 10)
    book_indices = np.random.choice(books_df.index, num_books_in_series, replace=False)
    series_books_mapping[series_name] = book_indices

books_df['series_name'] = ''
for series_name, book_indices in series_books_mapping.items():
    books_df.loc[book_indices, 'series_name'] = series_name



'''
=====================================
CREATING USERS.CSV
    user_id INT
    first_name VARCHAR(30)
    last_name VARCHAR(30)
    email VARCHAR(320)
    password VARCHAR(30)
    join_date TIMESTAMP
=====================================
'''
NUMBER_USERS = 500

def generate_email(first, last, domain):
    first = first.lower()
    last = last.lower()
    email_formats = {
        1: lambda first, last: f"{first}.{last}",
        2: lambda first, last: f"{first[0]}{last}",
        3: lambda first, last: f"{first}_{last}",
        4: lambda first, last: f"{first}{last}",
        5: lambda first, last: f"{first[0]}{last}{random.randint(0, 999)}",
        6: lambda first: f"{first}{fake.word().lower()}{random.randint(0, 999)}",
        7: lambda first, last: f"{first[0]}{last}{fake.word().lower()}",
        8: lambda: f"{fake.word().lower()}{fake.word().lower()}{random.randint(0, 999)}"
    }
    email_format = email_formats[random.randint(1, 8)]
    return f"{email_format}@{domain}"

users_data = []
for _ in range(NUMBER_USERS):
    first_name = fake.first_name()
    last_name = fake.last_name()
    domains = random.choice(["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com"])
    email = generate_email(first_name, last_name, random.choice(domains))
    while email in users_data[2]:
        email = generate_email(first_name, last_name, random.choice(domains))
    password = fake.password()
    join_date = fake.date_time_this_decade()
    users_data.append((first_name, last_name, email, password, join_date))

users_df = pd.DataFrame(users_data, columns=['first_name', 'last_name', 'email', 'password', 'join_date'])


'''
=====================================
CREATING FRIENDS.CSV
    user_id INT
    friend_id INT
=====================================
'''
MAX_FRIENDS = 50

friend_tuples = set()
for i in range(NUMBER_USERS):
    num_friends = random.randint(0, MAX_FRIENDS)
    friends = random.sample(range(NUMBER_USERS), num_friends)
    for friend in friends:
        if friend != i:
            friend_tuples.add((i, friend))
            friend_tuples.add((friend, i))

friends_df = pd.DataFrame(friend_tuples, columns=['user_id', 'friend_id'])


'''
=====================================
CREATING REVIEWS.CSV
    review_id INT
    user_id INT
    isbn VARCHAR(13)
    star_rating DECIMAL(2, 1)
    review_text TEXT
    review_date TIMESTAMP
=====================================
'''    
reviews_df = pd.DataFrame(columns=['review_id', 'user_id', 'isbn', 'star_rating', 'review_text', 'review_date'])
for user_id in users_df['user_id']:
    num_reviews = random.randint(0, 10)
    for _ in range(num_reviews):
        isbn = random.choice(books_df['isbn'])
        star_rating = round(random.uniform(0.5, 5.0), 1)
        review_text = fake.paragraph(nb_sentences=6, variable_nb_sentences=True)
        review_date = fake.date_time_this_decade()
        reviews_df = reviews_df.append({'user_id': user_id, 'isbn': isbn, 'star_rating': star_rating, 'review_text': review_text, 'review_date': review_date}, ignore_index=True)

'''    
=====================================
CREATING SHELVES.CSV
    shelf_id INT
    user_id INT
    shelf_name VARCHAR(255)
    is_private BOOLEAN
=====================================
'''    
shelves_df = pd.DataFrame(columns=['shelf_id', 'user_id', 'shelf_name', 'is_private'])

for user_id in users_df['user_id']:
    default_shelves = ["favorites", "has read", "wants to read", "currently reading"]
    for shelf_name in default_shelves:
        is_private = random.choice([True, False])
        shelves_df = shelves_df.append({'user_id': user_id, 'shelf_name': shelf_name, 'is_private': is_private}, ignore_index=True)

    num_shelves = random.randint(0, 5)
    for _ in range(num_shelves):
        shelf_name = fake.sentence(nb_words=5)
        is_private = random.choice([True, False])
        shelves_df = shelves_df.append({'user_id': user_id, 'shelf_name': shelf_name, 'is_private': is_private}, ignore_index=True)

'''    
=====================================
CREATING ON_SHELF.CSV
    isbn VARCHAR(13)
    shelf_id INT 
=====================================
'''
MEAN_BOOKS = 10

on_shelf_df = pd.DataFrame(columns=['isbn', 'shelf_id'])

for shelf_id in shelves_df['shelf_id']:
    num_books = max(0, min(int(np.random.normal(MEAN_BOOKS, 3)), len(books_df)))
    for isbn in random.sample(books_df['isbn'], num_books):
        on_shelf_df = on_shelf_df.append({'isbn': isbn, 'shelf_id': shelf_id}, ignore_index=True)

'''    
=====================================
CREATING GENRES.CSV
    genre name VARCHAR(50)
=====================================
'''
genres = ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", "Mystery", "Thriller", "Romance", "Western", "Dystopian", "Historical Fiction", "Horror", "Memoir", "Biography", "Self-Help", "Cooking", "Art", "Travel", "Religion", "Science", "History", "Math", "Poetry", "Philosophy", "Business", "Economics", "Psychology", "Sociology", "Political Science", "Education", "Technology", "Health", "Fitness", "Sports", "Nature", "Animals", "Crafts", "Hobbies", "Music", "Film", "Theatre", "Television", "Gaming", "Comics", "Graphic Novels", "Manga", "Children's", "Young Adult", "Adult", "Elderly", "LGBTQ+", "Feminism"]
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
books_df.to_csv("gen_csvs/books.csv", index=False)
users_df.to_csv("gen_csvs/users.csv", index=False)
friends_df.to_csv("gen_csvs/friends.csv", index=False)
reviews_df.to_csv("gen_csvs/reviews.csv", index=False)
shelves_df.to_csv("gen_csvs/shelves.csv", index=False)
on_shelf_df.to_csv("gen_csvs/on_shelf.csv", index=False)
genres_df.to_csv("gen_csvs/genres.csv", index=False)
book_genres_df.to_csv("gen_csvs/book_genres.csv", index=False)