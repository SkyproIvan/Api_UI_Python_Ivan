import requests
from sqlalchemy import true


class BoardsApi:

    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url.rstrip('/')
        self.token = token

    def get_all_boards_by_org_id(self, org_id: str) -> dict:
        # 1. Корректно формируем URL с помощью f-строки
        path = f"{self.base_url}/projects/{org_id}"

        # 2. Передаем токен в заголовках (Authorization).
        #    Формат "Bearer" очень распространен, но если API требует просто токен, уберите "Bearer "
        headers = {"Authorization": f"Bearer {self.token}"}

        # 3. Выполняем запрос
        resp = requests.get(path, headers=headers)

        # 4. Проверяем успешность ответа перед возвратом JSON
        resp.raise_for_status()  # Вызовет исключение, если запрос был неудачным (код 4xx или 5xx)

        return resp.json()

    def create_project(self, name, default_lists=True):
        body = {
            "title": name
        }
        headers = {"Authorization": f"Bearer {self.token}"}
        path = f"{self.base_url}/projects"
        resp = requests.post(path, json=body, headers=headers)

        return resp.json()

    def create_project_role(self, body, org_id, default_lists=True):
        true = True
        name = body["name"]
        description = body["description"]
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

        headers = {"Authorization": f"Bearer {self.token}"}
        path = f"{self.base_url}/projects/{org_id}/roles"
        resp = requests.post(path, json=body, headers=headers)

        return resp.json()


    def delete_project_role_by_id(self, org_id: str, role_id: str):
        headers = {"Authorization": f"Bearer {self.token}"}
        path = f"{self.base_url}/projects/{org_id}/roles/{role_id}"
        resp = requests.delete(path, json=headers, headers=headers)

        return resp.json()
