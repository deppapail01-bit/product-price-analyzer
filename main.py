import pandas as pd
from database import save_books_to_database
from database import load_books_from_database

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
with pd.ExcelWriter("books_report.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="All Books", index=False)
    sorted_books.to_excel(writer, sheet_name="Sorted by Price", index=False)

    workbook = writer.book

    for sheet_name in writer.sheets:
        worksheet = writer.sheets[sheet_name]

        # Freeze πρώτη γραμμή
        worksheet.freeze_panes = "A2"

        # Auto filter
        worksheet.auto_filter.ref = worksheet.dimensions

        # Πλάτος στηλών
        worksheet.column_dimensions["A"].width = 45
        worksheet.column_dimensions["B"].width = 12
        worksheet.column_dimensions["C"].width = 12
        worksheet.column_dimensions["D"].width = 15
        worksheet.column_dimensions["E"].width = 60

        # Μορφοποίηση header
        for cell in worksheet[1]:
            cell.font = cell.font.copy(bold=True)
            cell.alignment = cell.alignment.copy(horizontal="center")

        # Μορφοποίηση price column
        for cell in worksheet["B"][1:]:
            cell.number_format = '£0.00'
df.to_excel("books.xlsx", index=False)
sorted_books.to_excel("books_sorted_by_price.xlsx", index=False)

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

save_books_to_database(df)

print("\n===== DATA FROM DATABASE =====")

database_df = load_books_from_database()

print(database_df.head())

choice = input("""
========== BOOK ANALYZER ==========

1. Όλα τα βιβλία
2. Βιβλία με 5 αστέρια
3. Top 5 ακριβότερα
4. Μέση τιμή
5. Έξοδος

Επιλογή: 
""")

if choice == "1":
    query = "SELECT * FROM books"
    result = load_books_from_database(query)
    print(result)

elif choice == "2":
    query = """
    SELECT *
    FROM books
    WHERE rating = 'Five'
    """
    result = load_books_from_database(query)
    print(result)

elif choice == "3":
    query = """
    SELECT *
    FROM books
    ORDER BY price DESC
    LIMIT 5
    """
    result = load_books_from_database(query)
    print(result)

elif choice == "4":
    query = """
    SELECT AVG(price) AS average_price
    FROM books
    """
    result = load_books_from_database(query)
    print(result)

elif choice == "5":
    print("Έξοδος από το πρόγραμμα.")

else:
    print("Μη έγκυρη επιλογή. Παρακαλώ δοκιμάστε ξανά.")