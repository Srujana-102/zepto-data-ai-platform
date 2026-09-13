import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import time


BASE_URL = "https://books.toscrape.com/"
CATALOGUE_URL = "https://books.toscrape.com/catalogue/"


def get_soup(url):
    """Download a webpage and return its BeautifulSoup object."""
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def get_category(book_url):
    """Open a book page and extract its category from the breadcrumb."""
    try:
        soup = get_soup(book_url)

        breadcrumb = soup.select("ul.breadcrumb li a")

        # Breadcrumb normally looks like:
        # Home -> Books -> Category
        if len(breadcrumb) >= 3:
            return breadcrumb[2].get_text(strip=True)

        return "Unknown"

    except Exception as e:
        print(f"Category error for {book_url}: {e}")
        return "Unknown"


def scrape_pages(number_of_pages=5):
    """Scrape books from the first five catalogue pages."""

    books = []

    for page_number in range(1, number_of_pages + 1):

        page_url = f"{CATALOGUE_URL}page-{page_number}.html"

        print(f"\nScraping page {page_number}: {page_url}")

        try:
            soup = get_soup(page_url)

        except Exception as e:
            print(f"Could not load page {page_number}: {e}")
            continue

        book_cards = soup.select("article.product_pod")

        print(f"Books found on page: {len(book_cards)}")

        for book in book_cards:

            try:
                # Title
                title_tag = book.select_one("h3 a")
                title = title_tag.get("title", "").strip()

                # Book URL
                relative_url = title_tag.get("href")
                book_url = urljoin(page_url, relative_url)

                # Price
                price = book.select_one("p.price_color").get_text(strip=True)

                # Star rating
                rating_tag = book.select_one("p.star-rating")
                rating_classes = rating_tag.get("class", [])

                if len(rating_classes) >= 2:
                    star_rating = rating_classes[1]
                else:
                    star_rating = "Unknown"

                # Availability
                availability = book.select_one(
                    "p.instock.availability"
                ).get_text(" ", strip=True)

                # Category from individual book page
                category = get_category(book_url)

                books.append({
                    "title": title,
                    "price": price,
                    "star_rating": star_rating,
                    "availability": availability,
                    "category": category,
                    "book_url": book_url
                })

                print(f"  ✓ {title}")

                # Small delay to be polite to the website
                time.sleep(0.1)

            except Exception as e:
                print(f"Error processing a book: {e}")

    return books


def main():

    # First five catalogue pages = 100 books on the standard site
    books = scrape_pages(number_of_pages=5)

    df = pd.DataFrame(books)

    print("\n" + "=" * 60)
    print("SCRAPING COMPLETE")
    print("=" * 60)

    print(f"Total books scraped: {len(df)}")

    print("\nCategories found:")
    print(df["category"].value_counts())

    print("\nFirst 5 rows:")
    print(df.head())

    # Save raw dataset
    output_path = "data_pipeline/data/raw_books.csv"

    df.to_csv(output_path, index=False)

    print(f"\nRaw data saved to: {output_path}")


if __name__ == "__main__":
    main()