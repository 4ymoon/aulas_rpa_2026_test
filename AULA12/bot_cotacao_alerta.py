import os
import smtplib
from email.mime.text import MIMEText

import requests


URL_COTACAO = "https://economia.awesomeapi.com.br/json/last/USD-BRL"


def obter_cotacao() -> float:
    resposta = requests.get(URL_COTACAO, timeout=15)
    resposta.raise_for_status()
    dados = resposta.json()
    return float(dados["USDBRL"]["bid"])


def criar_email(cotacao: float) -> MIMEText:
    mensagem = MIMEText(
        f"A cotação atual do dólar é R$ {cotacao:.4f}.",
        "plain",
        "utf-8",
    )
    mensagem["Subject"] = "Alerta de cotação USD/BRL"
    mensagem["From"] = os.environ.get("SMTP_FROM", "")
    mensagem["To"] = os.environ.get("SMTP_TO", "")
    return mensagem


def enviar_alerta(cotacao: float) -> None:
    mensagem = criar_email(cotacao)
    if os.environ.get("MOCK_EMAIL", "").lower() == "true":
        print(f"[MOCK] E-mail de alerta preparado: {mensagem.get_payload(decode=True).decode('utf-8')}")
        return

    obrigatorias = ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD", "SMTP_FROM", "SMTP_TO")
    ausentes = [nome for nome in obrigatorias if not os.environ.get(nome)]
    if ausentes:
        raise ValueError("Configure as variáveis SMTP: " + ", ".join(ausentes))

    with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ["SMTP_PORT"]), timeout=15) as servidor:
        servidor.starttls()
        servidor.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
        servidor.send_message(mensagem)
    print("Alerta enviado por e-mail.")


def main() -> None:
    cotacao = obter_cotacao()
    print(f"Cotação USD/BRL: R$ {cotacao:.4f}")
    limite = float(os.environ.get("ALERTA_COTACAO", "5.0"))
    if cotacao >= limite:
        enviar_alerta(cotacao)
    else:
        print(f"Cotação abaixo do limite de alerta (R$ {limite:.2f}).")


if __name__ == "__main__":
    main()
