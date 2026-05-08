import requests
import json
import re

API_KEY = "ed50d0e18fd6889bbaec93d575bb015b30756ab8"

TARGET_URL = "https://www.tesourodireto.com.br/titulos/precos-e-taxas.htm"

url = (
    "https://api.zenrows.com/v1/?"
    f"apikey={API_KEY}"
    f"&url={TARGET_URL}"
    "&js_render=true"
)

response = requests.get(url, timeout=120)

html = response.text

print("HTML recebido")
print(html[:3000])

taxa = None

# procura qualquer ocorrência do título
padrao_titulo = r'Tesouro Renda\+ Aposentadoria Extra 2065'

titulo = re.search(
    padrao_titulo,
    html,
    re.S
)

if titulo:

    print("Título encontrado")

    # pega trecho próximo do título
    inicio = titulo.start()

    trecho = html[inicio:inicio + 5000]

    print("TRECHO:")
    print(trecho)

    # procura IPCA +
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
