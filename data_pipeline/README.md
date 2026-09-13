# Module 1 - Data Pipeline

## Overview

This module builds an end-to-end data pipeline for book data from the public
Books to Scrape website.

The pipeline performs:

1. Web scraping using Requests and BeautifulSoup.
2. Data cleaning and type conversion.
3. GBP to INR price conversion.
4. SQLite database creation with normalized tables.
5. SQL querying and analysis.
6. Validation using pandas `read_sql()` and `merge()`.

---

## Source

Data source:

Books to Scrape - https://books.toscrape.com/

The website is a public practice website for web scraping.

The scraper collects data from the first five catalogue pages.

The final dataset contains 100 books across 29 categories.

---

## Technologies

- Python
- Requests
- BeautifulSoup
- Pandas
- SQLite
- SQL

---

## Project Files

### `scraper.py`

Scrapes book information from the website.

The following fields are collected:

- title
- price
- star_rating
- availability
- category
- book_url

The first five catalogue pages are scraped.

---

### `pipeline.py`

Cleans the raw scraped data.

Cleaning operations include:

- Removing the pound currency symbol from prices.
- Converting price to numeric `price_gbp`.
- Converting One, Two, Three, Four and Five to ratings 1-5.
- Converting availability text to boolean `in_stock`.
- Handling invalid numeric values using median imputation.
- Creating `price_inr`.

---

## Currency Conversion

The assignment requires the fixed conversion rate:

**1 GBP = 105.50 INR**

No live currency API is used.

The conversion is:

```text
price_inr = price_gbp * 105.50