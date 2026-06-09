import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:

    def __init__(self, driver: WebDriver) -> None:
        self.__driver = driver

    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        return self.__driver.current_url

    @allure.step("Мои задачи")
    def open_menu(self):
        self.__driver.find_element(By.CSS_SELECTOR,
                                   "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(7) > div:nth-child(2)").click()

    @allure.step("Прочитать информацию о моих задачах")
    def get_account_info(self) -> str:
        # Ожидаем полной загрузки меню
        (WebDriverWait(self.__driver, 10).
         until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                 "div[class='relative text-primary truncate isolate flex-1 min-w-0 break-words text-sm-regular ml-4'] span span"))))
        container = self.__driver.find_element(By.CSS_SELECTOR,
                                               "div[class='relative text-primary truncate isolate flex-1 min-w-0 break-words text-sm-regular ml-4'] span span")
        name = container.text
        #email = fields[1].text
        # Возвращаем имя и почту пользователя:
        return name