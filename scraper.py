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

    page.wait_for_timeout(15000)

    texto = page.locator("body").inner_text()

    browser.close()

    print("=== TEXTO DA PÁGINA ===")
    print(texto[:5000])

    linhas = texto.split("\n")

    for linha in linhas:

        linha = linha.strip()

        print(linha)

        # procura taxa diretamente
        if (
            "Tesouro Renda+ Aposentadoria Extra 2065"
            in linha
        ):

            print("TÍTULO ENCONTRADO")

            match = re.search(
                r'IPCA\s*\+\s*([0-9,]+)',
                linha
            )

            if match:

                taxa = float(
                    match.group(1)
                    .replace(",", ".")
                )

                print("TAXA:", taxa)

                break

# salva mesmo se null
dados = {
    "taxa": taxa
}

with open("taxa.json", "w") as f:
    json.dump(dados, f)

print("JSON SALVO")
