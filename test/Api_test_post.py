from API.BoardsApi import BoardsApi
import pytest


@pytest.mark.api
def test_create_project(api_client: BoardsApi, test_data: dict):
    """Тест проверяет успешное создание проекта через API."""
    project = test_data.get("project")
    # Действие: Создаем доску
    # Предполагаем, что метод create_board возвращает JSON-ответ от сервера
    create_response = api_client.create_project(project)

    assert create_response is not None, "Ответ на запрос создания доски пустой"

    project_id = create_response.get("id")
    print(project_id)
    assert project_id is not None, "В ответе на создание доски отсутствует поле 'id'"


@pytest.mark.api
def test_create_project_role(api_client: BoardsApi, test_data: dict):
    """Тест проверяет успешное создание роли в проекте."""
    org_id = test_data.get("org_id")
    body = test_data.get("body")
    #  Действие: Создаем роль
    create_response = api_client.create_project_role(org_id=org_id, body=body)
    project_role_id = create_response.get("id")
    print(project_role_id)
    #  Действие: удаляем вновь созданную роль
    api_client.delete_project_role_by_id(org_id=org_id, role_id=project_role_id)
    assert (
        project_role_id is not None
    ), "В ответе на создание доски отсутствует поле 'id'"


@pytest.mark.api
def test_delete_project_role(
    api_client: BoardsApi, dummy_project_id: str, dummy_project_role_id: str
):
    """
    Тест проверяет успешное создание
    и последующее удаление роли в проекте.
    """
    resp = api_client.delete_project_role_by_id(dummy_project_id, dummy_project_role_id)

    print(resp)
    assert resp["statusCode"] == 404, "Статус код не равен 404"


@pytest.mark.api
def test_create_department(api_client: BoardsApi, test_data: dict):
    """
    Тест проверяет успешное создание отдела через API.
    """
    department = test_data.get("department")
    #  Действие: Создаем отдел
    create_response = api_client.create_department(department)
    assert create_response is not None, "Ответ на запрос создания доски пустой"

    # Проверяем наличие
    # ID у созданного отдела
    department_id = create_response.get("id")
    print(department_id)
    assert department_id is not None, "В ответе на создание доски отсутствует поле 'id'"


@pytest.mark.api
def test_create_project_no_auth(api_client_no_auth: BoardsApi, test_data: dict):
    """Тест проверяет, что создание проекта без авторизации возвращает ошибку 401."""
    project = test_data.get("project")
    create_response = api_client_no_auth.create_project(project)
    #  Проверка негативного сценария
    assert create_response["statusCode"] == 401, "Статус код не равен 401"
    assert (
        create_response["message"] == "Unauthorized"
    ), "В ответе message лтсутствует информация или отличается от ожидаемой"
