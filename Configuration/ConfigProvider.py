import configparser

global_config = configparser.ConfigParser()
print("Обратились к файловой системе")
global_config.read("test_config.ini")


class ConfigProvider:
    def __init__(self):
        self.config = global_config

    def get(self, section: str, prop: str):
        return self.config[section].get(prop)

    def getint(self, section: str, prop: str):
        return self.config[section].getint(prop)

    def get_ui_url(self) -> str | None:
        return self.config["ui"].get("base_url")

    def get_api_url(self):
        return self.config["api"].get("base_url")
