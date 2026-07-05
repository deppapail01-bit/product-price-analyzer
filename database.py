import sqlite3
import pandas as pd


def save_books_to_database(df, database_name="books.db"):
    connection = sqlite3.connect(database_name)

    df.to_sql(
        "books",
        connection,
        if_exists="replace",
        index=False
    )

    connection.close()


def run_query(query, database_name="books.db", params=None):
    connection = sqlite3.connect(database_name)

    result = pd.read_sql(query, connection, params=params)

    connection.close()

    return result


def get_all_books():
    query = "SELECT * FROM books"
    return run_query(query)


def get_five_star_books():
    query = """
    SELECT *
    FROM books
    WHERE rating = 'Five'
    """
    return run_query(query)


def get_top_5_expensive_books():
    query = """
    SELECT *
    FROM books
    ORDER BY price DESC
    LIMIT 5
    """
    return run_query(query)


def get_average_price():
    query = """
    SELECT AVG(price) AS average_price
    FROM books
    """
    return run_query(query)


def search_books_by_title(title):
    query = """
    SELECT *
    FROM books
    WHERE title LIKE ?
    """
    return run_query(query, params=(f"%{title}%",))


def get_books_by_price_range(min_price, max_price):
    query = """
    SELECT *
    FROM books
    WHERE price BETWEEN ? AND ?
    ORDER BY price ASC
    """
    return run_query(query, params=(min_price, max_price))


def get_books_by_rating(rating):
    query = """
    SELECT *
    FROM books
    WHERE rating = ?
    """
    return run_query(query, params=(rating,))