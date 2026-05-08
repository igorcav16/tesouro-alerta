import requests
import json

URL = "https://www.tesourodireto.com.br/json/treasurybondsinfo.json"

response = requests.get(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=60
)

dados = response.json()

taxa = None

for titulo in dados["response"]["TrsrBdTradgList"]:

    nome = titulo["TrsrBd"]["nm"]

    # procura Renda+ 2065
    if "Renda+" in nome and "2065" in nome:

        taxa = titulo["TrsrBd"]["anulInvstmtRate"]

        break

print("Taxa encontrada:", taxa)

with open("taxa.json", "w") as f:

    json.dump(
        {
            "taxa": taxa
        },
        f
    )
