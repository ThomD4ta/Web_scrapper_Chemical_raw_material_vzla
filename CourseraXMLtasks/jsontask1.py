import urllib.request
import json

def fetch_json(url: str) -> bytes:
    """Descarga datos JSON desde una URL."""
    with urllib.request.urlopen(url) as response:
        return response.read()

def parse_json(json_bytes: bytes) -> dict:
    """Convierte bytes JSON en un diccionario Python."""
    return json.loads(json_bytes)

def sum_comment_counts(data: dict) -> tuple[int, int]:
    """
    Extrae los conteos de comentarios y calcula:
    - número de comentarios
    - suma total
    """
    comments = data.get("comments", [])
    total_sum = sum(item["count"] for item in comments)
    return len(comments), total_sum

def main():
    url = input("Enter url location: ").strip()
    if not url:
        url = "https://py4e-data.dr-chuck.net/comments_2353327.json"

    print("Retrieving", url)

    json_bytes = fetch_json(url)
    print("Retrieved", len(json_bytes), "characters")

    data = parse_json(json_bytes)
    count, total = sum_comment_counts(data)

    print("Count:", count)
    print("Sum:", total)

if __name__ == "__main__":
    main()
