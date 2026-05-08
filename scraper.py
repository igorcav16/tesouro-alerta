import requests
import json

URL = "https://www.tesourodireto.com.br/json-data/resgate"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

response = requests.get(
    URL,
    headers=headers,
    timeout=60
)

print("Status:", response.status_code)
print(response.text[:500])

dados = response.json()

taxa = None

# percorre títulos
for titulo in dados.get("response", {}).get("TrsrBdTradgList", []):

    nome = titulo.get("TrsrBd", {}).get("nm", "")

    if (
        "Renda+" in nome and
        "2065" in nome
    ):

        taxa = titulo["TrsrBd"].get(
            "anulInvstmtRate"
        )

        break

print("Taxa encontrada:", taxa)

with open("taxa.json", "w") as f:

    json.dump(
        {
            "taxa": taxa
        },
        f
    )
