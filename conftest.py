import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from API.BoardsApi import BoardsApi
from Configuration.ConfigProvider import ConfigProvider
from test_data.DataProvider import DataProvider
from page.AuthPage import AuthPage

""" Основные настройки браузеров"""


@pytest.fixture
def browser():
    with allure.step("Открыть и настроить браузер"):
        timeout = ConfigProvider().getint("ui", "timeout")
        browser_name = ConfigProvider().get("ui", "browser_name")
        if browser_name == "chrome":
            browser = webdriver.Chrome()
        else:
            service = FirefoxService(GeckoDriverManager().install())
            browser = webdriver.Firefox(service=service)

        browser.implicitly_wait(timeout)
        browser.maximize_window()
        auth = AuthPage(browser)
        auth.make_auth()
        yield browser

    with allure.step("Закрыть браузер"):
        browser.quit()


@pytest.fixture
def browser_no_auth():
    with allure.step("Открыть и настроить браузер"):
        timeout = ConfigProvider().getint("ui", "timeout")
        browser_name = ConfigProvider().get("ui", "browser_name")
        if browser_name == "chrome":
            browser = webdriver.Chrome()
        else:
            service = FirefoxService(GeckoDriverManager().install())
            browser = webdriver.Firefox(service=service)

        browser.implicitly_wait(timeout)
        browser.maximize_window()
        yield browser

    with allure.step("Закрыть браузер"):
        browser.quit()

        """Тест отработал"""


@pytest.fixture
def api_client() -> BoardsApi():
    return BoardsApi(ConfigProvider().get_api_url(), DataProvider().get_token())


@pytest.fixture
def api_client_no_auth() -> BoardsApi():
    return BoardsApi(ConfigProvider().get_api_url(), "")


@pytest.fixture
def dummy_project_id() -> str:
    api = BoardsApi(ConfigProvider().get_api_url(), DataProvider().get_token())
    resp_project = api.create_project("Project to delete").get("id")
    return resp_project


@pytest.fixture
def dummy_project_role_id() -> str:
    # Инициализируем API-клиент
    api = BoardsApi(ConfigProvider().get_api_url(), DataProvider().get_token())

    # Шаг 1: Создаем проект ОДИН РАЗ и сохраняем весь ответ
    project_data = api.create_project("Project for role")
    # Извлекаем org_id (ID проекта) из ответа
    org_id = project_data.get("id")
    # Извлекаем name (имя проекта) из того же самого ответа,
    name = project_data.get("name")
    description = "Для удаления"
    true = True
    body = {
        "name": name,
        "description": description,
        "permissions": {
            "editTitle": true,
            "delete": true,
            "addBoard": true,
            "boards": {
                "editTitle": true,
                "delete": true,
                "move": true,
                "showStickers": true,
                "editStickers": true,
                "addColumn": true,
                "columns": {
                    "editTitle": true,
                    "delete": true,
                    "move": "no",
                    "addTask": true,
                    "allTasks": {
                        ...
                    },  # Остальная часть структуры разрешений остается без изменений
                    # ...
                },
                "settings": true,
            },
            "children": {},
        },
    }

    # Шаг 2: Используем полученный org_id для создания роли
    resp_role = api.create_project_role(org_id=org_id, body=body)
    role_id = resp_role.get("id")

    return role_id


@pytest.fixture
def created_project_role(api_client):
    # ЭТАП НАСТРОЙКИ: Создаем роль
    org_id = DataProvider().get("org_id")
    body = DataProvider().get("body")
    response = api_client.create_project_role(org_id=org_id, body=body)
    role_id = response.get("id")

    # Проверяем, что роль создалась успешно
    assert (
        role_id is not None
    ), "Не удалось создать проектную роль: поле 'id' отсутствует в ответе"

    # Передаем данные в тест
    yield {"org_id": org_id, "role_id": role_id}

    # ЭТАП ОЧИСТКИ: Удаляем роль после завершения теста
    print(f"\nОчистка: Удаление роли с ID {role_id}")
    try:
        api_client.delete_project_role_by_id(org_id=org_id, role_id=role_id)
    except Exception as e:
        print(f"Внимание: Не удалось удалить роль. Ошибка: {e}")


@pytest.fixture
def test_data():
    return DataProvider()
