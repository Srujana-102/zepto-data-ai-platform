import sqlite3
import pandas as pd


DB_PATH = "data_pipeline/database/zepto_catalog.db"
CSV_PATH = "data_pipeline/data/clean_books.csv"


def create_database():
    # Read cleaned dataset
    df = pd.read_csv(CSV_PATH)

    # Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    # Enable foreign key support
    cursor.execute("PRAGMA foreign_keys = ON")

    # Drop old tables if they exist
    cursor.execute("DROP TABLE IF EXISTS books")
    cursor.execute("DROP TABLE IF EXISTS categories")

    # -----------------------------
    # Create categories table
    # -----------------------------
    cursor.execute("""
        CREATE TABLE categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL UNIQUE
        )
    """)

    # -----------------------------
    # Create books table
    # -----------------------------
    cursor.execute("""
        CREATE TABLE books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price_gbp REAL,
            price_inr REAL,
            rating INTEGER,
            in_stock INTEGER,
            category_id INTEGER,
            FOREIGN KEY (category_id)
                REFERENCES categories(category_id)
        )
    """)

    # -----------------------------
    # Insert unique categories
    # -----------------------------
    categories = df["category"].dropna().unique()

    for category in categories:
        cursor.execute(
            "INSERT INTO categories (category_name) VALUES (?)",
            (category,)
        )

    # -----------------------------
    # Insert books
    # -----------------------------
    for _, row in df.iterrows():

        # Find category ID
        cursor.execute(
            """
            SELECT category_id
            FROM categories
            WHERE category_name = ?
            """,
            (row["category"],)
        )

        category_id = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO books
            (
                title,
                price_gbp,
                price_inr,
                rating,
                in_stock,
                category_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                row["title"],
                row["price_gbp"],
                row["price_inr"],
                row["rating"],
                int(row["in_stock"]),
                category_id
            )
        )

    # Save changes
    conn.commit()

    # -----------------------------
    # Verify database
    # -----------------------------
    cursor.execute("SELECT COUNT(*) FROM books")
    book_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM categories")
    category_count = cursor.fetchone()[0]

    print("=" * 60)
    print("DATABASE CREATED SUCCESSFULLY")
    print("=" * 60)

    print(f"Books inserted: {book_count}")
    print(f"Categories inserted: {category_count}")

    conn.close()


if __name__ == "__main__":
    create_database()