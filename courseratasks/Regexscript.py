import urllib.request
import re
import ssl

# ----------------------------
# Configuración SSL
# ----------------------------
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# ----------------------------
# URL del archivo
# ----------------------------
url = "http://py4e-data.dr-chuck.net/regex_sum_2353322.txt"

# ----------------------------
# Lectura del archivo
# ----------------------------
with urllib.request.urlopen(url, context=ctx) as response:
    text = response.read().decode()

# ----------------------------
# Extracción con Regex
# ----------------------------
numbers = re.findall(r'\d+', text)

# Convertir a enteros y sumar
total_sum = sum(int(n) for n in numbers)

# ----------------------------
# Resultado
# ----------------------------
print("Cantidad de números encontrados:", len(numbers))
print("Suma total:", total_sum)
