import logging
import queue
import threading
from logging.handlers import RotatingFileHandler

from tenacity import retry, stop_after_attempt, wait_exponential


FATURAS = [
    {"numero": "FAT-001", "valor": 1250.00},
    {"numero": "FAT-002", "valor": 840.50},
    {"numero": "FAT-003", "valor": 2100.75},
]


def configurar_logging() -> None:
    handler = RotatingFileHandler(
        "app_rpa.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[handler, logging.StreamHandler()],
    )


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.1, min=0.1, max=1),
    reraise=True,
)
def processar_fatura(fatura: dict) -> str:
    """Valida e processa uma fatura, com política de retry para falhas."""
    numero = fatura.get("numero")
    valor = fatura.get("valor")
    if not numero or not isinstance(valor, (int, float)) or valor <= 0:
        raise ValueError("Fatura sem número ou com valor inválido.")
    logging.info("Fatura %s processada: R$ %.2f", numero, valor)
    return str(numero)


def produzir_faturas(fila: queue.Queue, faturas: list[dict]) -> None:
    for fatura in faturas:
        fila.put(fatura)
    fila.put(None)


def consumir_faturas(fila: queue.Queue) -> None:
    while True:
        fatura = fila.get()
        try:
            if fatura is None:
                break
            try:
                processar_fatura(fatura)
            except ValueError:
                logging.exception("Fatura inválida descartada: %s", fatura)
        finally:
            fila.task_done()


def executar_fila(faturas: list[dict]) -> None:
    fila: queue.Queue = queue.Queue()
    consumidor = threading.Thread(target=consumir_faturas, args=(fila,))
    consumidor.start()
    produzir_faturas(fila, faturas)
    fila.join()
    consumidor.join()


def main() -> None:
    configurar_logging()
    logging.info("Iniciando processamento da fila de faturamento.")
    executar_fila(FATURAS)
    logging.info("Processamento da fila concluído.")


if __name__ == "__main__":
    main()
