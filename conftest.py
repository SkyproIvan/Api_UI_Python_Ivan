import pytest
import allure
from selenium import webdriver
from API.BoardsApi import BoardsApi
""" тут всё в норме"""
@pytest.fixture
def browser():
    with allure.step("Открыть и настроить браузер"):
        browser = webdriver.Chrome()
        browser.implicitly_wait(5)

        browser.maximize_window()
        yield browser

    with allure.step("Закрыть браузер"):
        browser.quit()
        """Тест отработал"""
@pytest.fixture
def api_client() -> BoardsApi():
    return BoardsApi("https://ru.yougile.com/api-v2","5zO0PQDcT4kSEHsPEzvwtu230DpmLM8VD7BaawTil7QEfToMhBur2Az7SCKPM8go")

@pytest.fixture
def api_client_no_auth() -> BoardsApi():
    return BoardsApi("https://ru.yougile.com/api-v2", "")

@pytest.fixture
def dummy_project_id() -> str:
    api = BoardsApi("https://ru.yougile.com/api-v2", "5zO0PQDcT4kSEHsPEzvwtu230DpmLM8VD7BaawTil7QEfToMhBur2Az7SCKPM8go")
    resp_project = api.create_project("Project to delete").get("id")
    return resp_project


@pytest.fixture
def dummy_project_role_id() -> str:
    # Инициализируем API-клиент
    api = BoardsApi(
        "https://ru.yougile.com/api-v2",
        "5zO0PQDcT4kSEHsPEzvwtu230DpmLM8VD7BaawTil7QEfToMhBur2Az7SCKPM8go"
    )

    # Шаг 1: Создаем проект ОДИН РАЗ и сохраняем весь ответ
    project_data = api.create_project("Project for role")

    # Извлекаем org_id (ID проекта) из ответа
    org_id = project_data.get("id")

    # Извлекаем name (имя проекта) из того же самого ответа,
    # а не создаем новый проект ради этого
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
                    "allTasks": {...},  # Остальная часть структуры разрешений остается без изменений
                    # ...
                },
                "settings": true
            },
            "children": {}
        }
    }

    # Шаг 2: Используем полученный org_id для создания роли
    resp_role = api.create_project_role(org_id=org_id, body=body)
    role_id = resp_role.get("id")

    return role_id


@pytest.fixture
def created_project_role(api_client):
    # ЭТАП НАСТРОЙКИ: Создаем роль
    org_id = "5b455e28-51d3-4491-9303-64f3dcfccabb"
    body = {
        "name": "Иван",
        "description": "Студент",
        "permissions": {...}
    }

    response = api_client.create_project_role(org_id=org_id, body=body)
    role_id = response.get("id")

    # Проверяем, что роль создалась успешно
    assert role_id is not None, "Не удалось создать проектную роль: поле 'id' отсутствует в ответе"

    # Передаем данные в тест
    yield {"org_id": org_id, "role_id": role_id}

    # ЭТАП ОЧИСТКИ: Удаляем роль после завершения теста
    print(f"\nОчистка: Удаление роли с ID {role_id}")
    try:
        api_client.delete_project_role_by_id(
            org_id=org_id,
            role_id=role_id
        )
    except Exception as e:
        print(f"Внимание: Не удалось удалить роль. Ошибка: {e}")