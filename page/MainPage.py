import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


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

        # 4. Нажимаем на кнопку "Сохранить"
        WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable(save_task_button_locator)
        ).click()

        container = self.__driver.find_element(By.XPATH, "//span[contains(text(),'Новая задача для теста')]")
        name = container.text
        # Возвращаем имя и почту пользователя:
        return name

    @allure.step("Удаление созданных задач")
    def delete_new_task(self):
        """"Удаляет созданную задачу.
                """
        cont_of_task_locator = (By.CSS_SELECTOR, "div.group\\/row.flex.flex-col.hoverable-group")

        # Локатор для иконки меню (трех точек) внутри контейнера
        button_of_task_locator = (By.CSS_SELECTOR, "div > [data-testid='board-task-menu']")

        # Локатор для кнопки "Удалить" в выпадающем меню
        button_delete_locator = (By.XPATH, "//div[contains(text(),'Удалить')]")
        # Локатор для подтверждения
        button_delete_ok = (By.XPATH, "//div[@class='text-left flex items-center justify-center w-full'][contains(text(),'Удалить')]")

        try:
            # 1. Находим контейнер задачи и кликаем по нему, чтобы вызвать появление меню
            # Используем visibility_of_element_located, так как элемент должен быть виден для клика
            cont_of_task_element = WebDriverWait(self.__driver, 10).until(
                EC.visibility_of_element_located(cont_of_task_locator)
            )
            cont_of_task_element.click()  # Или можно использовать ActionChains для клика

            # 2. Находим иконку меню (кнопку) внутри уже найденного контейнера
            # Это более надежно, чем искать по всему документу
            button_of_task_element = WebDriverWait(self.__driver, 5).until(
                EC.element_to_be_clickable(button_of_task_locator)
            )


            # 3. Наводим курсор на найденную иконку меню
            actions = ActionChains(self.__driver)
            actions.move_to_element(button_of_task_element).perform()
            button_of_task_element.click()

            # 4. Ожидаем появления кнопки "Удалить" и кликаем по ней
            # Иногда кнопка появляется не сразу после наведения, поэтому ждем ее
            button_delete = WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable(button_delete_locator)
            )
            button_delete.click()

            click_ok = WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable(button_delete_ok)
            )
            time.sleep(5)

            click_ok.click()
            time.sleep(5)

        except Exception as e:
            print(f"Произошла ошибка при удалении задачи: {e}")
            # Здесь можно добавить сохранение скриншота для отладки
            # self.__driver.save_screenshot('error_delete_task.png')
            raise  # Пробрасываем исключение, чтобы тест упал

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


