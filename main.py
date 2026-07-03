import requests
from bs4 import BeautifulSoup
import pandas as pd


def clean_price_column(df):
    df["price"] = df["price"].str.replace("Â£", "", regex=False)
    df["price"] = df["price"].str.replace("£", "", regex=False)
    df["price"] = df["price"].astype(float)
    return df


def get_most_expensive_book(df):
    index = df["price"].idxmax()
    return df.loc[index]


def get_cheapest_book(df):
    index = df["price"].idxmin()
    return df.loc[index]


def get_average_price(df):
    return df["price"].mean()


url = "https://books.toscrape.com"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

books = soup.find_all("article", class_="product_pod")

books_data = []

for book in books:
    title = book.find("h3").find("a")["title"]
    price = book.find("p", class_="price_color").text
    availability = book.find("p", class_="instock availability").text.strip()
    rating = book.find("p", class_="star-rating")["class"][1]
    link = book.find("h3").find("a")["href"]

    book_data = {
        "title": title,
        "price": price,
        "rating": rating,
        "availability": availability,
        "link": link
    }

    books_data.append(book_data)


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