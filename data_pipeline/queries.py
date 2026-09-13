import sqlite3
import pandas as pd


DB_PATH = "data_pipeline/database/zepto_catalog.db"
OUTPUT_PATH = "data_pipeline/outputs/sql_results.txt"


def run_queries():

    conn = sqlite3.connect(DB_PATH)

    queries = {

        "QUERY 1 - Books costing more than £30":
        """
        SELECT title, price_gbp
        FROM books
        WHERE price_gbp > 30
        """,

        "QUERY 2 - Most expensive books":
        """
        SELECT title, price_gbp
        FROM books
        ORDER BY price_gbp DESC
        LIMIT 10
        """,

        "QUERY 3 - Distinct ratings":
        """
        SELECT DISTINCT rating
        FROM books
        ORDER BY rating
        """,

        "QUERY 4 - Books rated 4 or 5":
        """
        SELECT title, rating
        FROM books
        WHERE rating IN (4, 5)
        ORDER BY rating DESC
        """,

        "QUERY 5 - Books between £20 and £40":
        """
        SELECT title, price_gbp
        FROM books
        WHERE price_gbp BETWEEN 20 AND 40
        ORDER BY price_gbp
        """,

        "QUERY 6 - Books with their categories":
        """
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
    }

    output_lines = []

    for name, query in queries.items():

        print("\n" + "=" * 60)
        print(name)
        print("=" * 60)

        print("SQL:")
        print(query.strip())

        # Read SQL result into pandas DataFrame
        result = pd.read_sql(query, conn)

        print("\nResult:")
        print(result.to_string(index=False))

        # Save query and output
        output_lines.append("=" * 60)
        output_lines.append(name)
        output_lines.append("=" * 60)
        output_lines.append("SQL:")
        output_lines.append(query.strip())
        output_lines.append("\nRESULT:")
        output_lines.append(result.to_string(index=False))
        output_lines.append("\n")

    conn.close()

    # Save all queries and outputs
    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        file.write("\n".join(output_lines))

    print("\n" + "=" * 60)
    print(f"All SQL queries and outputs saved to: {OUTPUT_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    run_queries()