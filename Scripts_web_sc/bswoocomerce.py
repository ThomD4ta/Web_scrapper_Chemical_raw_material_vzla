import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# ============================
# Cargar variables de entorno
# ============================
load_dotenv()

BASE_URL = os.getenv("LAGALERIA_BASE_URL")

if not BASE_URL:
    raise ValueError("LAGALERIA_BASE_URL no está definido en el archivo .env")

# ============================
# Headers HTTP
# ============================
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9",
}

# ============================
# Scraper de una página
# ============================
def fetch_products(page_url: str) -> list[dict]:
    """Extrae productos desde una página específica de WooCommerce."""
    try:
        response = requests.get(page_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"[ERROR] No se pudo acceder a {page_url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.select("li.product")

    records = []

    for product in products:
        link = product.select_one("a.woocommerce-LoopProduct-link")
        title = product.select_one("h2.woocommerce-loop-product__title")

        if not link or not title:
            continue

        records.append({
            "source_url": link.get("href"),
            "raw_text": title.get_text(strip=True)
        })

    return records

# ============================
# Función para build_dataset
# ============================
def results_w() -> list[dict]:
    """Extrae todos los productos paginados y devuelve una lista de registros."""
    all_records = []
    page = 1

    while True:
        page_url = BASE_URL if page == 1 else f"{BASE_URL}page/{page}/"
        print(f"[INFO] Scraping: {page_url}")

        records = fetch_products(page_url)

        if not records:
            print("[INFO] No hay más productos. Fin de la paginación.")
            break

        all_records.extend(records)
        page += 1

    return all_records

# ============================
# Ejecución manual (debug)
# ============================
if __name__ == "__main__":
    data = results_w()
    print(f"\nTotal productos extraídos: {len(data)}")
    for item in data:
        print(item)
