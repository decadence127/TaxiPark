from json import encoder
import socket
from tkinter import *
import tkinter.messagebox as box
import json
import re

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


class QueryModel:
    login = ""
    password = ""
    query_token = 0
    secret_key = ""

    def __init__(self) -> None:
        pass

    def __init__(self, login, password, query_token):
        self.login = login
        self.password = password
        self.query_token = query_token

    def __init__(self, login, password, query_token, secret_key):
        self.login = login
        self.password = password
        self.query_token = query_token
        self.secret_key = secret_key

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
icon = PhotoImage(file='icon.ico')
master.iconphoto(False, icon)

LOGINUSER = StringVar()
LOGINPASS = StringVar()

REGUSER = StringVar()
REGPASS = StringVar()

REGKEY = StringVar()

DESERIALIZED_LIST = []


def recieveDataHandler():
    pass


def SendQuery(login, password, token, secret_key):
    if login.get() == "" or login.get() == "":
        box.showerror("Ошибка", "Поля не должны быть пустыми ")
        return
    else:
        tempLogin = login.get()
        tempPass = password.get()
        tempKey = secret_key.get()
        loginData = QueryModel(tempLogin, tempPass, token, tempKey)
        JsonObject = loginData.toJSON()
        serialized = json.dumps(JsonObject)
        client.sendall(serialized.encode(FORMAT))
        if token == 0:
            answer_length = client.recv(HEADER).decode(FORMAT)
            answer = client.recv(int(answer_length))
            answer = answer.decode(FORMAT)
            if str(answer) == "access_granted":
                DashBoardWindow()
            elif str(answer) == "access_denied":
                box.showerror("Данные были введены неверно",
                              "Попробуйте снова или зарегистрируйтесь")
                LoginPanel()
            elif str(answer) == "access_granted_admin":
                AdministratorDashboard()
        elif token == 1:
            reg_answer_length = client.recv(HEADER).decode(FORMAT)
            reg_answer = client.recv(int(reg_answer_length))
            reg_answer = reg_answer.decode(FORMAT)
            if str(reg_answer) == "reg_success":
                box.showinfo("Успех", "Пользователь успешно зарегистрирован")
            elif str(reg_answer) == "validation_error":
                box.showerror("Ошибка", "Такой пользователь уже существует!")
        elif token == 2:
            regadm_answer_length = client.recv(HEADER).decode(FORMAT)
            regadm_answer = client.recv(int(regadm_answer_length))
            regadm_answer = regadm_answer.decode(FORMAT)
            print(regadm_answer)
            if str(regadm_answer) == "bad_key":
                box.showerror(
                    "Ошибка", "Ключ не подходит! Вы не были зарегистрированы")
            elif str(regadm_answer) == "good_key":
                box.showinfo(
                    "Успех", "Вы были зарегистрированы как администратор!")
            elif str(regadm_answer) == "validation_error":
                box.showerror("Ошибка", "Такой пользователь уже существует")


def RequestDataList():
    tempList = []
    emptyRequest = QueryModel("", "", 3, "")
    JsonRequest = emptyRequest.toJSON()
    serializedRequest = json.dumps(JsonRequest)
    client.sendall(serializedRequest.encode(FORMAT))
    del_answer = client.recv(1024)
    del_answer = del_answer.decode(FORMAT)
    try:
        deserialized_list = json.loads(del_answer)
    except (TypeError, ValueError) as e:
        raise Exception('Data received was not in JSON format')
    res = json.loads(deserialized_list)
    print(type(res))
    tempList = res[0]
    return tempList


def AdminRegistrationWindow(button):
    global registrationAdminWindow
    registrationAdminWindow = Toplevel(master)
    registrationAdminWindow.title("Registration Admin panel")
    registrationAdminWindow.geometry("520x280")
    registrationAdminWindow.resizable(False, False)
    registrationAdminWindow.iconphoto(False, icon)
    registrationAdminWindow.protocol(
        "WM_DELETE_WINDOW", deleteAdminWindow)
    lbl_username = Label(registrationAdminWindow, text="Введите логин:",
                         font=('courier', 14), bd=14)
    lbl_username.grid(row=1)

    lbl_password = Label(registrationAdminWindow, text="Введите пароль:",
                         font=('courier', 14), bd=14)
    lbl_password.grid(row=2)

    reg_user = Entry(registrationAdminWindow, font=('verdana', 16),
                     textvariable=REGUSER, width=15)
    reg_user.grid(row=1, column=1)

    reg_pass = Entry(registrationAdminWindow, font=('verdana', 16),
                     textvariable=REGPASS, width=15, show="*")
    reg_pass.grid(row=2, column=1)
    lbl_keyword = Label(registrationAdminWindow, text="Введите секретный ключ:",
                        font=('courier', 14), bd=14)
    lbl_keyword.grid(row=3)
    reg_keyword = Entry(registrationAdminWindow, font=(
        'verdana', 16), textvariable=REGKEY, width=15)
    reg_keyword.grid(row=3, column=1)

    btn_register = Button(registrationAdminWindow, font=('arial', 16),
                          text="Зарегистрировать", command=lambda: SendQuery(REGUSER, REGPASS, 2, REGKEY))
    btn_register.grid(row=6, columnspan=2)


def deleteAdminWindow():
    registrationAdminWindow.destroy()
    reg_button["state"] = 'normal'


def deleteWindow():
    registrationWindow.destroy()
    reg_button["state"] = 'normal'


def LoginPanel():
    global reg_button
    TitleFrame = Frame(master, height=100, width=640, bd=1, relief=SOLID)
    TitleFrame.pack(side=TOP)
    LoginFrame = Frame(master)
    LoginFrame.pack(side=TOP, pady=20)

    lbl_title = Label(TitleFrame, text="Таксопарк",
                      font=('courier', 18), bd=1, width=640)
    lbl_title.pack()
    lbl_username = Label(LoginFrame, text="Введите логин:",

                         font=('courier', 14), bd=18)
    lbl_username.grid(row=1)
    lbl_password = Label(LoginFrame, text="Введите пароль:",
                         font=('courier', 14), bd=18)

    lbl_password.grid(row=2)
    lbl_result = Label(LoginFrame, text="", font=('arial', 18))
    lbl_result.grid(row=5, columnspan=2)

    user = Entry(LoginFrame, font=('verdana', 16),
                 textvariable=LOGINUSER, width=15)
    user.grid(row=1, column=1)
    pass1 = Entry(LoginFrame, font=('verdana', 16),
                  textvariable=LOGINPASS, width=15, show="*")
    pass1.grid(row=2, column=1)

    reg_button = Button(LoginFrame, font=('arial', 16),
                        text="Зарегистрироваться", command=lambda: RegistrationWindow(reg_button))
    reg_button.grid(row=6, columnspan=3, padx=180)

    btn_login = Button(LoginFrame, font=('arial', 16),
                       text="Войти", command=lambda: [SendQuery(LOGINUSER, LOGINPASS, 0, REGKEY), LoginFrame.destroy(), TitleFrame.destroy()])

    btn_login.grid(row=6, columnspan=1)


def RegistrationWindow(button):
    global registrationWindow
    registrationWindow = Toplevel(master)
    registrationWindow.title("Registration")
    registrationWindow.geometry("520x280")
    registrationWindow.resizable(False, False)
    registrationWindow.iconphoto(False, icon)
    button["state"] = 'disabled'
    registrationWindow.protocol(
        "WM_DELETE_WINDOW", deleteWindow)
    lbl_checkbutton = Checkbutton(
        registrationWindow, text="Администратор", command=lambda: [AdminRegistrationWindow(button), registrationWindow.destroy()])
    lbl_checkbutton.grid(row=4)

    lbl_username = Label(registrationWindow, text="Введите логин:",
                         font=('courier', 14), bd=14)
    lbl_username.grid(row=1)

    lbl_password = Label(registrationWindow, text="Введите пароль:",
                         font=('courier', 14), bd=14)

    lbl_password.grid(row=2)

    reg_user = Entry(registrationWindow, font=('verdana', 16),
                     textvariable=REGUSER, width=15)
    reg_user.grid(row=1, column=1)

    reg_pass = Entry(registrationWindow, font=('verdana', 16),
                     textvariable=REGPASS, width=15, show="*")
    reg_pass.grid(row=2, column=1)

    btn_register = Button(registrationWindow, font=('arial', 16),
                          text="Зарегистрировать", command=lambda: SendQuery(REGUSER, REGPASS, 1, REGKEY))
    btn_register.grid(row=6, columnspan=2)


def AdministratorDashboard():
    adminDashboardTitleFrame = Frame(
        master, height=100, width=640, bd=1, relief=SOLID)
    adminDashboardTitleFrame.pack(side=TOP)

    adminDashboardFrame = Frame(master)
    adminDashboardFrame.pack(pady=20)

    lbl_title = Label(adminDashboardTitleFrame, text=f"Добро пожаловать, {LOGINUSER.get()}, в панель администратора!",
                      font=('courier', 14), bd=1, width=640)
    lbl_title.pack()

    btn_logout = Button(adminDashboardFrame, text="Выйти", font=(
        'Arial', 14), command=lambda: [adminDashboardFrame.destroy(), adminDashboardTitleFrame.destroy(), LoginPanel()])
    btn_logout.grid(row=5, columnspan=2, padx=520)
    btn_adduser = Button(adminDashboardFrame, text="Добавить пользователя", font=(
        'Arial', 14), command=lambda: RegistrationWindow(btn_adduser))
    btn_adduser.grid(row=1, column=0, sticky=W, padx=80, pady=10)
    btn_deleteuser = Button(adminDashboardFrame, text="Удалить пользователя", font=(
        'Arial', 14), command=lambda: [DeletionWindow(), adminDashboardTitleFrame.destroy(), adminDashboardFrame.destroy()])
    btn_deleteuser.grid(row=2, column=0, sticky=W, padx=80, pady=10)


def DashBoardWindow():
    dashboardTitleFrame = Frame(
        master, height=100, width=640, bd=1, relief=SOLID)
    dashboardTitleFrame.pack(side=TOP)

    dashboardFrame = Frame(master)
    dashboardFrame.pack(side=TOP, pady=20)

    lbl_title = Label(dashboardTitleFrame, text=f"Добро пожаловать, {LOGINUSER.get()}!",
                      font=('courier', 14), bd=1, width=640)
    lbl_title.pack()


def DeletionWindow():
    tempList = []
    tempList = RequestDataList()
    sortedList = sorted(tempList, key=lambda x: x[2])
    deletionTitleFrame = Frame(
        master, height=100, width=640, bd=1, relief=SOLID)
    deletionTitleFrame.pack(side=TOP)
    lbl_title = Label(deletionTitleFrame, text="Меню удаления пользователя", font=(
        'courier', 14), bd=1, width=640)
    lbl_title.pack()

    deletionWindow = Frame(master)
    deletionWindow.pack(side=TOP)
    text = Listbox(deletionWindow, width=640, bd=1, relief=SOLID)
    for i in sortedList:
        textPermission = "Администратор" if i[3] == 1 else "Пользователь"
        text.insert(
            END, "id: " + str(i[2]) + ". Логин: " + i[0] + " Права доступа: " + textPermission)
    text.pack(side=TOP, pady=20)

    del_btn = Button(deletionWindow, text="Удалить",
                     font=('Arial', 14), command=lambda: DeleteSelectedObject(text, sortedList))
    del_btn.pack(side=LEFT, pady=10, padx=20)
    return_btn = Button(deletionWindow, text="Вернуться",
                        font=('Arial', 14), command=lambda: [deletionWindow.destroy(), deletionTitleFrame.destroy(), AdministratorDashboard()])
    return_btn.pack(side=LEFT, pady=10, padx=20)
    refresh_btn = Button(deletionWindow, text="Обновить",
                         font=('Arial', 14), command=lambda: [deletionWindow.destroy(), deletionTitleFrame.destroy(), DeletionWindow()])
    refresh_btn.pack(side=LEFT, pady=10, padx=20)


def DeleteSelectedObject(text, tempList):
    tempStr = ""
    sortedList = sorted(tempList, key=lambda x: x[2])
    print(sortedList)
    for i in text.curselection():
        tempStr = text.get(i)
        print(tempStr)
        regex_id = re.search('(?<=: )\w+', tempStr)
        id = int(regex_id.group(0))
        for list_index, i in enumerate(sortedList):
            if id == i[2]:
                delObjectData = QueryModel(
                    sortedList[list_index][0], sortedList[list_index][1], 4, "")
                JsonObject = delObjectData.toJSON()
                serialized = json.dumps(JsonObject)
                client.sendall(serialized.encode(FORMAT))
                del_answer_length = client.recv(HEADER).decode(FORMAT)
                del_answer = client.recv(int(del_answer_length))
                del_answer = del_answer.decode(FORMAT)
                if str(del_answer == "successfully_deleted"):
                    box.showinfo("Успех!", "Вы успешно удалили пользователя!")
                    text.delete(i)
                elif str(del_answer == "failed_deletion"):
                    box.showerror(
                        "Ошибка!", "Не удалось удалить пользователя!")
                else:
                    box.showerror("Ошибка!", "Неизвестная ошибка!")
        else:
            box.showerror(
                "Ошибка!", "Не удалось отправить данные на сервер!")


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


LoginPanel()


if __name__ == '__main__':
    master.mainloop()
