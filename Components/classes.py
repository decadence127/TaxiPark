import json


class Driver:
    def __init__(self, name="", surname="", middle_name="", age=0, id=0):
        self.__id = id
        self.__name = name
        self.__surname = surname
        self.__middle_name = middle_name
        self.__age = age

    def __init__(self, name="", surname="", middle_name="", age=0):
        self.__name = name
        self.__surname = surname
        self.__middle_name = middle_name
        self.__age = age

    def __str__(self):
        return "Driver: Name = " + str(self.__name) + "; middle name = " + str(self.__middle_name) + "; surname = " + str(self.__surname) + "; age = " + str(self.__age) + ""


class QueryModel:
    login = ""
    password = ""
    balance = 0.0
    query_token = 0
    secret_key = ""

    def __init__(self) -> None:
        pass

    def __init__(self, *args):
        if len(args) == 4:
            self.login = args[0]
            self.password = args[1]
            self.secret_key = args[2]
            self.query_token = args[3]

        elif len(args) == 5:
            self.login = args[0]
            self.password = args[1]
            self.secret_key = args[2]
            self.query_token = args[3]
            self.balance = args[4]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class TaxiModel:

    def __init__(self, car_model="", query_token=0, name="", surname="", middle_name="", age=0, id=0):
        self.__car_model = car_model
        self.query_token = query_token
        self.__driverData = Driver(name, surname, middle_name, age, id)

    def __init__(self, car_model="", query_token=0, name="", surname="", middle_name="", age=0):
        self.__car_model = car_model
        self.query_token = query_token
        self.__driverData = Driver(name, surname, middle_name, age)

    def setDriver(self, name, surname, middle_name, age, id):
        self.__driverData = Driver(name, surname, middle_name, age, id)

    def get_taxi(self):
        return self.__car_model, self.query_token, self.__driverData

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class AnswerModel:
    balance = 0.0
    answer_message = ""

    def __init__(self, answer_message="", balance=0.0):
        self.answer_message = answer_message
        self.balance = balance

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
