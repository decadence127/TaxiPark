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
    permission = 0

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

        elif len(args) == 2:
            self.balance = args[0]
            self.permission = args[1]
        elif len(args) == 3:
            self.login = args[0]
            self.balance = args[1]
            self.query_token = args[2]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def setRideDistance(self, ride_distance):
        self.ride_distance = ride_distance


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
    permission = 0
    ride_cost = 0.0
    driver_delay = 0.0

    def __init__(self, *args):
        if len(args) == 4:
            self.answer_message = args[0]
            self.balance = args[1]
            self.driver_delay = args[2]
            self.ride_cost = args[3]
        if len(args) == 3:
            self.answer_message = args[0]
            self.balance = args[1]
            self.permission = args[2]
        if len(args) == 2:
            self.answer_message = args[0]
            self.balance = args[1]
        if len(args) == 1:
            self.answer_message = args[0]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Project:
    positiveProb: float
    negativeProb: float
    moneyLoss: int
    moneyGain: int

    def __init__(self, positiveProb, negativeProb, moneyLoss, moneyGain):
        self.positiveProb = positiveProb
        self.negativeProb = negativeProb
        self.moneyLoss = moneyLoss
        self.moneyGain = moneyGain

    def __str__(self):
        return "{} {} {} {}\n".format(self.positiveProb, self.negativeProb, self.moneyLoss, self.moneyGain)


class MethodQuery:
    projectData = []
    query_token: int

    def __init__(self, query_token):
        self.projectData = []
        self.query_token = query_token

    def addProject(self, *args):
        for i in range(len(args)):
            self.projectData.append(args[i])

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
