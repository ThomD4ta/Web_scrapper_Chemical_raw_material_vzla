from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

# ============================
# CONFIGURACIÓN SSL
# ============================
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# ============================
# URL OBJETIVO
# ============================
url = "https://py4e-data.dr-chuck.net/comments_2353324.html"

# ============================
# DESCARGA HTML
# ============================
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")

# ============================
# EXTRACCIÓN DE DATOS
# ============================
total_comments = 0
records = []

rows = soup.find_all("tr")

for row in rows:
    cols = row.find_all("td")

    if len(cols) != 2:
        continue

    name = cols[0].get_text(strip=True)
    comment_span = cols[1].find("span", class_="comments")

    if not comment_span:
        continue

    comments = int(comment_span.get_text(strip=True))

    records.append({
        "name": name,
        "comments": comments
    })

    total_comments += comments

# ============================
# RESULTADOS
# ============================
print("📋 Comentarios por persona:")
for r in records:
    print(f"- {r['name']}: {r['comments']}")

print("\n✅ Total de comentarios:", total_comments)
