import requests
import json

URL = "https://www.tesourodireto.com.br/json/treasurybondsinfo.json"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=60)

if response.status_code != 200:
    print("Erro HTTP:", response.status_code)
    exit()

data = response.json()

taxa = None

for item in data.get("response", {}).get("TrsrBdTradgList", []):

    nome = item.get("TrsrBd", {}).get("nm", "")

    vencimento = item.get("TrsrBd", {}).get("mtrtyDtTrgt", "")

    # identifica Renda+ 2065 corretamente
    if "Renda+" in nome and "2065" in nome:

        taxa = item["TrsrBd"].get("anulInvstmtRate")

        break

print("Taxa encontrada:", taxa)

with open("taxa.json", "w") as f:
    json.dump({"taxa": taxa}, f)
