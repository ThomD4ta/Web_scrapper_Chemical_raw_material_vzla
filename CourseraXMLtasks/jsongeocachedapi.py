import urllib.request
import urllib.parse
import json
import ssl

# ============================
# CONFIGURACIÓN
# ============================

SERVICE_URL = "http://py4e-data.dr-chuck.net/opengeo?"

# Ignorar errores de certificado SSL
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# ============================
# FUNCIONES
# ============================

def fetch_geo_data(address: str) -> dict:
    """Consulta el servicio OpenGeo y devuelve el JSON parseado."""
    params = {"q": address}
    url = SERVICE_URL + urllib.parse.urlencode(params)

    print("Retrieving", url)

    with urllib.request.urlopen(url, context=ctx) as response:
        data = response.read().decode()

    print("Retrieved", len(data), "characters")

    return json.loads(data)

def extract_plus_code(js: dict) -> str | None:
    """Extrae el primer plus_code del JSON."""
    try:
        return js["features"][0]["properties"]["plus_code"]
    except (KeyError, IndexError, TypeError):
        return None

# ============================
# MAIN
# ============================

def main():
    while True:
        address = input("Enter location: ").strip()
        if not address:
            break

        js = fetch_geo_data(address)

        if "features" not in js or len(js["features"]) == 0:
            print("==== Object not found ====")
            continue

        plus_code = extract_plus_code(js)

        if plus_code:
            print("Plus code", plus_code)
        else:
            print("Plus code not available")

if __name__ == "__main__":
    main()
