import sqlite3
import pandas as pd
from contextlib import redirect_stdout


DB_PATH = "data_pipeline/database/zepto_catalog.db"
OUTPUT_PATH = "data_pipeline/outputs/pandas_validation.txt"


def main():

    conn = sqlite3.connect(DB_PATH)

    # --------------------------------------------------
    # 1. Read SQL query using pd.read_sql()
    # --------------------------------------------------

    query_1 = """
    SELECT title, price_gbp
    FROM books
    WHERE price_gbp > 30
    ORDER BY price_gbp DESC
    LIMIT 10
    """

    result_sql_1 = pd.read_sql(query_1, conn)

    print("=" * 70)
    print("SQL RESULT 1 - pd.read_sql()")
    print("=" * 70)
    print(result_sql_1.to_string(index=False))

    # --------------------------------------------------
    # 2. Read SQL JOIN using pd.read_sql()
    # --------------------------------------------------

    join_query = """
    SELECT
        books.title,
        books.price_gbp,
        books.rating,
        categories.category_name
    FROM books
    JOIN categories
        ON books.category_id = categories.category_id
    ORDER BY books.price_gbp DESC
    LIMIT 10
    """

    result_sql_join = pd.read_sql(join_query, conn)

    print("\n" + "=" * 70)
    print("SQL JOIN RESULT - pd.read_sql()")
    print("=" * 70)
    print(result_sql_join.to_string(index=False))

    # --------------------------------------------------
    # 3. Read both database tables into DataFrames
    # --------------------------------------------------

    books_df = pd.read_sql(
        "SELECT * FROM books",
        conn
    )

    categories_df = pd.read_sql(
        "SELECT * FROM categories",
        conn
    )

    # --------------------------------------------------
    # 4. Reproduce SQL JOIN using pd.merge()
    # --------------------------------------------------

    merged_df = pd.merge(
        books_df,
        categories_df,
        on="category_id",
        how="inner"
    )

    result_pandas_join = merged_df[
        [
            "title",
            "price_gbp",
            "rating",
            "category_name"
        ]
    ].sort_values(
        by="price_gbp",
        ascending=False
    ).head(10).reset_index(drop=True)

    result_sql_join = result_sql_join.reset_index(drop=True)

    print("\n" + "=" * 70)
    print("PANDAS JOIN RESULT - pd.merge()")
    print("=" * 70)
    print(result_pandas_join.to_string(index=False))

    # --------------------------------------------------
    # 5. Compare SQL JOIN and pandas merge
    # --------------------------------------------------

    results_match = result_sql_join.equals(result_pandas_join)

    print("\n" + "=" * 70)
    print("VALIDATION")
    print("=" * 70)

    print("SQL JOIN and pandas merge match:", results_match)

    conn.close()


if __name__ == "__main__":

    # Save everything printed by the program
    with open(OUTPUT_PATH, "w", encoding="utf-8") as output_file:
        with redirect_stdout(output_file):
            main()

    # Also tell us where the file was saved
    print(f"Validation output saved to: {OUTPUT_PATH}")