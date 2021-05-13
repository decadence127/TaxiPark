
import socket
from tkinter import *
import tkinter.messagebox as box

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


class Window(Toplevel):

    def __init__(self, master=None):
        super().__init__(master=master)


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


# =======================================VARIABLES=====================================
LOGINUSER = StringVar()
LOGINPASS = StringVar()

REGUSER = StringVar()
REGPASS = StringVar()

# =======================================METHODS=======================================


def RecieveMessage():
    msg_name_length = client.recv(HEADER).decode(FORMAT)
    if msg_name_length:
        msg_name_length = int(msg_name_length)
        msg_name = client.recv(msg_name_length).decode(FORMAT)


def RegistrationWindow(button):
    registrationWindow = Window()
    registrationWindow.title("Registration")
    registrationWindow.geometry("640x480")
    button.configure(state="disabled")

    lbl_title.pack()
    lbl_username = Label(registrationWindow, text="Username:",
                         font=('arial', 18), bd=18)
    lbl_username.grid(row=1)

    lbl_password = Label(registrationWindow, text="Password:",
                         font=('arial', 18), bd=18)
    lbl_password.grid(row=2)

    lbl_result = Label(registrationWindow, text="", font=('arial', 18))
    lbl_result.grid(row=5, columnspan=2)

    reg_user = Entry(registrationWindow, font=('arial', 20),
                     textvariable=REGUSER, width=15)
    reg_user.grid(row=1, column=1)

    pass2 = Entry(registrationWindow, font=('arial', 20),
                  textvariable=REGPASS, width=15, show="*")
    pass2.grid(row=2, column=1)

    btn_register = Button(registrationWindow, font=('arial', 20),
                          text="Register", command=send_login_credentials(REGUSER, REGPASS))
    btn_register.grid(row=6, columnspan=2)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def send_login_credentials(LOGINUSER, LOGINPASS):
    login = LOGINUSER.get()
    password = LOGINPASS.get()
    send(login)
    send(password)


# =====================================FRAMES====================================
TitleFrame = Frame(master, height=100, width=640, bd=1, relief=SOLID)
TitleFrame.pack(side=TOP)
LoginFrame = Frame(master)
LoginFrame.pack(side=TOP, pady=20)


lbl_title = Label(TitleFrame, text="Таксопарк",
                  font=('arial', 18), bd=1, width=640)
lbl_title.pack()
lbl_username = Label(LoginFrame, text="Username:",
                     font=('arial', 18), bd=18)
lbl_username.grid(row=1)
lbl_password = Label(LoginFrame, text="Password:",
                     font=('arial', 18), bd=18)
lbl_password.grid(row=2)
lbl_result = Label(LoginFrame, text="", font=('arial', 18))
lbl_result.grid(row=5, columnspan=2)


user = Entry(LoginFrame, font=('arial', 20),
             textvariable=LOGINUSER, width=15)
user.grid(row=1, column=1)
pass1 = Entry(LoginFrame, font=('arial', 20),
              textvariable=LOGINPASS, width=15, show="*")
pass1.grid(row=2, column=1)

btn_register = Button(LoginFrame, font=('arial', 20),
                      text="Register", command=lambda: RegistrationWindow(btn_register))
btn_register.grid(row=6, columnspan=2)

btn_login = Button(LoginFrame, font=('arial', 20),
                   text="Login", command=lambda: send_login_credentials(LOGINUSER, LOGINPASS))
btn_login.grid(row=6, columnspan=1)

RecieveMessage()

# async def AccessValidation():
#     access = RecieveMessage()
#     if access == "access_granted":
#         lbl_result.config("Ok", color="green")


# ========================================INITIALIZATION===================================
if __name__ == '__main__':
    master.mainloop()
