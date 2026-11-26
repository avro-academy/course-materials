"""Module 3: the complete cleaning script. Run from the starter folder: python scripts/clean_sales.py"""
import pandas as pd

df = pd.read_csv("data/cafe_sales_2025.csv")
start = len(df)
df = df.drop_duplicates()                                      # 1. exact duplicate rows
df["item"] = df["item"].str.strip().str.capitalize()           # 2. tidy text
df["payment"] = df["payment"].str.title().fillna("Unknown")
df["unit_price"] = df["unit_price"].str.replace("$", "", regex=False).astype(float)   # 3. types
df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
df = df[df["quantity"] != 120]                                 # 4. typo: order 12346 (checked with manager)
df = df.dropna(subset=["quantity"])                            # 5. can't use rows with no quantity
df["quantity"] = df["quantity"].astype(int)
df["revenue"] = df["quantity"] * df["unit_price"]              # 6. new column
print(f"{start} rows in, {len(df)} rows out")
print(f"Total revenue: ${df['revenue'].sum():,.2f}")
df.to_csv("data/cafe_sales_2025_clean.csv", index=False)
