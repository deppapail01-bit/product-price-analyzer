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


def load_books_from_database(query="SELECT * FROM books", database_name="books.db"):
    connection = sqlite3.connect(database_name)

    
    df = pd.read_sql_query(query, connection)

    connection.close()

    return df