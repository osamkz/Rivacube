import requests
import json
import time


def request_data(url: str = "http://127.0.0.1:8000/ticker/?format=json", results: list[dict] = None) -> list[dict]:
    # Initialise la valeurs de results à [] si elle n'existe pas
    results = results if results else []

    # Recupere les données depuis l'api
    data = json.loads(requests.get(url).text)
    results += data["results"]
    has_next = data["next"]

    if (has_next):
        request_data(has_next, results)
    return results


s = time.time()
data = request_data()
e = time.time()

print("{}s pour récupérer {} lignes avec 1,000,000 lignes par requete".format(
    e - s, len(data)))
