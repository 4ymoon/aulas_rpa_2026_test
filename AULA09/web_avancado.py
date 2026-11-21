from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


BASE_URL = "https://the-internet.herokuapp.com"


def executar_exemplos() -> None:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    try:
        driver.get(f"{BASE_URL}/dropdown")
        Select(driver.find_element(By.ID, "dropdown")).select_by_value("1")

        driver.get(f"{BASE_URL}/javascript_alerts")
        driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']").click()
        alerta = driver.switch_to.alert
        print(f"Alerta: {alerta.text}")
        alerta.accept()

        driver.get(f"{BASE_URL}/iframe")
        driver.switch_to.frame(driver.find_element(By.ID, "mce_0_ifr"))
        texto = driver.find_element(By.ID, "tinymce").text
        print(f"Texto no iframe: {texto}")
        driver.switch_to.default_content()
    finally:
        driver.quit()


if __name__ == "__main__":
    executar_exemplos()
