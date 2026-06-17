import allure
from selenium.webdriver import ActionChains
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
        """Ожидает появления контейнера с информацией о пользователе и возвращает его имя.
                """
        (WebDriverWait(self.__driver, 10).
         until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                 "div[class='relative text-primary truncate isolate flex-1 min-w-0 break-words text-sm-regular ml-4'] span span"))))
        container = self.__driver.find_element(By.CSS_SELECTOR,
                                               "div[class='relative text-primary truncate isolate flex-1 min-w-0 break-words text-sm-regular ml-4'] span span")
        name = container.text
        # Возвращаем имя:
        return name

    @allure.step("Создать новую задачу с названием '{task_name}'")
    def create_new_task(self, task_name: str):
        """
        Создает новую задачу на главной странице.
        :param task_name: Название для новой задачи.
        """
        # Локаторы для элементов формы создания задачи
        button_locator = (By.XPATH,"//div[contains(text(),'Мои задачи')]")
        create_task_button_locator = (By.XPATH, "//span[contains(text(), 'Создать задачу')]")
        task_title_input_locator = (By.CSS_SELECTOR, "textarea[placeholder='Введите название задачи']")
        save_task_button_locator = (By.XPATH,"//div[contains(text(),'Мои задачи')]")

        # 1. Нажимаем на кнопку "Мои задачи"
        WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable(button_locator)
        ).click()
        # 2. Нажимаем на создать задачу
        WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable(create_task_button_locator)
        ).click()

        # 3. Вводим название задачи в поле ввода
        title_input = WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable(task_title_input_locator)
        )
        title_input.send_keys(task_name)

        # 4. Нажимаем на кнопку "Мои задачи" для сохранения
        WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable(save_task_button_locator)
        ).click()

        container = self.__driver.find_element(By.XPATH, "//span[contains(text(),'Новая задача для теста')]")
        name = container.text
        # Возвращаем название
        return name

    @allure.step("Удаление созданных задач")
    def delete_new_task(self):
        """Удаляет созданную задачу."""

        try:
            # 1. Находим список всех задач.
            tasks_list = self.__driver.find_elements(By.CSS_SELECTOR, "div.hoverable-group")

            if not tasks_list:
                raise Exception("Список задач пуст. Не удалось найти ни одной задачи.")

            # 2. Берем ПЕРВУЮ задачу в списке
            first_task_element = tasks_list[0]

            # --- НОВЫЙ БЛОК ДЛЯ ДИАГНОСТИКИ ---
            # Сначала наводим курсор на задачу
            actions = ActionChains(self.__driver)
            actions.move_to_element(first_task_element).perform()

            # Ищем элемент немедленно
            button_of_task_locator = (By.CSS_SELECTOR, "[data-testid='board-task-menu']")
            button_of_task_element = first_task_element.find_element(*button_of_task_locator)

            print("Кнопка меню успешно найдена! Продолжаем тест...")
            button_of_task_element.click()

            # --- КОНЕЦ БЛОКА ДИАГНОСТИКИ ---

            # Если диагностика прошла успешно, выполняем остальную логику удаления
            button_delete_locator = (By.XPATH, ".//div[contains(text(),'Удалить')]")
            button_delete = WebDriverWait(self.__driver, 10).until(
                EC.visibility_of_element_located(button_delete_locator)
            )
            button_delete.click()

            confirm_button_locator = (By.XPATH, '//div[@role="button"][normalize-space()="Удалить"]')
            confirm_button = WebDriverWait(self.__driver, 15).until(
                EC.element_to_be_clickable(confirm_button_locator)
            )
            confirm_button.click()

            WebDriverWait(self.__driver, 20).until(
                EC.invisibility_of_element(first_task_element))

            container_number = self.__driver.find_element(By.CSS_SELECTOR,
                                                          ".bg-background-secondary.rounded-4.px-6.py-2.text-subtitle-xs.text-secondary")
            number_task = container_number.text
            return number_task

            print("Задача успешно отправлена в корзину/удалена.")
            return True  # Сигнализируем об успехе



        except Exception as e:
            self.__driver.save_screenshot('final_fix_error.png')
            raise e


    @allure.step("Главная страница")
    def open_exit(self):
        button_locator = (By.CSS_SELECTOR,".truncate.ml-6.text-14.leading-4")
        WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable(button_locator)).click()
    @allure.step("Выйти из учетной записи")
    def logout(self):
        """
        Выполняет выход из учетной записи пользователя.
        """
        # 1. Открываем меню пользователя (где находится кнопка выхода)
        self.open_exit()

        # Локатор для кнопки "Выйти"
        logout_button_locator = (By.CSS_SELECTOR, "div[class='cursor-pointer']")

        # 2. Находим и нажимаем кнопку выхода
        WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable(logout_button_locator)
        ).click()

        container_exit = self.__driver.find_element(By.CSS_SELECTOR,
                                               "input[placeholder='example@mail.ru']")
        name_exit = container_exit.text
        # Возвращаем имя и почту пользователя:
        return name_exit



