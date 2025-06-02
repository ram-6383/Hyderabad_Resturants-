from flask import Flask, render_template
from flask import Flask, render_template, url_for
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import os
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)

def load_and_clean_data():
    df = pd.read_csv("cleaned_hyderabad_restaurants.csv")
    df.dropna(inplace=True)
    df['ratings'] = pd.to_numeric(df['ratings'], errors='coerce')
    df['price for one'] = pd.to_numeric(df['price for one'], errors='coerce')
    return df

def plot_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return img_base64

@app.route("/")
def index():
    df = load_and_clean_data()

    # Plot 1: Ratings Histogram
    fig1, ax1 = plt.subplots()
    sns.histplot(df['ratings'], kde=True, bins=20, ax=ax1, color='skyblue')
    ax1.set_title("Ratings Distribution")
    rating_hist = plot_to_base64(fig1)

    # Plot 2: Price Histogram
    fig2, ax2 = plt.subplots()
    sns.histplot(df['price for one'], bins=20, kde=True, color='orange', ax=ax2)
    ax2.set_title("Price for One Distribution")
    price_hist = plot_to_base64(fig2)

    # Plot 3: Top 10 Cuisines
    cuisine_counts = df['cuisine'].str.split(', ').explode().value_counts().head(10)
    fig3, ax3 = plt.subplots()
    cuisine_counts.plot(kind='barh', ax=ax3, color='green')
    ax3.set_title("Top 10 Cuisines")
    cuisine_bar = plot_to_base64(fig3)

    # Plot 4: Top 10 Expensive Restaurants
    top_exp = df.sort_values("price for one", ascending=False).drop_duplicates("names").head(10)
    fig4, ax4 = plt.subplots()
    sns.barplot(x="price for one", y="names", data=top_exp, palette="Reds_r", ax=ax4)
    ax4.set_title("Top 10 Expensive Restaurants")
    exp_rest = plot_to_base64(fig4)

    # Plot 5: Rating vs Price Scatter
    fig5, ax5 = plt.subplots()
    sns.scatterplot(data=df, x="price for one", y="ratings", alpha=0.6, ax=ax5)
    ax5.set_title("Price vs Ratings")
    scatter_plot = plot_to_base64(fig5)

    # Plot 6: Cuisines with Highest Average Rating
    cuisine_avg = df.copy()
    cuisine_avg['cuisine'] = cuisine_avg['cuisine'].str.split(',').str[0]
    top_cuisine_ratings = cuisine_avg.groupby('cuisine')['ratings'].mean().sort_values(ascending=False).head(10)
    fig6, ax6 = plt.subplots()
    top_cuisine_ratings.plot(kind='bar', ax=ax6, color='purple')
    ax6.set_title("Top 10 Cuisines by Avg Rating")
    top_cuisine_plot = plot_to_base64(fig6)


    powerbi_image = url_for('static', filename='screenshots/Screenshot 2025-05-31 182224.png')

    

    insights = {
    "rating": "⭐ Most restaurants have ratings between **3.5 and 4.5**, indicating average to good customer satisfaction.",
    "price": "💰 The majority of restaurants charge between **₹150 to ₹300** per person, suggesting affordability for most.",
    "cuisine": "🍽️ **North Indian**, **Chinese**, and **Biryani** dominate the top cuisines — reflecting Hyderabad's flavor preferences.",
    "expensive": "👑 High-end restaurants can go up to **₹1000+** per person, mostly located in premium or posh areas.",
    "scatter": "📉 There’s **no strong correlation** between price and rating — expensive doesn’t always mean better!",
    "top_cuisine": "🍕 **Continental** and **Italian** cuisines tend to receive **higher average ratings**, hinting at consistent quality."
}



    return render_template("index.html",
                           rating_histogram=rating_hist,
                           price_histogram=price_hist,
                           cuisine_bar=cuisine_bar,
                           exp_rest=exp_rest,
                           scatter_plot=scatter_plot,
                           top_cuisine_plot=top_cuisine_plot,
                           powerbi_image=powerbi_image,
                           insights=insights
                        

)
if __name__ == "__main__":
    app.run(debug=True)
