import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
from datetime import datetime, timezone

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.5",
    "Connection": "keep-alive",
}

BASE_URL = "https://www.tesco.com/groceries/en-GB/search?query={}&page={}"


def fetch_page(query, page):
    url = BASE_URL.format(query, page)
    response = requests.get(url, headers=HEADERS)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'html.parser')


def extract_product(soup):
    return soup.find_all('div', class_='_ecrjxvBD_ol38Z')


def clean_price(price_text):
    if not price_text:
        return None
    try:
        return float(price_text.replace('£', '').strip())
    except:
        return None


def parse_products(product):
    name = product.find('a', class_='gyT8MW_titleLink')
    price = product.find('p', class_='gyT8MW_priceText')
    price_per_kg = product.find('p', class_='gyT8MW_subtext')

    return {
        'name': name.text.strip() if name else None,
        'price': clean_price(price.text.strip()) if price else None,
        'price_per_kg': price_per_kg.text.strip() if price_per_kg else None
    }


CATEGORIES = ['chicken', 'beef', 'fish', 'milk', 'eggs', 'bread']


def run_scraper(max_pages=3):
    all_products = []
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    for category in CATEGORIES:
        print(f"Scraping {category}...")

        for page in range(1, max_pages + 1):
            soup = fetch_page(category, page)
            products = extract_product(soup)

            for product in products:
                data = parse_products(product)
                data['category'] = category
                all_products.append(data)

            print(f"  Page {page}: {len(products)} products")
            time.sleep(1)

    df = pd.DataFrame(all_products)

    # Clean data
    df = df.dropna(subset=["name", "price"])

    # 🔥 GUARANTEED DATE COLUMN
    df["date"] = today

    print(f"\n✅ Total scraped: {len(df)}")
    return df


def save_data(new_df, file="tesco_data.csv"):
    if os.path.exists(file):
        old_df = pd.read_csv(file)

        # 🔥 FIX: ensure old file has required columns
        for col in ["name", "price", "price_per_kg", "category", "date"]:
            if col not in old_df.columns:
                old_df[col] = None

        combined_df = pd.concat([old_df, new_df], ignore_index=True)

    else:
        combined_df = new_df

    # 🔥 REMOVE DUPLICATES SAFELY
    combined_df = combined_df.drop_duplicates(
        subset=["name", "category", "date"],
        keep="last"
    )

    # Optional: sort for readability
    combined_df = combined_df.sort_values(by=["date", "category"])

    combined_df.to_csv(file, index=False)

    print(f"✅ Data saved to {file} (rows: {len(combined_df)})")


if __name__ == "__main__":
    df = run_scraper(max_pages=3)
    save_data(df)
