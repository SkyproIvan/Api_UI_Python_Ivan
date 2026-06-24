import os
import sys
import uuid
import pytest
import allure
from dotenv import load_dotenv
from page.auth_page import AuthPage
from page.main_page import MainPage


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
load_dotenv()


@pytest.mark.ui
@allure.title("Негативный сценарий: попытка входа с некорректным email")
@allure.story("Попытка входа без пароля")
def test_no_password(browser_no_auth, test_data: dict):
    """Проверяет, что система не позволяет
    войти в аккаунт с некорректным email"""
    email = test_data.get("invalid_email")
    password = test_data.get("invalid_password")
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
def test_create_task(browser):
    """Проверяет успешное создание новой задачи с уникальным именем."""
    main_page = MainPage(browser)
    task_name = f"Автотест_{uuid.uuid4().hex[:8]}"

    with allure.step("Открыть раздел «Мои задачи»"):
        main_page.open_menu_for_create()

    with allure.step(f"Создать задачу с именем '{task_name}'"):
        actual_task_name = main_page.create_new_task(task_name)

    with allure.step("Проверить имя созданной задачи в списке"):
        assert actual_task_name == task_name, (
            f"Имя задачи не совпадает. "
            f"Ожидалось: '{task_name}', получено: '{actual_task_name}'"
        )


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

    with allure.step("Получение списка задач"):
        initial_count = main_page.get_task_count()
        assert initial_count > 0, "Нет задач для удаления"

    with allure.step("Удалить задачу"):
        main_page.delete_new_task()

        with allure.step("Проверить, что количество задач уменьшилось"):
            final_count = main_page.wait_for_task_count_change(initial_count)
            assert (
                final_count == initial_count - 1
            ), f"Удаление не сработало. Было задач: {initial_count}, стало: {final_count}"


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
        assert name_exit == "", "Имя отображается"
