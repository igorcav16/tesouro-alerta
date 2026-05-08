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

print(html[:2000])

taxa = None

padrao = r'Tesouro Renda\+ Aposentadoria Extra 2065.*?IPCA \+ ([0-9,]+)%'

resultado = re.search(
    padrao,
    html,
    re.S
)

if resultado:

    taxa = float(
        resultado.group(1)
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
