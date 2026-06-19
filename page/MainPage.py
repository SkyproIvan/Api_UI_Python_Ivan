import allure
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    def __init__(self, driver: WebDriver) -> None:
        self.__driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        return self.__driver.current_url

    @allure.step("Мой аккаунт")
    def open_menu(self):
        self.__driver.find_element(
            By.CSS_SELECTOR, ".truncate.ml-6.text-14.leading-4"
        ).click()
        # Проверяем, что после запуска теста URL заканчивается заданной подстрокой:
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

        # Ожидаем, пока элемент станет видимым и готовым к взаимодействию.
        element = self.wait.until(EC.visibility_of_element_located(input_field_locator))

        # Для <input> и <textarea> используем get_attribute('value')
        return element.get_attribute("value")

    @allure.step("Удаление созданных задач")
    def delete_new_task(self):
        """Удаляет созданную задачу."""

        try:
            # Находим список всех задач.
            tasks_list = self.__driver.find_elements(
                By.CSS_SELECTOR, "div.hoverable-group"
            )

            if not tasks_list:
                raise Exception("Список задач пуст. Не удалось найти ни одной задачи.")

            # Берем ПЕРВУЮ задачу в списке
            first_task_element = tasks_list[0]

            # Сначала наводим курсор на задачу
            actions = ActionChains(self.__driver)
            actions.move_to_element(first_task_element).perform()

            # Ищем элемент немедленно
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

            # Если диагностика прошла успешно, выполняем удаление
            # Находим в меню команду удалить
            button_delete_locator = (By.XPATH, ".//div[contains(text(),'Удалить')]")
            button_delete = self.wait.until(
                EC.visibility_of_element_located(button_delete_locator)
            )
            # нажать удалить
            button_delete.click()

            # Подтверждение удаления во всплывающем окне
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
            # забираем количество оставшихся задач
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
        # Открываем меню пользователя (где находится кнопка выхода)
        self.open_exit()

        # Локатор для кнопки "Выйти"
        logout_button_locator = (By.CSS_SELECTOR, "div[class='cursor-pointer']")

        # Находим и нажимаем кнопку выхода
        self.wait.until(EC.element_to_be_clickable(logout_button_locator)).click()

        container_exit = self.__driver.find_element(
            By.CSS_SELECTOR, "input[placeholder='example@mail.ru']"
        )
        name_exit = container_exit.text
        # Возвращаем имя и почту пользователя:
        return name_exit

    @allure.step("Мои задачи")
    def open_menu_for_create(self):
        self.__driver.find_element(
            By.XPATH,
            "//div[@class='select-none text-14 leading-4 text-panel-text-primary whitespace-nowrap'][contains(text(),'Мои задачи')]",
        ).click()

    def create_new_task(self, task_name: str):
        """
        Создает новую задачу через автосохранение при клике вне поля ввода.
        :param task_name: Название для новой задачи.
        """

        # Локаторы (предполагается, что мы уже находимся в нужном разделе)
        create_task_button_locator = (
            By.XPATH,
            "//span[contains(text(), 'Создать задачу')]",
        )
        task_title_input_locator = (
            By.CSS_SELECTOR,
            "textarea[placeholder='Введите название задачи']",
        )

        # Локатор для кнопки, которая закрывает форму и сохраняет изменения
        save_task_button_locator = (By.XPATH, "//div[contains(text(),'Мои задачи')]")

        with allure.step(f"Проверить появление задачи '{task_name}' в списке"):
            try:
                # Нажимаем на кнопку "Создать задачу"
                self.wait.until(
                    EC.element_to_be_clickable(create_task_button_locator)
                ).click()

                # Вводим название задачи
                title_input = self.wait.until(
                    EC.presence_of_element_located(task_title_input_locator)
                )
                title_input.send_keys(task_name)

                # Кликаем на "Мои задачи", чтобы сработало автосохранение
                self.wait.until(
                    EC.element_to_be_clickable(save_task_button_locator)
                ).click()

                # Ждем появления элемента с нашим текстом
                # Используем XPATH, который ищет span с точным или частичным совпадением текста
                self.wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, f"//span[contains(text(), '{task_name}')]")
                    )
                )

                return task_name

            except TimeoutException:
                # Если ожидание не сработало, собираем отладочную информацию
                assert (
                    False
                ), f"Тайм-аут ожидания: Задача '{task_name}' не появилась в списке после автосохранения."
