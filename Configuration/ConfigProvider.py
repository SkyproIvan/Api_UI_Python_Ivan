import configparser
from encodings.punycode import selective_find


class ConfigProvider:



    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.sections()
        self.config.read('test_config.ini')

    def get(self, section:str, prop:str):
        return self.config[section].get(prop)
    def getint(self, section:str, prop:str):
        return self.config[section].getint(prop)
    def get_ui_url(self):
        return self.config["ui"].get("base_url")
    def get_api_url(self):
        return self.config["api"].get("base_url")
    def get_api_token(self):
        return self.config["api"].get("token")


