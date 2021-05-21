
class Driver:
    def __init__(self, name="", surname="", middle_name="", age=0, id=0):
        self.__id = id
        self.__name = name
        self.__surname = surname
        self.__middle_name = middle_name
        self.__age = age

    def __repr__(self):
        return "Driver: Name = " + str(self.__name) + "; middle name = " + str(self.__middle_name) + "; surname = " + str(self.__surname) + "; age = " + str(self.__age) + ""


class TaxiModel:

    def __init__(self, car_model="", query_token=0):
        self.__car_model = car_model
        self.__query_token = query_token
        self.__driverList = []

    def addDriver(self, name, surname, middle_name, age, id):
        self.__driverList.append(Driver(name, surname, middle_name, age, id))

    def get_taxi(self):
        return self.__car_model, self.__query_token, self.__driverList
