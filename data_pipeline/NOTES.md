# Data Pipeline Implementation Notes

## Pipeline Flow

The pipeline follows this sequence:

1. `scraper.py` collects book information from Books to Scrape.
2. `pipeline.py` cleans the scraped data and converts GBP prices to INR.
3. `database.py` creates the normalized SQLite database.
4. `queries.py` executes SQL queries and saves their outputs.
5. `pandas_validation.py` validates the SQL JOIN using `pd.merge()`.

## Validation

The final validation confirmed that the SQL JOIN and pandas merge
produce matching results.

```text
SQL JOIN and pandas merge match: True