
import socket
from tkinter import *
import tkinter.messagebox as box

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)

print('Received', repr(data))


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
                          text="Register", command=Register)
    btn_register.grid(row=6, columnspan=2)


def Exit():
    result = tkMessageBox.askquestion(
        'System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        master.destroy()
        exit()


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
                   text="Login", command=Login)
btn_login.grid(row=6, columnspan=1)


# ========================================INITIALIZATION===================================
if __name__ == '__main__':
    master.mainloop()
