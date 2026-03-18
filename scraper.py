import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}

BASE_URL = "https://www.tesco.com/groceries/en-GB/search?query={}&page={}"

def fetch_page(query, page):
    url = BASE_URL.format(query, page)
    response = requests.get(url, headers=HEADERS)
    response.encoding='utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


### ------------------------------------ff-----------------------------------------
## run tesco_test.py → prettify() shows new class names → update scraper → done, (incase  any  of the classname below changes from the website)

##EXTRACT PRODUCT
def extract_product(soup):
    products = soup.find_all('div', class_='_ecrjxvBD_ol38Z')
    return products

def parse_products(product):
    name = product.find('a', class_='gyT8MW_titleLink')
    price = product.find('p', class_='gyT8MW_priceText')
    price_per_kg = product.find('p', class_='gyT8MW_subtext')

    return {
        'name': name.text.strip() if name else None,
        'price': price.text.strip() if price else None,
        'price_per_kg': price_per_kg.text.strip() if price_per_kg else None
    }



CATEGORIES = ['chicken', 'beef', 'fish', 'milk', 'eggs', 'bread']
def run_scraper(max_pages=3):
    all_products = []

    for category in CATEGORIES:
        print(f"Scraping {category}...")

        for page in range(1, max_pages + 1):
            print(f" page{page}/{max_pages}")
            soup = fetch_page(category, page)
            products = extract_product(soup)


            for product in products:
                data = parse_products(product)
                data['category'] = category
                all_products.append(data)

            print(f" {len(products)} products found")
            time.sleep(1)
    df = pd.DataFrame(all_products)
    print(f"\n✅ Total: {len(df)} products scraped")
    return df

if __name__ ==  "__main__":
    df = run_scraper(max_pages=3)
    df.to_csv("tesco_data.csv", index=False)
    print("Saved to tesco_data.csv")