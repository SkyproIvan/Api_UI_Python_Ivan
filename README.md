# Api_UI_Python_Ivan

## Шаблон для автоматизации тестирования на python

### Шаги
1. Склонировать проект 'git clone https://github.com/SkyproIvan/Api_UI_Python_Ivan.git
2. Установить зависимости 'pip3 install > -r requirements.txt'
3. Запустить тесты только для API: 'pytest -m api', только для UI: 'pytest -m ui', ВСЕ тесты: 'pytest'           
4. Сгенерировать отчет 'pytest --alluredir=allure-results'
5. Открыть отчет 'allure serve allure-results'

### Стек:
- pytest
- selenium
- webdriver manager
- requests
- allure
- configparser
- json


### Структура:
- ./test - тесты API и UI
- ./page - описание страниц
- ./api - хелперы для работы с API
- test_config.ini - настройка тестов
- ./configuration - провайдер настроек
- ./test_data - провайдер тестовых данных
- test_data.json


### Полезные ссылки
- [Подсказка по markdown](https://www.markdownguide.org/basic-syntax/)
- [Генератор файла .gitignore](https://www.toptal.com/developers/gitignore/)
- [Про configparser](https://docs.python.org/3/library/configparser.html)
- [Про pip freeze](https://pip.pypa.io/en/stable/cli/pip_freeze/)