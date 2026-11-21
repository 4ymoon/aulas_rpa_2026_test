import argparse
import re
from pathlib import Path

import pandas as pd
import pdfplumber


PADROES = {
    "cpf": r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "valor": r"(?:R\$\s*)\d{1,3}(?:\.\d{3})*(?:,\d{2})",
}


def extrair_dados(caminho_pdf: Path) -> dict:
    partes = []
    with pdfplumber.open(caminho_pdf) as documento:
        for pagina in documento.pages:
            partes.append(pagina.extract_text() or "")
    texto = "\n".join(partes)
    dados = {"arquivo": caminho_pdf.name}
    for campo, padrao in PADROES.items():
        correspondencia = re.search(padrao, texto, flags=re.IGNORECASE)
        dados[campo] = correspondencia.group(0) if correspondencia else ""
    return dados


def exportar_faturas(arquivos_pdf: list[Path], destino: Path) -> None:
    dados = [extrair_dados(caminho) for caminho in arquivos_pdf]
    pd.DataFrame(dados).to_excel(destino, index=False)
    print(f"{len(dados)} fatura(s) exportada(s) para {destino}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extrai campos de faturas em PDF.")
    parser.add_argument("pdf", nargs="+", type=Path, help="Arquivo(s) PDF de entrada.")
    parser.add_argument("--saida", type=Path, default=Path("faturas_extraidas.xlsx"))
    args = parser.parse_args()

    ausentes = [caminho for caminho in args.pdf if not caminho.is_file()]
    if ausentes:
        parser.error("PDF(s) não encontrado(s): " + ", ".join(map(str, ausentes)))
    exportar_faturas(args.pdf, args.saida)


if __name__ == "__main__":
    main()
