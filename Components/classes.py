
import json


class LoginModel:
    login = ""
    password = ""
    login_token = 0

    def __init__(self) -> None:
        pass

    def __init__(self, login, password, login_token):
        self.login = login
        self.password = password
        self.login_token = login_token

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=3)
