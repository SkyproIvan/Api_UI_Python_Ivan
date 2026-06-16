import requests

from API.BoardsApi import BoardsApi
import pytest

def test_create_project(api_client: BoardsApi):
    """Тест проверяет успешное создание проекта через API.
       """
    project = "Мой финальный проект"
    # 2. Действие: Создаем доску
    # Предполагаем, что метод create_board возвращает JSON-ответ от сервера
    create_response = api_client.create_project(project)

    assert create_response is not None, "Ответ на запрос создания доски пустой"

    project_id = create_response.get("id")
    print(project_id)
    assert project_id is not None, "В ответе на создание доски отсутствует поле 'id'"

def test_create_project_role(api_client: BoardsApi):
    """Тест проверяет успешное создание роли в проекте.
        """
    org_id = "5b455e28-51d3-4491-9303-64f3dcfccabb"
    name = "Иван"
    description = "Студент"
    body = {
        "name": name,
        "description": description
            }
    create_response = api_client.create_project_role(org_id=org_id, body=body)
    project_role_id = create_response.get("id")
    print(project_role_id)
    api_client.delete_project_role_by_id(
        org_id=org_id,
        role_id=project_role_id
    )
    assert project_role_id is not None, "В ответе на создание доски отсутствует поле 'id'"

def test_delete_project_role(api_client: BoardsApi, dummy_project_id: str, dummy_project_role_id: str):
    """
        Тест проверяет успешное создание и последующее удаление роли в проекте.
        """
    resp = api_client.delete_project_role_by_id(dummy_project_id, dummy_project_role_id)
    print(resp)
    assert resp['statusCode'] == 404, "Статус код не равен 404"

def test_create_department(api_client: BoardsApi):
    """
    Тест проверяет успешное создание отдела через API.
        """
    department = "Отдел технического перевооружения"
    #  Действие: Создаем отдел
    create_response = api_client.create_department(department)
    assert create_response is not None, "Ответ на запрос создания доски пустой"
    # Проверяем наличие ID у созданного отдела
    department_id = create_response.get("id")
    print(department_id)
    assert department_id is not None, "В ответе на создание доски отсутствует поле 'id'"

def test_create_project_no_auth(api_client_no_auth: BoardsApi):
    """Тест проверяет, что создание проекта без авторизации возвращает ошибку 401.
        """
    project = "Мой финальный проект"
    create_response = api_client_no_auth.create_project(project)
    assert create_response['statusCode'] == 401, "Статус код не равен 401"
    assert create_response['message'] == "Unauthorized", "В ответе message лтсутствует информация или отличается от ожидаемой"