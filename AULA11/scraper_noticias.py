import argparse
import csv
from pathlib import Path

import requests
from bs4 import BeautifulSoup


URL_NOTICIAS = "https://news.ycombinator.com/"


def coletar_noticias(url: str = URL_NOTICIAS) -> list[dict[str, str]]:
    resposta = requests.get(
        url,
        headers={"User-Agent": "AulasRPA/1.0 (educational scraper)"},
        timeout=15,
    )
    if resposta.status_code != 200:
        raise requests.HTTPError(
            f"Resposta HTTP inesperada: {resposta.status_code}", response=resposta
        )
    sopa = BeautifulSoup(resposta.text, "html.parser")
    noticias = []
    for link in sopa.select("span.titleline > a"):
        noticias.append({"titulo": link.get_text(strip=True), "url": link.get("href", "")})
    return noticias


def salvar_csv(noticias: list[dict[str, str]], destino: Path) -> None:
    with destino.open("w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=["titulo", "url"])
        escritor.writeheader()
        escritor.writerows(noticias)
    print(f"{len(noticias)} notícia(s) salva(s) em {destino}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Coleta títulos do Hacker News.")
    parser.add_argument("--url", default=URL_NOTICIAS)
    parser.add_argument("--saida", type=Path, default=Path("noticias.csv"))
    args = parser.parse_args()
    salvar_csv(coletar_noticias(args.url), args.saida)


if __name__ == "__main__":
    main()
