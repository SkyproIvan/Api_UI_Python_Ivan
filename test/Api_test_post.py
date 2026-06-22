from API.BoardsApi import BoardsApi
import pytest
import allure


@pytest.mark.api
@allure.title("Успешное создание проекта через API")
@allure.story("Управление проектами. Получение id проекта")
def test_create_project(api_client: BoardsApi, test_data: dict):
    """Тест проверяет успешное создание проекта через API."""
    project = test_data.get("project")
    with allure.step("Создание проекта с наименованием 'project'"):
        create_response = api_client.create_project(project)
        # Проверка: ответ на создание доски содержит данные
        with allure.step("Проверка id созданного проекта"):
            assert create_response is not None, "Ответ на запрос создания доски пустой"
            # Из полученного json вытягиваем id
            project_id = create_response.get("id")
            print(project_id)
            assert (
                project_id is not None
            ), "В ответе на создание доски отсутствует поле 'id'"


@pytest.mark.api
@allure.title("Успешное создание роли в проекте через API")
@allure.story("Управление ролями в проекте. Получение id роли")
def test_create_project_role(api_client: BoardsApi, test_data: dict):
    """Тест проверяет успешное создание роли в проекте."""
    org_id = test_data.get("org_id")
    body = test_data.get("body")
    with allure.step("Создание роли в проекте с 'org_id'"):
        create_response = api_client.create_project_role(org_id=org_id, body=body)
        project_role_id = create_response.get("id")
        print(project_role_id)
        with allure.step("Удаляем только что созданную роль для чистоты пространства"):
            api_client.delete_project_role_by_id(org_id=org_id, role_id=project_role_id)
            assert (
                project_role_id is not None
            ), "В ответе на создание доски отсутствует поле 'id'"


@pytest.mark.api
@allure.title("Успешное удаление роли из проекта")
@allure.story("Удаление созданных ролей, проверка через статус код")
def test_delete_project_role(
    api_client: BoardsApi, dummy_project_id: str, dummy_project_role_id: str
):
    """Тест проверяет удаление вновь
    созданной роли в проекте."""
    with allure.step("Удаление ранее созданной роли"):
        resp = api_client.delete_project_role_by_id(
            dummy_project_id, dummy_project_role_id
        )
        print(resp)
        with allure.step("Проверка статус кода удаленной роли (404)"):
            assert resp["statusCode"] == 404, "Статус код не равен 404"


@pytest.mark.api
@allure.title("Успешное создание отдела через API")
@allure.story("Создание отдела, получение id отдела")
def test_create_department(api_client: BoardsApi, test_data: dict):
    """
    Тест проверяет успешное создание отдела через API.
    """
    department = test_data.get("department")
    with allure.step("Создание нового отдела"):
        create_response = api_client.create_department(department)
        assert create_response is not None, "Ответ на запрос создания доски пустой"

        with allure.step("Проверка id вновь созданного отдела"):

            department_id = create_response.get("id")
            print(department_id)
            assert (
                department_id is not None
            ), "В ответе на создание отдела отсутствует поле 'id'"


@pytest.mark.api
@allure.title("Негативный сценарий: создание проекта без авторизации (401)")
@allure.story("Аутентификация и авторизация, получение предупреждения об ошибке")
def test_create_project_no_auth(api_client_no_auth: BoardsApi, test_data: dict):
    """Тест проверяет, что создание проекта без авторизации возвращает ошибку 401."""
    project = test_data.get("project")
    with allure.step("Попытка входа в аккаунт без пароля"):
        create_response = api_client_no_auth.create_project(project)
        with allure.step("Проверка статус кода ответа на неверный пароль"):
            assert create_response["statusCode"] == 401, "Статус код не равен 401"
            assert (
                create_response["message"] == "Unauthorized"
            ), "В ответе message лтсутствует информация или отличается от ожидаемой"
