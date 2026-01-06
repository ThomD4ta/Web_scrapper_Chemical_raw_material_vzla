import urllib.request
from bs4 import BeautifulSoup
import ssl
from urllib.parse import urljoin

# ============================
# CONFIGURACIÓN SSL
# ============================
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# ============================
# CONFIGURACIÓN DEL PROBLEMA
# ============================
START_URL = "http://py4e-data.dr-chuck.net/known_by_Kelvin.html"
POSITION = 18
REPEAT = 7

current_url = START_URL

print("🔗 Proceso de navegación:\n")

# ============================
# LOOP PRINCIPAL
# ============================
for i in range(REPEAT):
    print(f"Paso {i + 1}")
    print("URL actual:", current_url)

    html = urllib.request.urlopen(current_url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    tags = soup.find_all("a")
    print("Total de enlaces encontrados:", len(tags))

    selected_tag = tags[POSITION - 1]
    name = selected_tag.get_text(strip=True)
    href = selected_tag.get("href")

    # 🔑 FIX CRÍTICO AQUÍ
    next_url = urljoin(current_url, href)

    print("Nombre encontrado:", name)
    print("Siguiente URL:", next_url)
    print("-" * 45)

    current_url = next_url

# ============================
# RESULTADO FINAL
# ============================
print("\n✅ RESPUESTA FINAL:", name)
