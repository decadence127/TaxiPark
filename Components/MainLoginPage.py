
from json import encoder
import re
import socket
from tkinter import *
import tkinter.messagebox as box
import json


HEADER = 64
PORT = 5040
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


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
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


master = Tk()
master.title("Taxipark")
width = 640
height = 480
screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
master.geometry("%dx%d+%d+%d" % (width, height, x, y))
master.resizable(0, 0)


LOGINUSER = StringVar()
LOGINPASS = StringVar()

REGUSER = StringVar()
REGPASS = StringVar()


def send_login_credentials(login, password, token):
    if login.get() == "" or login.get() == "":
        box.showerror("Error", "Enter User Name And Password")
        return
    else:
        tempLogin = login.get()
        tempPass = password.get()
        loginData = LoginModel(tempLogin, tempPass, token)
        JsonObject = loginData.toJSON()
        serialized = json.dumps(JsonObject)
        client.sendall(serialized.encode(FORMAT))


def RegistrationWindow(button):
    registrationWindow = Toplevel(master)
    registrationWindow.title("Registration")
    registrationWindow.geometry("480x280")
    registrationWindow.resizable(False, False)

    lbl_title.pack(side=TOP)
    lbl_username = Label(registrationWindow, text="Введите логин:",
                         font=('roboto', 14), bd=14)
    lbl_username.grid(row=1)

    lbl_password = Label(registrationWindow, text="Введите пароль:",
                         font=('roboto', 14), bd=14)

    lbl_password.grid(row=2)

    reg_user = Entry(registrationWindow, font=('roboto', 16),
                     textvariable=REGUSER, width=15)
    reg_user.grid(row=1, column=1)

    reg_pass = Entry(registrationWindow, font=('roboto', 16),
                     textvariable=REGPASS, width=15, show="*")
    reg_pass.grid(row=2, column=1)
    btn_register = Button(registrationWindow, font=('roboto', 16),
                          text="Зарегистрировать", command=lambda: send_login_credentials(REGUSER, REGPASS, 1))

    btn_register.grid(row=6, columnspan=2)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


TitleFrame = Frame(master, height=100, width=640, bd=1, relief=SOLID)
TitleFrame.pack(side=TOP)
LoginFrame = Frame(master)
LoginFrame.pack(side=TOP, pady=20)


lbl_title = Label(TitleFrame, text="Таксопарк",
                  font=('roboto', 18), bd=1, width=640)
lbl_title.pack()
lbl_username = Label(LoginFrame, text="Введите логин:",

                     font=('roboto', 14), bd=18)
lbl_username.grid(row=1)
lbl_password = Label(LoginFrame, text="Введите пароль:",
                     font=('roboto', 14), bd=18)

lbl_password.grid(row=2)
lbl_result = Label(LoginFrame, text="", font=('arial', 18))
lbl_result.grid(row=5, columnspan=2)


user = Entry(LoginFrame, font=('roboto', 16),
             textvariable=LOGINUSER, width=15)
user.grid(row=1, column=1)
pass1 = Entry(LoginFrame, font=('roboto', 16),
              textvariable=LOGINPASS, width=15, show="*")
pass1.grid(row=2, column=1)
btn_register = Button(LoginFrame, font=('roboto', 16),
                      text="Зарегистрироваться", command=lambda: RegistrationWindow(btn_register))
btn_register.grid(row=6, columnspan=3, padx=180)

btn_login = Button(LoginFrame, font=('roboto', 16),
                   text="Войти", command=lambda: send_login_credentials(LOGINUSER, LOGINPASS, 0))

btn_login.grid(row=6, columnspan=1)


if __name__ == '__main__':
    master.mainloop()
