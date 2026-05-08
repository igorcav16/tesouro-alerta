import requests
from bs4 import BeautifulSoup
import json
import re

url = "https://www.tesourodireto.com.br/titulos/precos-e-taxas.htm"

headers = {
    "User-Agent": "Mozilla/5.0"
}

html = requests.get(url, headers=headers).text

# procura taxa do Renda+ 2065
padrao = r'Renda\+\sAposentadoria\sExtra\s2065.*?IPCA \+ ([0-9,]+)%'

resultado = re.search(padrao, html, re.S)

taxa = None

if resultado:
    taxa = float(
        resultado.group(1).replace(",", ".")
    )

dados = {
    "taxa": taxa
}

with open("taxa.json", "w") as f:
    json.dump(dados, f)
