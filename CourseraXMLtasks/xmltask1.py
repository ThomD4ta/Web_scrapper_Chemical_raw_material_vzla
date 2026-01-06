import urllib.request
import xml.etree.ElementTree as ET

url = input('Enter URL location to retrieve data: ')
if len(url) < 1:
    url = 'http://py4e-data.dr-chuck.net/comments_2353326.xml'

print('Retrieving', url)

# 1. Abrir la URL
uh = urllib.request.urlopen(url)
data = uh.read()

print('Retrieved', len(data), 'characters')

# 2. Parsear XML
tree = ET.fromstring(data)

# 3. Buscar todos los <count> XPATH Flexible
counts = tree.findall('.//count')

nums = []

for count in counts:
    value = int(count.text)
    nums.append(value)

# 4. Resultados
print('Count:', len(nums))
print('Sum:', sum(nums))
