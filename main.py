import json
import psycopg2
import socket
import threading

HEADER = 64
FORMAT = 'utf-8'
PORT = 5040
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind(ADDR)
except socket.error as e:
    print(str(e))


def Database():

    global conn, cursor
    conn = psycopg2.connect(database="decadence", user="postgres",
                            password="12344321", host="localhost", port="5432")
    cursor = conn.cursor()
    print("Database opened successfully")


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    server.send(send_length)
    server.send(message)


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

        if(int(res["login_token"]) == 0):
            Login(res["login"], res["password"])

        elif(int(res["login_token"]) == 1):
            Register(res["login"], res["password"])

        else:
            print("Error")

    conn.close()


def Login(msg_name, msg_password):
    Database()
    cursor.execute('SELECT "user", pass, id FROM public."user"')
    rows = cursor.fetchall()
    valid = False
    for row in rows:
        print(row)
        if msg_name == row[0] and msg_password == row[1]:
            print('he is right')
            valid = True
            conn.commit()
            cursor.close()
            conn.close()
            break
        else:
            print("hes not right")
            valid = False

    if valid == True:
        accessGranted = "access_granted"
        message = accessGranted.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        server.send(send_length)
        server.send(message)
    else:
        accessGranted = "access_denied"
        message = accessGranted.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        server.send(send_length)
        server.send(message)


def Register(msg_login, msg_password):
    Database()
    cursor.execute('SELECT * FROM public."user"')

    cursor.execute('INSERT INTO public."user" ("user", pass) VALUES (%s, %s)',
                   (msg_login, str(msg_password)))
    conn.commit()
    print("Successfully Created!")
    cursor.close()
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("Server is starting...")

start()
