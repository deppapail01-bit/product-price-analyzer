import pandas as pd

from scraper import scrape_books
from analysis import (
    clean_price_column,
    get_most_expensive_book,
    get_cheapest_book,
    get_average_price,
)


url = "https://books.toscrape.com"

books_data = scrape_books(url)

df = pd.DataFrame(books_data)

df = clean_price_column(df)

most_expensive_book = get_most_expensive_book(df)
cheapest_book = get_cheapest_book(df)
average_price = get_average_price(df)

sorted_books = df.sort_values(by="price", ascending=False)

print("========== BOOK ANALYZER ==========")

print(f"\n📚 Συνολικά βιβλία: {len(df)}")
print(f"\n💰 Μέση τιμή: £{average_price:.2f}")

print("\n📈 Ακριβότερο βιβλίο")
print(f"Title : {most_expensive_book['title']}")
print(f"Price : £{most_expensive_book['price']:.2f}")
print(f"Rating: {most_expensive_book['rating']}")

print("\n📉 Φθηνότερο βιβλίο")
print(f"Title : {cheapest_book['title']}")
print(f"Price : £{cheapest_book['price']:.2f}")
print(f"Rating: {cheapest_book['rating']}")

print("\nTop 5 πιο ακριβά βιβλία")
print(sorted_books.head())

print("\n===================================")