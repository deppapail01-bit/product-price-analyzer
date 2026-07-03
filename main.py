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