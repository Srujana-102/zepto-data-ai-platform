import pandas as pd


# Required fixed conversion rate from the assignment
GBP_TO_INR = 105.50


def clean_price(price):
    """Convert price such as Â£51.77 into a numeric value."""
    try:
        price = str(price)
        price = price.replace("Â£", "").replace("£", "").strip()
        return float(price)
    except (ValueError, TypeError):
        return None


def clean_rating(rating):
    """Convert One, Two, Three, Four, Five into 1-5."""
    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    return rating_map.get(str(rating).strip(), None)


def clean_availability(value):
    """Convert availability text into True/False."""
    if pd.isna(value):
        return False

    return "in stock" in str(value).lower()


def main():

    input_path = "data_pipeline/data/raw_books.csv"
    output_path = "data_pipeline/data/clean_books.csv"

    # Load scraped data
    df = pd.read_csv(input_path)

    print("=" * 60)
    print("RAW DATA")
    print("=" * 60)

    print(df.head())
    print("\nData types before cleaning:")
    print(df.dtypes)

    # -----------------------------
    # Clean price
    # -----------------------------
    df["price_gbp"] = df["price"].apply(clean_price)

    # -----------------------------
    # Clean rating
    # -----------------------------
    df["rating"] = df["star_rating"].apply(clean_rating)

    # -----------------------------
    # Clean availability
    # -----------------------------
    df["in_stock"] = df["availability"].apply(clean_availability)

    # -----------------------------
    # Handle invalid numeric values
    # -----------------------------
    price_median = df["price_gbp"].median()
    rating_median = df["rating"].median()

    df["price_gbp"] = df["price_gbp"].fillna(price_median)
    df["rating"] = df["rating"].fillna(rating_median).round().astype(int)

    # -----------------------------
    # Convert GBP to INR
    # -----------------------------
    df["price_inr"] = df["price_gbp"] * GBP_TO_INR

    # -----------------------------
    # Keep required columns
    # -----------------------------
    df = df[
        [
            "title",
            "price_gbp",
            "price_inr",
            "rating",
            "in_stock",
            "category",
            "book_url"
        ]
    ]

    # -----------------------------
    # Save cleaned dataset
    # -----------------------------
    df.to_csv(output_path, index=False)

    print("\n" + "=" * 60)
    print("CLEANING COMPLETE")
    print("=" * 60)

    print(f"Total rows: {len(df)}")

    print("\nCleaned data:")
    print(df.head())

    print("\nData types after cleaning:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

    print(f"\nFixed GBP to INR conversion rate: {GBP_TO_INR}")

    print(f"\nCleaned dataset saved to: {output_path}")


if __name__ == "__main__":
    main()