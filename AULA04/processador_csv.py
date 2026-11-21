import logging


def configurar_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("execucao_bot.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def processar_arquivo(caminho: str) -> None:
    """Lê e registra as linhas de um arquivo, sem ocultar erros inesperados."""
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            for numero, linha in enumerate(arquivo, start=1):
                logging.info("Linha %d: %s", numero, linha.rstrip())
    except FileNotFoundError:
        logging.error("Arquivo não encontrado: %s", caminho)
    finally:
        logging.info("Tentativa de processamento finalizada: %s", caminho)


if __name__ == "__main__":
    configurar_logging()
    processar_arquivo("dados.csv")
