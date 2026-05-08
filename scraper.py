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

    page.goto(
        URL,
        wait_until="domcontentloaded",
        timeout=60000
    )

    # espera javascript carregar
    page.wait_for_timeout(15000)

    texto = page.locator("body").inner_text()

    browser.close()

    linhas = texto.split("\n")

    encontrou_titulo = False

    for linha in linhas:

        linha = linha.strip()

        # procura o título EXATO
        if "Tesouro Renda+ Aposentadoria Extra 2065" in linha:

            print("Título encontrado")

            encontrou_titulo = True

            continue

        # após encontrar o título
        # procura a taxa IPCA+
        if encontrou_titulo:

            match = re.search(
                r'IPCA\s*\+\s*([0-9,]+)',
                linha
            )

            if match:

                taxa = float(
                    match.group(1)
                    .replace(",", ".")
                )

                print("Taxa encontrada:", taxa)

                break

dados = {
    "taxa": taxa
}

with open("taxa.json", "w") as f:
    json.dump(dados, f)
