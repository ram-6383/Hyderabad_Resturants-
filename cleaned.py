import pandas as pd

# Load original CSV
df = pd.read_csv("HyderabadResturants.csv")

# Cleaning steps

# 1. Drop rows missing restaurant name or price (essential info)
df = df.dropna(subset=['names', 'price for one'])

# 2. Convert ratings to float, set invalid as NaN, then fill with 0
df['ratings'] = pd.to_numeric(df['ratings'], errors='coerce').fillna(0)

# 3. Strip whitespace from strings in 'names' and 'cuisine'
df['names'] = df['names'].str.strip()
df['cuisine'] = df['cuisine'].str.strip()

# 4. Convert 'price for one' to integer, set invalid as 0
df['price for one'] = pd.to_numeric(df['price for one'], errors='coerce').fillna(0).astype(int)

# 5. Optional: Remove duplicate restaurants by name (keep first)
df = df.drop_duplicates(subset=['names'])

# Save cleaned data to a new CSV file
df.to_csv('cleaned_hyderabad_restaurants.csv', index=False)

print("Cleaning done. Cleaned data saved to 'cleaned_hyderabad_restaurants.csv'")
