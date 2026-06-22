import pytest
import sys
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import allure
from dotenv import load_dotenv  # Для загрузки переменных из .env файла
from page.AuthPage import AuthPage
from page.MainPage import MainPage

""" Для привязки к папке"""
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
# Загрузка переменных окружения из файла .env
load_dotenv()


@pytest.mark.ui
@allure.title("Негативный сценарий: попытка входа с некорректным email")
@allure.story("Попытка входа без пароля")
def test_no_password(browser_no_auth):
    """Проверяет, что система не позволяет
    войти в аккаунт с некорректным email"""
    email = "Я программист"
    password = "111"
    assert (
        email is not None and password is not None
    ), "Данные для входа (email/password) не найдены в переменных окружения"

    with allure.step("Открыть страницу аутентификации"):
        auth_page = AuthPage(browser_no_auth)
        auth_page.go()
    with allure.step("Ввести неверный логин и пароль и попробовать выполнить вход"):
        auth_page.login_as(email, password, check="No_Ok")

    with allure.step("Наличие сообщения неверный email"):
        assert auth_page.is_error(), "Нет сообщения об ошибке"


@pytest.mark.ui
@allure.title("Позитивный сценарий: создание новой задачи")
@allure.story("Создание задачи")
def test_create_task(browser, test_data: dict):
    """Проверяет успешное создание новой
    задачи с заданным названием.
    Ожидаемый результат: задача
    появляется в списке с корректным именем."""
    main_page = MainPage(browser)
    main_page.open_menu_for_create()
    with allure.step("Открыть меню задач"):

        expected_task_name = test_data.get("expected_task_name")

        with allure.step("Создать задачу"):
            # Вызываем метод, который теперь возвращает название задачи
            actual_task_name = main_page.create_new_task(expected_task_name)
            print(actual_task_name)

            with allure.step("Проверка создания задачи"):

                # Проверяем, что название задачи на странице совпадает с тем, которое мы вводили
                assert (
                    actual_task_name == expected_task_name
                ), f"Название задачи не совпадает. Ожидалось: '{expected_task_name}', получено: '{actual_task_name}'"


@pytest.mark.ui
@allure.title("Проверка отображения информации об аккаунте пользователя")
@allure.story("Получение информации об аккаунте")
def test_get_task_info(browser):
    """Проверяет, что имя пользователя
    корректно отображается в интерфейсе после входа."""
    main_page = MainPage(browser)

    with allure.step("Получить информацию об аккаунте"):
        main_page.open_menu()
        account_info = main_page.get_account_info()
        print(account_info)  # Выведет: Ivan K
        assert account_info != "", "Имя пользователя не отображается"


@pytest.mark.ui
@allure.title("Позитивный сценарий: удаление существующей задачи")
@allure.story("Удаление задачи")
def test_delete_task(browser):
    """Проверяет успешное удаление задачи из списка.
    Ожидаемый результат: количество задач
    в списке уменьшается на одну."""
    main_page = MainPage(browser)
    main_page.open_task_menu()

    with allure.step("Удалить задачу"):
        task_counter_locator = (By.CSS_SELECTOR, "div.hoverable-group")

        # Используем этот локатор для получения количества
        initial_count = len(browser.find_elements(*task_counter_locator))

        # Если список пустой, нет смысла продолжать
        assert initial_count > 0, "Нет задач для удаления"

        #  Вызываем метод, который нажимает кнопки и ждет исчезновения элемента
        main_page.delete_new_task()

        # ОЖИДАЕМ, что количество задач стало меньше
        with allure.step("Проверить, что количество задач уменьшилось"):
            # Используем wait.until с лямбда-функцией
            wait = WebDriverWait(browser, 15)

            wait.until(
                lambda driver: len(
                    driver.find_elements(By.CSS_SELECTOR, "div.hoverable-group")
                )
                < initial_count
            )

            final_count = len(
                browser.find_elements(By.CSS_SELECTOR, "div.hoverable-group")
            )

            assert (
                final_count == initial_count - 1
            ), f"Удаление не сработало. Было задач: {initial_count}, стало: {final_count}"

        print("Успешно проверено, что задача была удалена.")


@pytest.mark.ui
@allure.title("Позитивный сценарий: выход из учетной записи")
@allure.story("Выход из аккаунта")
def test_exit(browser):
    """Проверяет успешный выход пользователя из системы.
    Ожидаемый результат: имя пользователя
    перестает отображаться в интерфейсе."""
    main_page = MainPage(browser)

    with allure.step("Нажать на кнопку выхода из учетной записи"):
        name_exit = main_page.logout()
        print("Вышли из аккаунта")
        assert name_exit == "", "Имя отображается"
