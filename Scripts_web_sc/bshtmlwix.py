import os
import urllib.request
import ssl
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# ============================
# Cargar variables de entorno
# ============================
load_dotenv()

RAW_URLS = os.getenv("CIAMPAI_URLS", "")
URLS = [u.strip() for u in RAW_URLS.split(",") if u.strip()]

# ============================
# Configuración SSL (exploratoria)
# ============================
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE

# ============================
# Función principal de scraping
# ============================
def scrape_wix_text(url: str) -> list[dict]:
    """Extrae textos relevantes de sitios Wix."""
    try:
        response = urllib.request.urlopen(url, context=SSL_CONTEXT)
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")

        elements = soup.find_all(class_="wixui-rich-text__text")

        records = []
        for el in elements:
            text_chunks = [
                t.strip()
                for t in el.stripped_strings
                if len(t.strip()) > 2
            ]

            for text in text_chunks:
                records.append({
                    "source_url": url,
                    "raw_text": text
                })

        return records

    except Exception as e:
        print(f"[ERROR] No se pudo procesar {url}: {e}")
        return []

# ============================
# Función para build_dataset
# ============================
def records_w() -> list[dict]:
    """Devuelve todos los registros de todas las URLs."""
    all_records = []
    for url in URLS:
        all_records.extend(scrape_wix_text(url))
    return all_records

# ============================
# Ejecución manual (debug)
# ============================
if __name__ == "__main__":
    for url in URLS:
        print(f"\n===== Contenido extraído de: {url} =====")
        records = scrape_wix_text(url)

        if not records:
            print("No se encontró contenido relevante.")
        else:
            for r in records:
                print("-", r)