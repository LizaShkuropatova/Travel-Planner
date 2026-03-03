import requests

ART_BASE_URL = "https://api.artic.edu/api/v1/artworks"

def artworks(external_id: str) -> bool:
    resp = requests.get(f"{ART_BASE_URL}/{external_id}", timeout=10)
    return resp.status_code == 200