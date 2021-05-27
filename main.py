import json
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

        else:
            print("Error")

    conn.close()


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
