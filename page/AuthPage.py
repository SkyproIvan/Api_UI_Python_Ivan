import os
from dotenv import load_dotenv
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
load_dotenv()
class AuthPage:

    def __init__(self, driver: WebDriver) -> None:
        self.url = None
        self.__url = "https://ru.yougile.com/team/settings-account"
        self.__driver = driver

    @allure.step("Перейти на страницу авторизации")
    def go(self):
        self.__driver.get(self.__url)

    @allure.step("Авторизоваться под {email}:{password}")
    def login_as(self, email: str, password: str):
        # Ожидаем появления поля ввода логина
        (WebDriverWait(self.__driver, 10).
         until(EC.visibility_of_element_located((By.
                                                 CSS_SELECTOR, "input[placeholder='example@mail.ru']")))).send_keys(email)

        # Ожидаем появления поля ввода пароля
        (WebDriverWait(self.__driver, 10).
         until(EC.visibility_of_element_located((By.
                                                 CSS_SELECTOR, "input[placeholder='Введите пароль']")))).send_keys(password)


        (self.__driver.find_element(By.CSS_SELECTOR, "div[role='button']").
         click())

        # Ожидаем появления логотипа
        # (убеждаемся что главная страница полностью загружена)
        (WebDriverWait(self.__driver, 10).
         until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                 '.user-avatar-photo'))))

    @allure.step("Получить текущий URL")
    def get_current_url(self):
        return self.__driver.current_url