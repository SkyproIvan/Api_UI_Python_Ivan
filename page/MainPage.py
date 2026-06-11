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
        """Ожидает появления контейнера с информацией о пользователе и возвращает его имя.
                """
        (WebDriverWait(self.__driver, 10).
         until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                 "div[class='relative text-primary truncate isolate flex-1 min-w-0 break-words text-sm-regular ml-4'] span span"))))
        container = self.__driver.find_element(By.CSS_SELECTOR,
                                               "div[class='relative text-primary truncate isolate flex-1 min-w-0 break-words text-sm-regular ml-4'] span span")
        name = container.text
        # Возвращаем имя и почту пользователя:
        return name

    @allure.step("Создать новую задачу с названием '{task_name}'")
    def create_new_task(self, task_name: str):
        """
        Создает новую задачу на главной странице.
        :param task_name: Название для новой задачи.
        """
        # Локаторы для элементов формы создания задачи
        create_task_button_locator = (By.CSS_SELECTOR, "[data-test-id='create-task-button']")
        task_title_input_locator = (By.CSS_SELECTOR, "[data-test-id='task-title-input']")
        save_task_button_locator = (By.CSS_SELECTOR, "[data-test-id='save-task-button']")

        # 1. Нажимаем на кнопку "Создать задачу"
        WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable(create_task_button_locator)
        ).click()

        # 2. Вводим название задачи в поле ввода
        title_input = WebDriverWait(self.__driver, 10).until(
            EC.visibility_of_element_located(task_title_input_locator)
        )
        title_input.clear()
        title_input.send_keys(task_name)

        # 3. Нажимаем на кнопку "Сохранить"
        WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable(save_task_button_locator)
        ).click()

    @allure.step("Проверить, что задача с названием '{task_name}' отображается в списке")
    def is_task_present(self, task_name: str) -> bool:
        """
        Проверяет наличие задачи с указанным названием в списке задач.

        :param task_name: Название задачи для поиска.
        :return: True, если задача найдена, иначе False.
        """
        # Динамический локатор для поиска задачи по названию
        task_locator = (By.CSS_SELECTOR, f"div[class='relative text-primary truncate isolate flex-1 min-w-0 break-words text-sm-regular ml-4'] span span]='{task_name}']")

        try:
            # Пытаемся найти элемент. Если он появится в течение 5 секунд, вернем True.
            WebDriverWait(self.__driver, 5).until(
                EC.presence_of_element_located(task_locator)
            )
            return True
        except:
            # Если элемент не найден за указанное время, возвращаем False.
            return False

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

    @allure.step("Создать новую задачу с названием '{task_name}'")
    def create_new_task(self, task_name: str):
        """
        Создает новую задачу и ожидает ее появления в списке.
        """
        # ... (код для нажатия кнопки "Создать", ввода текста и нажатия "Сохранить" остается без изменений)
        save_task_button_locator = (By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)")
        WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable(save_task_button_locator)
        ).click()

        WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable(save_task_button_locator)
        ).send_keys("Задча API")

        # --- ДОБАВЛЕНА НОВАЯ ЛОГИКА ---
        with allure.step(f"Дождаться появления задачи '{task_name}' в списке"):
            # Ждем, пока задача появится и станет видимой.
            # Используем тот же локатор, что и в is_task_present
            task_locator = (By.CSS_SELECTOR, f"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)('{task_name}')")
            WebDriverWait(self.__driver, 10).until(
                EC.visibility_of_element_located(task_locator),
                message=f"Задача '{task_name}' не появилась в списке после создания."
            )
