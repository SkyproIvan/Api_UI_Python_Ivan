import requests

class BoardsApi:

    def __init__(self, base_url: str, token: str) -> None:
        """Инициализация клиента API.
               :param base_url: Базовый URL API (например, 'https://api.example.com/v1')
               :param token: Токен авторизации (Bearer Token)"""
        self.base_url = base_url.rstrip('/')
        self.token = token

    def create_project(self, name):
        """Создание нового проекта.
               :param name: Название проекта.
               """
        body = {
            "title": name
        }
        headers = {"Authorization": f"Bearer {self.token}"}
        path = f"{self.base_url}/projects"
        resp = requests.post(path, json=body, headers=headers)

        return resp.json()

    def create_project_role(self, body, org_id):
        """Создание роли в проекте.
                :param body: Словарь с данными роли (name, description).
                :param org_id: ID организации/проекта.
                """
        name = body["name"]
        description = body["description"]
        body = {
            "name": name,
      "description": description,
      "permissions": {
        "editTitle": True,
        "delete": True,
        "addBoard": True,
        "boards": {
          "editTitle": True,
          "delete": True,
          "move": True,
          "showStickers": True,
          "editStickers": True,
          "addColumn": True,
          "columns": {
        "editTitle": True,
        "delete": True,
        "move": "no",
        "addTask": True,
        "allTasks": {
          "show": True,
          "delete": True,
          "editTitle": True,
          "editDescription": True,
          "complete": True,
          "close": True,
          "assignUsers": "no",
          "connect": True,
          "editSubtasks": "no",
          "editStickers": True,
          "editPins": True,
          "move": "no",
          "sendMessages": True,
          "sendFiles": True,
          "editWhoToNotify": "no"
        },
        "withMeTasks": {
          "show": True,
          "delete": True,
          "editTitle": True,
          "editDescription": True,
          "complete": True,
          "close": True,
          "assignUsers": "no",
          "connect": True,
          "editSubtasks": "no",
          "editStickers": True,
          "editPins": True,
          "move": "no",
          "sendMessages": True,
          "sendFiles": True,
          "editWhoToNotify": "no"
        },
        "myTasks": {
          "show": True,
          "delete": True,
          "editTitle": True,
          "editDescription": True,
          "complete": True,
          "close": True,
          "assignUsers": "no",
          "connect": True,
          "editSubtasks": "no",
          "editStickers": True,
          "editPins": True,
          "move": "no",
          "sendMessages": True,
          "sendFiles": True,
          "editWhoToNotify": "no"
        },
        "createdByMeTasks": {
          "show": True,
          "delete": True,
          "editTitle": True,
          "editDescription": True,
          "complete": True,
          "close": True,
          "assignUsers": "no",
          "connect": True,
          "editSubtasks": "no",
          "editStickers": True,
          "editPins": True,
          "move": "no",
          "sendMessages": True,
          "sendFiles": True,
          "editWhoToNotify": "no"
        }
      },
      "settings": True
    },
    "children": {}
  }
}
        headers = {"Authorization": f"Bearer {self.token}"}
        path = f"{self.base_url}/projects/{org_id}/roles"
        resp = requests.post(path, json=body, headers=headers)

        return resp.json()

    def delete_project_role_by_id(self, org_id: str, role_id: str):
        """Удаление роли по её ID.
               :param org_id: ID организации/проекта.
               :param role_id: ID роли для удаления.
               """
        headers = {"Authorization": f"Bearer {self.token}"}
        path = f"{self.base_url}/projects/{org_id}/roles/{role_id}"
        resp = requests.delete(path, json=headers, headers=headers)

        return resp.json()

    def create_department(self, name):
        """Создание нового отдела.
                :param name: Название отдела."""
        body = {
            "title": name
            }
        headers = {"Authorization": f"Bearer {self.token}"}
        path = f"{self.base_url}/departments"
        resp = requests.post(path, json=body, headers=headers)
        return resp.json()
    """Конец тестирования"""
