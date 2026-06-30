import requests
from bs4 import BeautifulSoup
url = 'https://books.toscrape.com'

response = requests.get(url)

print(response.status_code)

soup = BeautifulSoup(response.text, 'html.parser')
title=soup.find("h1")

books = soup.find_all("article")

print(type(books))
print(len(books))
print(books[0])
print(books[0])

print(title.text)
print(type(title))