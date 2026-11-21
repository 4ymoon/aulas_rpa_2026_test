import platform
import time


def executar_automacao() -> None:
    import pyautogui

    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5

    if platform.system() == "Windows":
        pyautogui.press("win")
        pyautogui.write("notepad", interval=0.1)
    else:
        pyautogui.press("win")
        pyautogui.write("gedit", interval=0.1)
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.write(
        "Relatório de Execução Automática - RPA PyAutoGUI Ativo!",
        interval=0.05,
    )
    pyautogui.hotkey("ctrl", "s")
    pyautogui.write("status_bot.txt", interval=0.05)
    pyautogui.press("enter")


if __name__ == "__main__":
    executar_automacao()
