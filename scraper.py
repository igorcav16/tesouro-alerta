from playwright.sync_api import sync_playwright
import json
import re

URL = "https://www.tesourodireto.com.br/titulos/precos-e-taxas.htm"

taxa = None

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page()

    # abre sem esperar tudo carregar
    page.goto(
        URL,
        wait_until="domcontentloaded",
        timeout=60000
    )

    # espera renderizar javascript
    page.wait_for_timeout(10000)

    html = page.content()

    browser.close()

    # procura taxa do Renda+ 2065
    padrao = r'Renda\+\sAposentadoria\sExtra\s2065.*?IPCA\s*\+\s*([0-9,]+)%'

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

dados = {
    "taxa": taxa
}

with open("taxa.json", "w") as f:
    json.dump(dados, f)
