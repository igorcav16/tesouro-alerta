import requests
import json
import re

API_KEY = "SUA_API_KEY"

TARGET_URL = "https://www.tesourodireto.com.br/titulos/precos-e-taxas.htm"

url = (
    "https://api.zenrows.com/v1/?"
    f"apikey={API_KEY}"
    f"&url={TARGET_URL}"
    "&js_render=true"
    "&wait=15000"
    "&premium_proxy=true"
)

response = requests.get(url, timeout=120)

html = response.text

print("HTML carregado")

# procura trecho do Renda+
match_titulo = re.search(
    r'Tesouro Renda\+ Aposentadoria Extra 2065',
    html,
    re.S
)

taxa = None

if match_titulo:

    print("Título encontrado")

    inicio = match_titulo.start()

    trecho = html[inicio:inicio + 10000]

    print(trecho)

    taxa_match = re.search(
        r'IPCA\s*\+\s*([0-9,]+)',
        trecho,
        re.S
    )

    if taxa_match:

        taxa = float(
            taxa_match.group(1)
            .replace(",", ".")
        )

print("Taxa encontrada:", taxa)

with open("taxa.json", "w") as f:

    json.dump(
        {
            "taxa": taxa
        },
        f
    )
