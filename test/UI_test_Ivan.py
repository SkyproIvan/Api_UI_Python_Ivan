import sys
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

""" Для привязки к папке"""
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
import allure
from dotenv import load_dotenv # Для загрузки переменных из .env файла
from page.AuthPage import AuthPage
from page.MainPage import MainPage

# Загрузка переменных окружения из файла .env
load_dotenv()

def test_auth(browser):

    email = os.getenv("TEST_USER_EMAIL")
    password = os.getenv("TEST_USER_PASSWORD")
    assert email is not None and password is not None, "Данные для входа (email/password) не найдены в переменных окружения"

    with allure.step("Открыть страницу аутентификации"):
        auth_page = AuthPage(browser)
        auth_page.go()
    with allure.step("Ввести логин и пароль и выполнить вход"):
        auth_page.login_as(email, password)

    with allure.step("Инициализировать главную страницу"):
        main_page = MainPage(browser)
    with allure.step("Открыть меню аккаунта"):
        main_page.open_menu()

    # Проверяем, что после запуска теста URL заканчивается заданной подстрокой:
    with allure.step("Проверить текущий URL страницы"):
        current_url = main_page.get_current_url()
        assert "my-tasks" in current_url, f"URL '{current_url}' не содержит 'my-tasks'"

    with allure.step("Создать задачу"):
        # Переменная для наглядности
        expected_task_name = "Новая задача для теста"

        # Вызываем метод, который теперь возвращает название задачи
        actual_task_name = main_page.create_new_task(expected_task_name)

        # Проверяем, что название задачи на странице совпадает с тем, которое мы вводили
        assert actual_task_name == expected_task_name, \
            f"Название задачи не совпадает. Ожидалось: '{expected_task_name}', получено: '{actual_task_name}'"

    with allure.step("Получить информацию об аккаунте"):
       account_info = main_page.get_account_info()
       assert account_info != "", "Имя пользователя не отображается"

    with allure.step("Удалить задачу"):
        task_counter_locator = (By.CSS_SELECTOR,
                                "div.hoverable-group")

        # Используем этот локатор для получения количества
        initial_count = len(browser.find_elements(*task_counter_locator))

        # Если список пустой, нет смысла продолжать
        assert initial_count > 0, "Нет задач для удаления"

        # 2. Вызываем метод, который нажимает кнопки и ждет исчезновения элемента
        main_page.delete_new_task()


        # 3. ОЖИДАЕМ, что количество задач стало меньше
        with allure.step("Проверить, что количество задач уменьшилось"):
            # Используем wait.until с лямбда-функцией
            wait = WebDriverWait(browser, 15)

            wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "div.hoverable-group")) < initial_count)

            final_count = len(browser.find_elements(By.CSS_SELECTOR, "div.hoverable-group"))

            assert final_count == initial_count - 1, \
                f"Удаление не сработало. Было задач: {initial_count}, стало: {final_count}"

        print("Успешно проверено, что задача была удалена.")

    with allure.step("Нажать на кнопку выхода из учетной записи"):
       name_exit = main_page.logout()
       print("Вышли из аккаунта")

       assert name_exit == "", "Имя отображается"





