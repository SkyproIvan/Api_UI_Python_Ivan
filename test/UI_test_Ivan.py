import sys
import os
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
    task_name = "Задача 1 API"

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

    with allure.step("Получить информацию об аккаунте"):
        account_info = main_page.get_account_info()
        assert account_info != "", "Имя пользователя не отображается"

    with allure.step("Нажать на кнопку выхода из учетной записи"):
        main_page.logout()

    # --- Проверки (Assertions) ---

    # Получаем текущий URL после нажатия на "Выход"
    current_url = main_page.get_current_url()

    with allure.step(f"Создать новую задачу с названием '{task_name}'"):
        main_page.create_new_task(task_name)

    with allure.step("Проверить, что текущий URL содержит '/login'"):
        # Используем более надежный метод проверки URL.
        # Вместо точного сравнения, проверяем наличие ключевого сегмента.
        assert "/login" in current_url, \
            f"Не удалось выйти из системы. Текущий URL: {current_url}, ожидается страница логина."




        """ Тесты сработали"""


