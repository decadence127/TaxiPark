import json
import random
from re import A
import psycopg2
import socket
import threading
from Components.classes import AnswerModel

HEADER = 64
FORMAT = 'utf-8'
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind(ADDR)
except socket.error as e:
    print(str(e))


def Database():

    global con, cursor
    con = psycopg2.connect(database="decadence", user="postgres",
                           password="12344321", host="localhost", port="5432")
    cursor = con.cursor()
    print("Database opened successfully")


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)


def deletionQuery(msg_name):
    Database()
    print(str(msg_name))
    try:
        cursor.execute(
            f"DELETE FROM public.\"user\" WHERE \"user\" = '{msg_name}'")
        con.commit()
        cursor.close()
        con.close()
        send("successfully_deleted")
    except (Exception, psycopg2.DatabaseError) as e:
        send("failed_deletion")
        print(e)
    finally:
        if con is not None:
            con.close()


def CarDeletionQuery(msg_name, msg_driverdata):
    Database()
    try:
        cursor.execute(
            f"DELETE FROM public.taxi WHERE \"model\" ='{msg_name}' AND \"driverName\" = '{msg_driverdata}'")
        con.commit()
        cursor.close()
        con.close()
        send("car_successfully_deleted")
    except (Exception, psycopg2.DatabaseError) as e:
        send("failed_car_deletion")
        print(e)
    finally:
        if con is not None:
            con.close()


def databaseDataRequest(token):
    if token == 0:
        Database()
        database_data = []
        cursor.execute(
            'SELECT "user", pass, id, permission, balance FROM public."user"')
        rows = cursor.fetchall()
        database_data.append(rows)
        print(database_data)
        print(type(database_data))
        data = json.dumps(database_data)
        sent_data = json.dumps(data)
        conn.sendall(sent_data.encode(FORMAT))

        con.commit()
        cursor.close()
        con.close()
    if token == 1:
        Database()
        database_data = []
        cursor.execute(
            'SELECT id, model, "driverName", "driverSurname", "driverMidName", "driverAge" FROM public.taxi;')
        rows = cursor.fetchall()
        database_data.append(rows)
        print(database_data)
        print(type(database_data))
        data = json.dumps(database_data)
        sent_data = json.dumps(data)
        conn.sendall(sent_data.encode(FORMAT))

        con.commit()
        cursor.close()
        con.close()


def MethodCalculator(projectData):
    if len(projectData) == 2:
        calc_moneyGain = projectData[0]["moneyGain"]
        calc_moneyLoss = projectData[0]["moneyLoss"]
        calc_negativeProb = projectData[0]["negativeProb"]
        calc_positiveProb = projectData[0]["positiveProb"]

        calc_moneyGain1 = projectData[1]["moneyGain"]
        calc_moneyLoss1 = projectData[1]["moneyLoss"]
        calc_negativeProb1 = projectData[1]["negativeProb"]
        calc_positiveProb1 = projectData[1]["positiveProb"]

        total_result1 = (float(calc_positiveProb) * float(calc_moneyGain)) + \
            (float(calc_negativeProb) * (0.0-float(calc_moneyLoss)))
        print(total_result1)
        total_result2 = (float(calc_positiveProb1) * float(calc_moneyGain1)) + \
            (float(calc_negativeProb1) * (0.0-float(calc_moneyLoss1)))
        print(total_result2)

        if total_result1 > total_result2:
            print(
                f"Наиболее целесообразно выбрать стратегию 1, т.е. расширить охват города на юг, стратегию 2 можно отбросить. ОДО наилучшего решения равна {total_result1} руб.")
        elif total_result2 > total_result1:
            print(
                f"Наиболее целесообразно выбрать стратегию 2, т.е. расширить охват города на север, а стратегию 1 можно отбросить. ОДО наилучшего решения равна {total_result2} руб.")
        else:
            print("Коэффиценты проектов равны")

        answer = AnswerModel("method_created")
        JsonObject = answer.toJSON()
        serialized = json.dumps(JsonObject)
        conn.sendall(serialized.encode(FORMAT))
    elif len(projectData) == 3:
        calc_moneyGain = projectData[0]["moneyGain"]
        calc_moneyLoss = projectData[0]["moneyLoss"]
        calc_negativeProb = projectData[0]["negativeProb"]
        calc_positiveProb = projectData[0]["positiveProb"]

        calc_moneyGain1 = projectData[1]["moneyGain"]
        calc_moneyLoss1 = projectData[1]["moneyLoss"]
        calc_negativeProb1 = projectData[1]["negativeProb"]
        calc_positiveProb1 = projectData[1]["positiveProb"]

        calc_moneyGain2 = projectData[2]["moneyGain"]
        calc_moneyLoss2 = projectData[2]["moneyLoss"]
        calc_negativeProb2 = projectData[2]["negativeProb"]
        calc_positiveProb2 = projectData[2]["positiveProb"]

        total_result1 = (float(calc_positiveProb) * float(calc_moneyGain)) + \
            (float(calc_negativeProb) * (0.0-float(calc_moneyLoss)))
        print(total_result1)
        total_result2 = (float(calc_positiveProb1) * float(calc_moneyGain1)) + \
            (float(calc_negativeProb1) * (0.0-float(calc_moneyLoss1)))
        print(total_result2)
        total_result3 = (float(calc_positiveProb2) * float(calc_moneyGain2)) + \
            (float(calc_negativeProb2) * (0.0-float(calc_moneyLoss2)))
        print(total_result3)

        if total_result1 > total_result2 and total_result1 > total_result3:
            print(
                f"Наиболее целесообразно выбрать стратегию 1, т.е. расширить охват города на юг, а стратегии 2 и 3 можно отбросить. ОДО наилучшего решения равна {total_result1} руб.")
            answer = AnswerModel("method1_best")
            JsonObject = answer.toJSON()
            serialized = json.dumps(JsonObject)
            conn.sendall(serialized.encode(FORMAT))
        elif total_result2 > total_result1 and total_result2 > total_result3:
            print(
                f"Наиболее целесообразно выбрать стратегию 2, т.е. расширить охват города на север, а стратегии 1 и 3 можно отбросить. ОДО наилучшего решения равна {total_result2} руб.")
            answer = AnswerModel("method2_best")
            JsonObject = answer.toJSON()
            serialized = json.dumps(JsonObject)
            conn.sendall(serialized.encode(FORMAT))
        elif total_result3 > total_result1 and total_result3 > total_result2:
            print(
                f"Наиболее целесообразно выбрать стратегию 3, т.е. расширить охват за городом, а стратегии 1 и 2 можно отбросить. ОДО наилучшего решения равна {total_result3} руб.")
            answer = AnswerModel("method3_best")
            JsonObject = answer.toJSON()
            serialized = json.dumps(JsonObject)
            conn.sendall(serialized.encode(FORMAT))
        else:
            print("Коэффиценты проектов равны")


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:

        received = conn.recv(1024)
        received = received.decode(FORMAT)
        try:
            deserialized = json.loads(received)
        except (TypeError, ValueError) as e:
            raise Exception('Data received was not in JSON format')
        print("obj:", deserialized)
        res = json.loads(deserialized)

        if(int(res["query_token"]) == 0):
            Login(res["login"], res["password"])
        elif(int(res["query_token"]) == 1):
            Register(res["login"], res["password"])
        elif(int(res["query_token"] == 2)):
            RegisterAdmin(res["login"], res["password"], res["secret_key"])
        elif(int(res["query_token"] == 3)):
            databaseDataRequest(0)
        elif(int(res["query_token"] == 4)):
            deletionQuery(res["login"])
        elif(int(res["query_token"] == 5)):
            databaseDataRequest(1)
        elif(int(res["query_token"] == 6)):
            CarAddition(res["_TaxiModel__car_model"], res["_TaxiModel__driverData"]["_Driver__name"],
                        res["_TaxiModel__driverData"]["_Driver__surname"], res["_TaxiModel__driverData"]["_Driver__middle_name"], res["_TaxiModel__driverData"]["_Driver__age"])
        elif(int(res["query_token"] == 7)):
            CarDeletionQuery(res["_TaxiModel__car_model"],
                             res["_TaxiModel__driverData"]["_Driver__name"])
        elif(int(res["query_token"] == 8)):
            BalanceAdditionQuery(res["login"], res["balance"])
        elif(int(res["query_token"] == 9)):
            MethodCalculator(res["projectData"])
        elif(int(res["query_token"] == 10)):
            OrderedTaxiCalculator(
                res["login"], res["balance"])
        elif(int(res["query_token"] == 11)):
            CarSearchDatabaseQuery(res["login"])
        elif(int(res["query_token"] == 12)):
            UserSearchDatabaseQuery(res["login"])

        else:
            print("Error")

    conn.close()


def UserSearchDatabaseQuery(msg_string):
    Database()
    database_data = []
    cursor.execute(
        f'SELECT "user", pass, id, permission, balance FROM public."user" WHERE "user" ILIKE \'%{str(msg_string)}%\'')
    rows = cursor.fetchall()
    database_data.append(rows)
    print(database_data)
    print(type(database_data))
    data = json.dumps(database_data)
    sent_data = json.dumps(data)
    conn.sendall(sent_data.encode(FORMAT))

    con.commit()
    cursor.close()
    con.close()


def CarSearchDatabaseQuery(msg_string):
    Database()
    database_data = []
    cursor.execute(
        f'SELECT id, model, "driverName", "driverSurname", "driverMidName", "driverAge" FROM public.taxi WHERE "driverName" ILIKE \'%{str(msg_string)}%\' or model ILIKE \'%{str(msg_string)}%\' or "driverSurname" ILIKE \'%{str(msg_string)}%\' or "driverMidName" ILIKE \'%{str(msg_string)}%\'')
    rows = cursor.fetchall()
    database_data.append(rows)
    print(database_data)
    print(type(database_data))
    data = json.dumps(database_data)
    sent_data = json.dumps(data)
    conn.sendall(sent_data.encode(FORMAT))

    con.commit()
    cursor.close()
    con.close()


def OrderedTaxiCalculator(msg_name, msg_balance):
    const_price = 5
    driver_distance = random.uniform(100.0, 5500.0)
    driver_time_delay = (driver_distance / 1000.0) * 5
    ride_distance = random.uniform(500.0, 12000.0)
    ride_cost = const_price + ((ride_distance / 1000.0) * 5)
    Database()
    cursor.execute('SELECT "user", pass, id, balance FROM public."user"')
    rows = cursor.fetchall()
    order_valid = False
    for row in rows:
        print(row)
        if msg_name == row[0] and float(msg_balance) > 0 and float(msg_balance) <= row[3]:
            cursor.execute(
                f'UPDATE public."user" SET balance= (balance -\'{ride_cost}\') WHERE "user" = \'{msg_name}\'')
            con.commit()
            cursor.close()
            con.close()
            order_valid = True
            break
        else:
            order_valid = False

    if order_valid == True:
        balance = row[3]
        answer = AnswerModel("ordered_successfully",
                             balance, driver_time_delay, ride_cost)
        JsonObject = answer.toJSON()
        serialized = json.dumps(JsonObject)
        conn.sendall(serialized.encode(FORMAT))
    elif order_valid == False:
        answer = AnswerModel("order_denied")
        JsonObject = answer.toJSON()
        serialized = json.dumps(JsonObject)
        conn.sendall(serialized.encode(FORMAT))


def BalanceAdditionQuery(msg_name, msg_balance):
    Database()
    cursor.execute('SELECT "user", pass, id, balance FROM public."user"')
    rows = cursor.fetchall()
    valid = False
    for row in rows:
        print(row)
        if msg_name == row[0] and float(msg_balance) > 0:
            cursor.execute(
                f'UPDATE public."user" SET balance= (balance +\'{msg_balance}\') WHERE "user" = \'{msg_name}\'')
            con.commit()
            cursor.close()
            con.close()
            valid = True
            break
        else:
            valid = False

    if valid == True:
        balance = row[3]
        answer = AnswerModel("balance_changed", balance)
        JsonObject = answer.toJSON()
        serialized = json.dumps(JsonObject)
        conn.sendall(serialized.encode(FORMAT))
    elif valid == False:
        answer = AnswerModel("balance_not_changed")
        JsonObject = answer.toJSON()
        serialized = json.dumps(JsonObject)
        conn.sendall(serialized.encode(FORMAT))


def RegisterAdmin(msg_name, msg_password, msg_key):
    Database()
    secret_key = "superuser"
    if msg_key == secret_key:
        cursor.execute(
            'SELECT "user", pass, id, permission FROM public."user"')
        rows = cursor.fetchall()
        for row in rows:
            print(row)
            if msg_name == row[0]:
                con.commit()
                cursor.close()
                con.close()
                send("validation_error")
                return

        cursor.execute('SELECT * FROM public."user"')
        cursor.execute(
            f'INSERT INTO public."user" ("user", pass, permission, balance) VALUES (\'{msg_name}\', \'{str(msg_password)}\', 1, 0.0)')
        con.commit()
        print("Successfully Created!")
        send("good_key")
        cursor.close()
        con.close()
    else:
        send("bad_key")


def Login(msg_name, msg_password):
    Database()
    cursor.execute(
        'SELECT "user", pass, id, permission, balance FROM public."user"')
    rows = cursor.fetchall()
    valid = False
    permission = 0
    for row in rows:
        print(row)
        if msg_name == row[0] and msg_password == row[1]:
            permission = row[3]
            print('he is right')
            valid = True
            con.commit()
            cursor.close()
            con.close()
            break
        else:
            print("hes not right")
            valid = False

    if permission == 0:
        if valid == True:
            balance = row[4]
            answer = AnswerModel("access_granted", balance, permission)
            JsonObject = answer.toJSON()
            serialized = json.dumps(JsonObject)
            conn.sendall(serialized.encode(FORMAT))
        else:
            answer = AnswerModel("access_denied")
            JsonObject = answer.toJSON()
            serialized = json.dumps(JsonObject)
            conn.sendall(serialized.encode(FORMAT))
    elif permission == 1:
        if valid == True:
            answer = AnswerModel("access_granted_admin")
            JsonObject = answer.toJSON()
            serialized = json.dumps(JsonObject)
            conn.sendall(serialized.encode(FORMAT))
        else:
            answer = AnswerModel("access_denied")
            JsonObject = answer.toJSON()
            serialized = json.dumps(JsonObject)
            conn.sendall(serialized.encode(FORMAT))


def Register(msg_login, msg_password):
    Database()
    cursor.execute('SELECT "user", pass, id FROM public."user"')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        if msg_login == row[0]:
            con.commit()
            cursor.close()
            con.close()
            send("validation_error")
            return

    cursor.execute('SELECT * FROM public."user"')
    cursor.execute(
        f'INSERT INTO public."user" ("user", pass, permission, balance) VALUES (\'{msg_login}\', \'{str(msg_password)}\', 0, 0.0)')
    con.commit()
    print("Successfully Created!")
    send("reg_success")
    cursor.close()
    con.close()


def CarAddition(msg_model, msg_driver_name, msg_driversurname, msg_drivermiddle_name, msg_driverage):
    Database()
    cursor.execute(
        'SELECT id, model, "driverName", "driverSurname", "driverMidName", "driverAge" FROM public.taxi')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        if msg_model == row[0]:
            con.commit()
            cursor.close()
            con.close()
            send("car_not_added")
            return
    cursor.execute('SELECT * FROM public.taxi')
    cursor.execute(
        f'INSERT INTO public."taxi" (model, "driverName", "driverSurname", "driverMidName", "driverAge") VALUES (\'{str(msg_model)}\', \'{str(msg_driver_name)}\', \'{str(msg_driversurname)}\', \'{str(msg_drivermiddle_name)}\', \'{msg_driverage}\')')
    con.commit()
    print("Successfully Created!")
    send("car_added")
    cursor.close()
    con.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        global conn, addr
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("Server is starting...")

start()
