import argparse
import csv
from pathlib import Path


CSV_PATH = Path(__file__).with_name("notas_alunos.csv")
alunos: list[dict] = [{"matricula": "100001", "nota": 8.0}]


def converter_nota(valor: str) -> float | None:
    valor = valor.strip().replace(",", ".")
    if not valor or valor.lower() in {"falta", "faltou", "n/a", "-"}:
        return None
    try:
        return float(valor)
    except ValueError:
        return None


def carregar_alunos(caminho: Path = CSV_PATH) -> list[dict]:
    registros = []
    with caminho.open("r", encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")
        for numero, linha in enumerate(leitor, start=1):
            notas = [
                converter_nota(linha.get(coluna, ""))
                for coluna in ("Nota01", "TF01", "Nota02", "TF02")
            ]
            if any(nota is None for nota in notas):
                print(f"Linha {numero}: nota ausente/inválida; registro ignorado.")
                continue

            nota01, tf01, nota02, tf02 = notas
            nota_provas = (nota01 + nota02) / 2
            nota_trabalhos = ((tf01 + tf02) / 2) / 2 * 10
            nota_final = nota_provas * 0.8 + nota_trabalhos * 0.2
            matricula = linha.get("RA", "").strip() or f"SEM-RA-{numero}"
            registros.append(
                {"matricula": matricula, "nota": round(nota_final, 2)}
            )
    return registros


def imprimir_resumo(registros: list[dict]) -> None:
    for aluno in registros:
        situacao = "APROVADO" if aluno["nota"] >= 6 else "REPROVADO"
        print(
            f"Matrícula: {aluno['matricula']} | Nota final: {aluno['nota']:.2f} "
            f"| {situacao}"
        )


def lancar_notas(registros: list[dict]) -> None:
    import pyautogui

    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5
    print("Deixe o formulário acadêmico aberto, com o campo de matrícula em foco.")
    input("Pressione Enter para iniciar; mova o mouse ao canto superior esquerdo para abortar.")
    for aluno in registros:
        pyautogui.write(aluno["matricula"], interval=0.05)
        pyautogui.press("tab")
        pyautogui.write(f"{aluno['nota']:.2f}".replace(".", ","), interval=0.05)
        pyautogui.press("tab")
        pyautogui.press("enter")
        pyautogui.sleep(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Calcula e lança notas de alunos.")
    parser.add_argument(
        "--executar",
        action="store_true",
        help="Interage com o formulário aberto. Sem esta opção, apenas exibe o resumo.",
    )
    args = parser.parse_args()

    global alunos
    alunos = carregar_alunos()
    imprimir_resumo(alunos)
    if args.executar:
        lancar_notas(alunos)


if __name__ == "__main__":
    main()
