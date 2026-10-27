import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json


def scrape_books():
    url = "https://books.toscrape.com/catalogue/page-1.html"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; PythonScraper/1.0)"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "lxml")
    
    books = soup.select("article.product_pod")
    
    books_list =[]
    for book in books:
        title = book.select_one("h3 a")
        price = book.select_one("p.price_color")

        link = title.get("href", "")   
        full_url = urljoin(url, link)
        price_text = price.get_text(strip=True) if price else ""
        clean_price = "".join(c for c in price_text if c.isdigit() or c == '.')



        
        if title:
            books_list.append({
                "title": title.get("title") or title.get_text(strip=True),
                "price": float(clean_price) if clean_price else None,
                "link": full_url,
            })

    form = {"books": books_list}
    with open("books.json", "w", encoding="utf-8") as f:
        json.dump(form, f, ensure_ascii=False, indent=4)

    return books_list

books = scrape_books()
print(f"Успешно сохранено книг: {len(books)}")
