from googlesearch import search
import requests
from bs4 import BeautifulSoup
import re
from app.llm_matcher import is_match

HEADERS = {"User-Agent": "Mozilla/5.0"}

def extract_price(text):
    match = re.search(r'[₹$€£]\s?[0-9,.]+', text)
    if match:
        raw = match.group()
        value = re.sub(r'[^0-9.]', '', raw)
        return value
    return None

def scrape_page(url, query, groq_api_key):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.title.string.strip() if soup.title else url
        text = soup.get_text(" ", strip=True)
        price = extract_price(text)

        if price and is_match(query, title, groq_api_key):
            return {
                "productName": title[:100],
                "price": price,
                "link": url,
                "currency": "USD" if '.com' in url else 'INR' if '.in' in url else 'GBP' if '.co.uk' in url else 'UNKNOWN'
            }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
    return None

def scrape_google_results(query, country, groq_api_key):
    search_query = f"{query} {country}"
    urls = list(search(search_query, num_results=10))
    results = []

    for url in urls:
        product = scrape_page(url, query, groq_api_key)
        if product:
            results.append(product)

    return sorted(results, key=lambda x: float(x['price']))