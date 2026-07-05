import sqlite3


def save_books_to_database(df, database_name="books.db"):
    connection = sqlite3.connect(database_name)

    df.to_sql(
        "books",
        connection,
        if_exists="replace",
        index=False
    )

    connection.close()