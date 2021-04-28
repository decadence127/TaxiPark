import psycopg2
import socket

HOST = '127.0.0.1'
PORT = 65432


def Database():
    global conn, cursor
    conn = psycopg2.connect(database="decadence", user="decadence",
                            password="12345", host="localhost", port="5432")
    cursor = conn.cursor()
    print("Database opened successfully")


def Register():
    Database()
    if REGUSER.get == "" or REGPASS.get() == "":
        lbl_result.config(
            text="Please complete the required field!", fg="orange")
    cursor.execute('SELECT * FROM public."user"')

    cursor.execute('INSERT INTO public."user" ("user", pass) VALUES (%s, %s)', (str(
        REGUSER.get()), str(REGPASS.get())))
    conn.commit()
    REGUSER.set("")
    REGPASS.set("")
    print("Successfully Created!")
    cursor.close()
    conn.close()


def Login():
    Database()
    cursor.execute('SELECT "user", pass, id FROM public."user"')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        if LOGINUSER.get() == row[0] and LOGINPASS.get() == row[1]:
            lbl_result.config(text="Successfully Entered!", fg="green")
            conn.commit()
            cursor.close()
            conn.close()
            break
        else:
            lbl_result.config(text="Incorrect credentials!", fg="red")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
