from playwright.sync_api import sync_playwright
import json

URL = "https://www.tesourodireto.com.br/titulos/precos-e-taxas.htm"

taxa = None

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page()

    page.goto(
        URL,
        wait_until="networkidle",
        timeout=120000
    )

    page.wait_for_timeout(15000)

    texto = page.inner_text("body")

    browser.close()

    linhas = texto.split("\n")

    for i, linha in enumerate(linhas):

        if (
            "Renda+" in linha and
            "2065" in linha
        ):

            for j in range(i, min(i + 10, len(linhas))):

                trecho = linhas[j]

                if "IPCA +" in trecho:

                    taxa_texto = (
                        trecho
                        .split("IPCA +")[1]
                        .replace("%", "")
                        .strip()
                        .replace(",", ".")
                    )

                    try:
                        taxa = float(taxa_texto)
                        break
                    except:
                        pass

dados = {
    "taxa": taxa
}

with open("taxa.json", "w") as f:
    json.dump(dados, f)
