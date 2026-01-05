import time
import random
import os
import cloudscraper
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# ============================
# CARGA DE VARIABLES DE ENTORNO
# ============================

load_dotenv()

BASE_DOMAIN = os.getenv("PRIMAZOL_BASE_DOMAIN")
CATEGORY_URLS = os.getenv("PRIMAZOL_CATEGORY_URLS", "").split(",")

if not BASE_DOMAIN or not CATEGORY_URLS:
    raise RuntimeError("❌ Variables PRIMAZOL_* no cargadas desde .env")

# ============================
# USER AGENTS ROTATIVOS
# ============================

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0 Safari/537.36",
]

# ============================
# SCRAPER FACTORY
# ============================

def create_scraper() -> cloudscraper.CloudScraper:
    scraper = cloudscraper.create_scraper(
        browser={
            "browser": "chrome",
            "platform": "windows",
            "mobile": False
        }
    )

    scraper.headers.update({
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": BASE_DOMAIN,
        "Upgrade-Insecure-Requests": "1",
    })

    return scraper

# ============================
# SCRAPER POR CATEGORÍA
# ============================

def scrape_category(url: str) -> list[dict]:
    print(f"\n🔍 Scraping categoría")

    scraper = create_scraper()

    try:
        response = scraper.get(url, timeout=25)
        response.raise_for_status()
    except Exception as e:
        print(f"[ERROR] Acceso fallido: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    buttons = soup.select("a.elementor-button")

    records = []

    for btn in buttons:
        href = btn.get("href")
        text = btn.select_one("span.elementor-button-text")

        if not href or not text:
            continue

        records.append({
            "source_url": href.strip(),
            "raw_text": text.get_text(strip=True),
            "category_url": url
        })

    print(f"✅ Productos encontrados: {len(records)}")
    time.sleep(random.uniform(1.8, 3.5))

    return records

# ============================
# ORQUESTADOR
# ============================

def results_ch() -> list[dict]:
    all_records = []

    for url in CATEGORY_URLS:
        all_records.extend(scrape_category(url))
        time.sleep(random.uniform(3.0, 6.0))

    return all_records

# ============================
# DEBUG
# ============================

if __name__ == "__main__":
    data = results_ch()
    print("\n📦 RESUMEN FINAL")
    print(f"Total productos extraídos: {len(data)}")
