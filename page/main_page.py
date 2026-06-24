import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    TASK_ROW = (By.CSS_SELECTOR, "div.hoverable-group")
    CREATE_TASK_BUTTON = (
        By.XPATH,
        "//span[contains(text(), 'Создать задачу')]",
    )
    TASK_TITLE_INPUT = (
        By.CSS_SELECTOR,
        "textarea[placeholder='Введите название задачи']",
    )
    TASK_LOCATOR = (By.CSS_SELECTOR, "div.hoverable-group")

    def __init__(self, driver: WebDriver) -> None:
        self.driver = None
        self.__driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Получение списка существующих задач")
    def _get_task_rows(self) -> list:
        rows = self.__driver.find_elements(*self.TASK_ROW)
        return [row for row in rows if "Создать задачу" not in row.text]

    @allure.step("Ожидание появления задачи в списке")
    def _wait_task_in_list(self, task_name: str):
        task_name_locator = (
            By.XPATH,
            (
                "//div[contains(@class,'hoverable-group')]"
                f"//span[contains(text(), '{task_name}')]"
            ),
        )
        return self.wait.until(
            EC.visibility_of_element_located(task_name_locator)
        )

    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        return self.__driver.current_url

    @allure.step("Мой аккаунт")
    def open_menu(self):
        self.__driver.find_element(
            By.CSS_SELECTOR, ".truncate.ml-6.text-14.leading-4"
        ).click()
        with allure.step("Проверить текущий URL страницы"):
            current_url = self.get_current_url()
            assert (
                "settings-account" in current_url
            ), f"URL '{current_url}' не содержит 'my-tasks'"

    @allure.step("Мои задачи")
    def open_task_menu(self):
        self.__driver.find_element(
            By.XPATH,
            "//div[@class='select-none text-14 leading-4 text-panel-text-primary whitespace-nowrap'][contains(text(),'Мои задачи')]",
        ).click()

        with allure.step("Проверить текущий URL страницы"):
            current_url = self.get_current_url()
            assert (
                "my-tasks" in current_url
            ), f"URL '{current_url}' не содержит 'my-tasks'"

    @allure.step("Прочитать информацию о моих задачах")
    def get_account_info(self) -> str:
        """Ожидает появления контейнера с информацией о пользователе и возвращает его имя."""
        input_field_locator = (
            By.CSS_SELECTOR,
            "input[placeholder='Отображаемое имя…']",
        )

        element = self.wait.until(EC.visibility_of_element_located(input_field_locator))

        return element.get_attribute("value")

    @allure.step("Получение списка задач")
    def get_task_count(self):
        """Возвращает текущее количество задач в списке."""
        return len(self.__driver.find_elements(*self.TASK_LOCATOR))

    @allure.step("Проверить, что количество задач уменьшилось")
    def wait_for_task_count_change(self, initial_count, timeout=15):
        """
        Ждёт, пока количество задач изменится.
        Возвращает финальное количество задач.
        """
        wait = WebDriverWait(self.__driver, timeout)
        wait.until(
            lambda driver: len(
                driver.find_elements(*self.TASK_LOCATOR)
            ) != initial_count
        )
        return self.get_task_count()

    @allure.step("Удаление созданных задач")
    def delete_new_task(self):
        """Удаляет созданную задачу."""

        try:
            tasks_list = self.__driver.find_elements(
                By.CSS_SELECTOR, "div.hoverable-group"
            )

            if not tasks_list:
                raise Exception("Список задач пуст. Не удалось найти ни одной задачи.")

            first_task_element = tasks_list[0]

            actions = ActionChains(self.__driver)
            actions.move_to_element(first_task_element).perform()

            button_of_task_locator = (
                By.CSS_SELECTOR,
                "[data-testid='board-task-menu']",
            )
            self.wait.until(EC.visibility_of_element_located(button_of_task_locator))
            button_of_task_element = first_task_element.find_element(
                *button_of_task_locator
            )

            print("Кнопка меню успешно найдена! Продолжаем тест...")
            button_of_task_element.click()

            button_delete_locator = (By.XPATH, ".//div[contains(text(),'Удалить')]")
            button_delete = self.wait.until(
                EC.visibility_of_element_located(button_delete_locator)
            )
            button_delete.click()

            confirm_button_locator = (
                By.XPATH,
                '//div[@role="button"][normalize-space()="Удалить"]',
            )
            confirm_button = self.wait.until(
                EC.element_to_be_clickable(confirm_button_locator)
            )
            confirm_button.click()

            self.wait.until(EC.invisibility_of_element(first_task_element))

            container_number = self.__driver.find_element(
                By.CSS_SELECTOR,
                ".bg-background-secondary.rounded-4.px-6.py-2.text-subtitle-xs.text-secondary",
            )
            number_task = container_number.text
            return number_task

        except Exception as e:
            self.__driver.save_screenshot("final_fix_error.png")
            raise e

    @allure.step("Переходим на страницу, где есть кнопка выйти")
    def open_exit(self):
        button_locator = (By.CSS_SELECTOR, ".truncate.ml-6.text-14.leading-4")
        self.wait.until(EC.element_to_be_clickable(button_locator)).click()

    @allure.step("Выйти из учетной записи")
    def logout(self):
        """
        Выполняет выход из учетной записи пользователя.
        """
        self.open_exit()

        logout_button_locator = (By.CSS_SELECTOR, "div[class='cursor-pointer']")

        self.wait.until(EC.element_to_be_clickable(logout_button_locator)).click()

        container_exit = self.__driver.find_element(
            By.CSS_SELECTOR, "input[placeholder='example@mail.ru']"
        )
        name_exit = container_exit.text
        return name_exit

    @allure.step("Мои задачи")
    def open_menu_for_create(self):
        self.__driver.find_element(
            By.XPATH,
            "//div[@class='select-none text-14 leading-4 text-panel-text-primary whitespace-nowrap'][contains(text(),'Мои задачи')]",
        ).click()
        self.wait.until(lambda driver: "my-tasks" in driver.current_url)

    @allure.step("Создать задачу '{task_name}'")
    def create_new_task(self, task_name: str) -> str:
        """
        Создаёт задачу в разделе «Мои задачи» и проверяет её появление в списке.
        """
        self.wait.until(
            EC.element_to_be_clickable(self.CREATE_TASK_BUTTON)
        ).click()

        title_input = self.wait.until(
            EC.visibility_of_element_located(self.TASK_TITLE_INPUT)
        )
        title_input.clear()
        title_input.send_keys(task_name)
        title_input.send_keys(Keys.ENTER)

        task_element = self._wait_task_in_list(task_name)
        return task_element.text.strip()
