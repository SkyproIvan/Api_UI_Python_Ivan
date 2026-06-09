from dis import name

import project_name
import requests
from allure_commons._allure import description
from sqlalchemy import true

from API.BoardsApi import BoardsApi


def test_get_boards():
    api = BoardsApi(
        base_url="https://ru.yougile.com/api-v2",
        token="5zO0PQDcT4kSEHsPEzvwtu230DpmLM8VD7BaawTil7QEfToMhBur2Az7SCKPM8go")

    try:
        boards_data = api.get_all_boards_by_org_id("00127ef9-e88c-4ac1-8a93-b3c98a217ce0")
        print(boards_data)
    except requests.exceptions.HTTPError as err:
        print(f"Ошибка при запросе к API: {err}")


def test_create_project():
    api = BoardsApi(
        base_url="https://ru.yougile.com/api-v2",
        token="5zO0PQDcT4kSEHsPEzvwtu230DpmLM8VD7BaawTil7QEfToMhBur2Az7SCKPM8go")

    project = "Мой финальный проект"

    # 2. Действие: Создаем доску
    # Предполагаем, что метод create_board возвращает JSON-ответ от сервера
    create_response = api.create_project(project)

    # 3. Проверка 1: Убеждаемся, что запрос прошел успешно
    # Проверяем, что ответ не None и содержит ожидаемые поля
    assert create_response is not None, "Ответ на запрос создания доски пустой"

    # Проверяем наличие ID у созданной доски
    project_id = create_response.get("id")
    print(project_id)
    assert project_id is not None, "В ответе на создание доски отсутствует поле 'id'"


def test_create_project_role():
    api = BoardsApi(
        base_url="https://ru.yougile.com/api-v2",
        token="5zO0PQDcT4kSEHsPEzvwtu230DpmLM8VD7BaawTil7QEfToMhBur2Az7SCKPM8go")
    org_id = "00127ef9-e88c-4ac1-8a93-b3c98a217ce0"
    true = True
    name = "Иван"
    description = "Студент"
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
                        "show": true,
                        "delete": true,
                        "editTitle": true,
                        "editDescription": true,
                        "complete": true,
                        "close": true,
                        "assignUsers": "no",
                        "connect": true,
                        "editSubtasks": "no",
                        "editStickers": true,
                        "editPins": true,
                        "move": "no",
                        "sendMessages": true,
                        "sendFiles": true,
                        "editWhoToNotify": "no"
                    },
                    "withMeTasks": {
                        "show": true,
                        "delete": true,
                        "editTitle": true,
                        "editDescription": true,
                        "complete": true,
                        "close": true,
                        "assignUsers": "no",
                        "connect": true,
                        "editSubtasks": "no",
                        "editStickers": true,
                        "editPins": true,
                        "move": "no",
                        "sendMessages": true,
                        "sendFiles": true,
                        "editWhoToNotify": "no"
                    },
                    "myTasks": {
                        "show": true,
                        "delete": true,
                        "editTitle": true,
                        "editDescription": true,
                        "complete": true,
                        "close": true,
                        "assignUsers": "no",
                        "connect": true,
                        "editSubtasks": "no",
                        "editStickers": true,
                        "editPins": true,
                        "move": "no",
                        "sendMessages": true,
                        "sendFiles": true,
                        "editWhoToNotify": "no"
                    },
                    "createdByMeTasks": {
                        "show": true,
                        "delete": true,
                        "editTitle": true,
                        "editDescription": true,
                        "complete": true,
                        "close": true,
                        "assignUsers": "no",
                        "connect": true,
                        "editSubtasks": "no",
                        "editStickers": true,
                        "editPins": true,
                        "move": "no",
                        "sendMessages": true,
                        "sendFiles": true,
                        "editWhoToNotify": "no"
                    }
                },
                "settings": true
            },
            "children": {}
        }
    }

    create_response = api.create_project_role(org_id=org_id, body=body)
    project_role_id = create_response.get("id")
    print(project_role_id)
    assert project_role_id is not None, "В ответе на создание доски отсутствует поле 'id'"


def test_delete_projtct_role():
    api = BoardsApi(
        base_url="https://ru.yougile.com/api-v2",
        token="5zO0PQDcT4kSEHsPEzvwtu230DpmLM8VD7BaawTil7QEfToMhBur2Az7SCKPM8go")
    org_id = "00127ef9-e88c-4ac1-8a93-b3c98a217ce0"
    role_id = "3d35f9d0-6c46-4ab7-8eb0-ba4a9044a09d"

    resp = api.delete_project_role_by_id(org_id, role_id)
    print(resp)


