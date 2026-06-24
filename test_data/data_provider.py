import json
from typing import Any, Optional


class DataProvider:
    """
    Класс для чтения данных из JSON-файла и предоставления доступа к ним.
    """

    def __init__(
        self, file_path: str = "test_data.json", encoding: str = "utf-8"
    ) -> None:
        """

        Args:
            file_path: Путь к JSON-файлу.
            encoding: Кодировка файла (по умолчанию 'utf-8').

        Raises:
            FileNotFoundError: Если файл не найден.
            json.JSONDecodeError: Если файл не является валидным JSON.
        """
        self.file_path = file_path
        self.data = {}

        try:
            with open(file_path, "r", encoding=encoding) as my_file:
                # Используем json.load() для чтения из объекта файла
                self.data = json.load(my_file)
        except FileNotFoundError:
            print(f"Ошибка: Файл '{file_path}' не найден.")
            raise
        except json.JSONDecodeError as e:
            print(f"Ошибка декодирования JSON в файле '{file_path}': {e}")
            raise

    def get(self, prop: str) -> Optional[Any]:
        """
        Возвращает значение свойства по ключу.

        Args:
            prop: Ключ в JSON-данных.

        Returns:
            Значение свойства или None, если ключа не существует.
        """
        return self.data.get(prop)

    def get_token(self) -> Optional[str]:
        """Возвращает токен авторизации."""
        return self.get("token")
