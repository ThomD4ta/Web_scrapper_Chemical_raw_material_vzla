import urllib.request
import xml.etree.ElementTree as ET


def fetch_xml(url: str) -> bytes:
    """Descarga datos desde la URL"""
    with urllib.request.urlopen(url) as response:
        return response.read()


def parse_xml(xml_bytes: bytes) -> ET.Element:
    """Intenta parsear XML, lanza error controlado si no es XML"""
    try:
        return ET.fromstring(xml_bytes)
    except ET.ParseError:
        raise ValueError(
            "El contenido descargado NO es XML válido. "
            "Verifica que la URL apunte a un recurso XML."
        )


def transform_data(tree: ET.Element) -> int:
    """Extrae y suma los valores <count>"""
    counts = tree.findall('.//count')
    return sum(int(c.text) for c in counts if c.text and c.text.isdigit())


def main():
    url = input("Enter URL: ").strip()

    try:
        xml_bytes = fetch_xml(url)
        tree = parse_xml(xml_bytes)
        total = transform_data(tree)
        print("Sum:", total)

    except ValueError as e:
        print("[DATA ERROR]", e)

    except Exception as e:
        print("[UNEXPECTED ERROR]", e)


if __name__ == "__main__":
    main()
