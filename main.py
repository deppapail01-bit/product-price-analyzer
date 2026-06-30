import requests
from bs4 import BeautifulSoup
url = 'https://books.toscrape.com'

response = requests.get(url)

print(response.status_code)

soup = BeautifulSoup(response.text, 'html.parser')


books = soup.find_all("article",class_="product_pod")

print(len(books))

books_data = []
for book in books:
    title=book.find("h3").find("a")["title"]
    price=book.find("p",class_="price_color").text
    availability=book.find("p",class_="instock availability").text.strip()
    print(f"Title: {title}, Price: {price}, Availability: {availability}")
    rating=book.find("p",class_="star-rating")["class"][1]
    link=book.find("h3").find("a")["href"]

    book_data = {
        "title": title,
        "price": price,
        "rating": rating,
        "availability": availability,
        "link": link
    }

    books_data.append(book_data)

    print(books_data)