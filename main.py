import json
import psycopg2
import socket
import threading

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


def databaseDataRequest():
    Database()
    database_data = []
    cursor.execute('SELECT "user", pass, id, permission FROM public."user"')
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
            databaseDataRequest()
        elif(int(res["query_token"] == 4)):
            print(deserialized)
            deletionQuery(res["login"])

        else:
            print("Error")

    conn.close()


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
            f'INSERT INTO public."user" ("user", pass, permission) VALUES ({msg_name}, {str(msg_password)}, 1)')
        con.commit()
        print("Successfully Created!")
        send("good_key")
        cursor.close()
        con.close()
    else:
        send("bad_key")


def Login(msg_name, msg_password):
    Database()
    cursor.execute('SELECT "user", pass, id, permission FROM public."user"')
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
            accessGranted = "access_granted"
            send(accessGranted)
        else:
            accessGranted = "access_denied"
            send(accessGranted)
    elif permission == 1:
        if valid == True:
            accessGranted = "access_granted_admin"
            send(accessGranted)
        else:
            accessGranted = "access_denied"
            send(accessGranted)


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
        f'INSERT INTO public."user" ("user", pass, permission) VALUES ({msg_login}, {str(msg_password)}, 0)')
    con.commit()
    print("Successfully Created!")
    send("reg_success")
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
