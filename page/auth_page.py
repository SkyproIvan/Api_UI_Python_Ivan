from dotenv import load_dotenv
import allure
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Configuration.config_provider import ConfigProvider

load_dotenv()


class AuthPage:
    """Страница авторизации"""

    def __init__(self, driver: WebDriver) -> None:
        config_provider = ConfigProvider()
        url = config_provider.get_ui_url()
        self.url = None
        self.__url = url + "/team/settings-account"
        self.__driver = driver
        self.wait = WebDriverWait(self.__driver, 10)

    @allure.step("Перейти на страницу авторизации")
    def go(self):
        self.__driver.get(self.__url)

    @allure.step("Ввести {email}:{password}")
    def login_as(self, email: str, password: str, check: str = "Ok"):
        # Ожидаем появления поля ввода логина
        self.wait.until(
            (
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "input[placeholder='example@mail.ru']")
                )
            )
        ).send_keys(email)

        # Ожидаем появления поля ввода пароля
        self.wait.until(
            (
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "input[placeholder='Введите пароль']")
                )
            )
        ).send_keys(password)

        self.__driver.find_element(By.CSS_SELECTOR, "div[role='button']").click()

        if check == "Ok":
            # Ожидаем появления логотипа
            # (убеждаемся что главная страница полностью загружена)
            self.wait.until(
                (
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, ".user-avatar-photo")
                    )
                )
            )

    @allure.step("Выполнить вход с логином и паролем")
    def make_auth(self):
        email = os.getenv("TEST_USER_EMAIL")
        password = os.getenv("TEST_USER_PASSWORD")
        assert (
            email is not None and password is not None
        ), "Данные для входа (email/password) не найдены в переменных окружения"

        with allure.step("Открыть страницу аутентификации"):
            self.go()
        with allure.step("Ввести логин и пароль и выполнить вход"):
            self.login_as(email, password)

    @allure.step("Попытка входа без пароля")
    def is_error(self):
        return self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="login-error"]'))
        )
