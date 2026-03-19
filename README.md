# Tesco UK Grocery Price Scraper 🛒

A Python web scraper that collects real-time grocery price data from Tesco UK across multiple categories.

## What it does
- Scrapes product names, prices, and price-per-kg across 6 categories
- Categories: chicken, beef, fish, milk, eggs, bread
- Collects 400+ products per run
- Runs automatically every day via GitHub Actions
- Saves data to CSV with scraped date for time-series analysis

## Tech Stack
- Python 3.12
- BeautifulSoup4
- Pandas
- Requests
- GitHub Actions (automated daily scraping)

## Project Structure
```
tesco-scraper/
├── scraper.py          # main scraper
├── requirements.txt
├── .github/
│   └── workflows/
│       └── scraper.yml # daily automation
└── tesco_data.csv      # collected data
```

## How to run
```bash
git clone https://github.com/Delphineuzoeto/tesco-scraper.git
cd tesco-scraper
pip install -r requirements.txt
python scraper.py
```
