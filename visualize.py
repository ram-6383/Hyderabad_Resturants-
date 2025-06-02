import pandas as pd
import numpy as np  # <-- ✅ This is required for np.log1p
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load dataset
df = pd.read_csv("HyderabadResturants.csv")

# -----------------------------
# 📌 Data Cleaning
# -----------------------------

# Strip whitespace from object (string) columns
df = df.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)

# Replace empty strings with NaN
df.replace('', pd.NA, inplace=True)

# Convert 'ratings' to numeric, coerce errors to NaN
df['ratings'] = pd.to_numeric(df['ratings'], errors='coerce')

# Drop rows with missing critical values
df.dropna(subset=['names', 'ratings', 'price for one', 'cuisine'], inplace=True)

# Remove duplicates
df.drop_duplicates(subset=['names', 'cuisine', 'price for one'], keep='first', inplace=True)

# -----------------------------
# 📌 Data Transformation
# -----------------------------

# Extract primary cuisine (first cuisine mentioned)
df['primary_cuisine'] = df['cuisine'].apply(lambda x: x.split(',')[0] if isinstance(x, str) else x)

# Convert column names to lowercase and replace spaces with underscores
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Optionally, normalize price for one (log scale) – helpful for visualization
df['log_price'] = df['price_for_one'].apply(lambda x: np.log1p(x) if x > 0 else 0)

# -----------------------------
# 📊 Data Analysis & Visualization
# -----------------------------

# Plot 1: Ratings Distribution
plt.figure(figsize=(8, 4))
sns.histplot(df['ratings'], bins=20, kde=True, color='skyblue')
plt.title('Distribution of Restaurant Ratings')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot 2: Top 10 Primary Cuisines
top_cuisines = df['primary_cuisine'].value_counts().head(10)
plt.figure(figsize=(10, 5))
sns.barplot(x=top_cuisines.index, y=top_cuisines.values, palette='viridis')
plt.title('Top 10 Primary Cuisines')
plt.xlabel('Cuisine')
plt.ylabel('Number of Restaurants')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot 3: Price vs Rating Scatter Plot
plt.figure(figsize=(8, 5))
sns.scatterplot(x='price_for_one', y='ratings', data=df, hue='primary_cuisine', legend=False)
plt.title('Price vs. Ratings by Primary Cuisine')
plt.xlabel('Price for One (₹)')
plt.ylabel('Rating')
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot 4: Word Cloud for All Cuisines
cuisine_text = ', '.join(df['cuisine'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='plasma').generate(cuisine_text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Popular Cuisines Word Cloud')
plt.tight_layout()
plt.show()

# Plot 5: Boxplot - Price by Top 5 Cuisines
top5_cuisines = df['primary_cuisine'].value_counts().nlargest(5).index
filtered_df = df[df['primary_cuisine'].isin(top5_cuisines)]
plt.figure(figsize=(10, 6))
sns.boxplot(x='primary_cuisine', y='price_for_one', data=filtered_df, palette='coolwarm')
plt.title('Price Distribution by Top 5 Cuisines')
plt.xlabel('Cuisine')
plt.ylabel('Price for One (₹)')
plt.tight_layout()
plt.show()

# Plot 6: Correlation Heatmap
plt.figure(figsize=(5, 4))
sns.heatmap(df[['ratings', 'price_for_one']].corr(), annot=True, cmap='Blues')
plt.title('Correlation between Ratings and Price')
plt.tight_layout()
plt.show()
