import socket
from tkinter import *
import tkinter.messagebox as box
import json
import re
from Components import classes

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


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
icon = PhotoImage(file='Components/icon.ico')
master.iconphoto(False, icon)

LOGINUSER = StringVar()
LOGINPASS = StringVar()

REGUSER = StringVar()
REGPASS = StringVar()

REGKEY = StringVar()

CARMODEL = StringVar()
DRIVERNAME = StringVar()
DRIVERSURNAME = StringVar()
DRIVERMIDDLENAME = StringVar()
DRIVERAGE = StringVar()

BALANCE = StringVar()
CURBALANCE = 0.0


def SendCarQuery(token, carmodel, drivername, driversurname, drivermiddlename, driverage):
    tempCarmodel = carmodel.get()
    tempDrivername = drivername.get()
    tempDriverSurname = driversurname.get()
    tempDriverMiddleName = drivermiddlename.get()
    tempDriverAge = driverage.get()
    carObject = classes.TaxiModel(
        tempCarmodel, 6, tempDrivername, tempDriverSurname, tempDriverMiddleName, tempDriverAge)
    JsonObject = carObject.toJSON()
    serialized = json.dumps(JsonObject)
    client.sendall(serialized.encode(FORMAT))
    if token == 0:
        answer_length = client.recv(HEADER).decode(FORMAT)
        answer = client.recv(int(answer_length))
        answer = answer.decode(FORMAT)
        if str(answer) == "car_added":
            box.showinfo("Успех!", "Автомобиль был успешно добавлен")
        elif str(answer) == "car_not_added":
            box.showerror("Ошибка!",
                          "Автомобиль не удалось добавить")


def SendQuery(login, password, token, secret_key):
    if login.get() == "" or login.get() == "":
        box.showerror("Ошибка", "Поля не должны быть пустыми ")
        return
    else:
        tempLogin = login.get()
        tempPass = password.get()
        tempKey = secret_key.get()
        loginData = classes.QueryModel(tempLogin, tempPass, tempKey, token)
        JsonObject = loginData.toJSON()
        serialized = json.dumps(JsonObject)
        client.sendall(serialized.encode(FORMAT))
        if token == 0:
            received_answer = client.recv(1024).decode(FORMAT)
            deserialized = json.loads(received_answer)
            res = json.loads(deserialized)
            if str(res["answer_message"]) == "access_granted":
                balance = 0.0
                balance = res["balance"]
                CURBALANCE = res["balance"]
                DashBoardWindow(balance)
            elif str(res["answer_message"]) == "access_denied":
                box.showerror("Данные были введены неверно",
                              "Попробуйте снова или зарегистрируйтесь")
                LoginPanel()
            elif str(res["answer_message"]) == "access_granted_admin":
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


def RequestDataList(token):
    if token == 0:
        tempList = []
        emptyRequest = classes.QueryModel("", "", "", 3)
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
    elif token == 1:
        tempList = []
        emptyRequest = classes.QueryModel("", "", "", 5)
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


def LoginPanel():

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
                        text="Зарегистрироваться", command=lambda: [RegistrationWindow(reg_button), LOGINUSER.set(""), LOGINPASS.set(""), REGPASS.set(""), REGKEY.set("")])
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
        "WM_DELETE_WINDOW", lambda: deleteWindow(button))
    lbl_checkbutton = Checkbutton(
        registrationWindow, text="Администратор", command=lambda: [AdminRegistrationWindow(button), registrationWindow.destroy(), REGPASS.set(""), REGUSER.set("")])
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


def AdminRegistrationWindow(button):
    global registrationAdminWindow
    registrationAdminWindow = Toplevel(master)
    registrationAdminWindow.title("Registration Admin panel")
    registrationAdminWindow.geometry("520x280")
    registrationAdminWindow.resizable(False, False)
    registrationAdminWindow.iconphoto(False, icon)
    registrationAdminWindow.protocol(
        "WM_DELETE_WINDOW", lambda: deleteAdminWindow(button))
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


def deleteAdminWindow(button):
    registrationAdminWindow.destroy()
    button["state"] = 'normal'


def deleteWindow(button):
    registrationWindow.destroy()
    button["state"] = 'normal'


def deleteBalanceFrame(button):
    balanceFrame.destroy()
    dashboardTitleFrame.destroy()
    dashboardFrame.destroy()
    DashBoardWindow(CURBALANCE)
    button["state"] = 'normal'


def deleteCarWindow(button):
    carAddingWindow.destroy()
    button["state"] = 'normal'


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
    btn_usershandler = Button(adminDashboardFrame, text="Пользователи", font=(
        'Arial', 14), command=lambda: [UsersHandlerWindow(), adminDashboardTitleFrame.destroy(), adminDashboardFrame.destroy()])
    btn_usershandler.grid(row=2, column=0, sticky=W, padx=80, pady=10)
    btn_cars = Button(adminDashboardFrame, text="Автомобили", font=('Arial', 14), command=lambda: [
                      adminDashboardFrame.destroy(), adminDashboardTitleFrame.destroy(), CarsHandlerWindow()])
    btn_cars.grid(row=3, column=0, sticky=W, padx=80, pady=10)


def CarsHandlerWindow():
    tempCarList = []
    tempCarList = RequestDataList(1)
    sortedList = sorted(tempCarList, key=lambda x: x[0])
    print(sortedList)
    print(sortedList[0][0])
    handlerTitleFrame = Frame(
        master, height=100, width=640, bd=1, relief=SOLID)
    handlerTitleFrame.pack(side=TOP)
    lbl_title = Label(handlerTitleFrame, text="Меню автомобилей", font=(
        'courier', 14), bd=1, width=640)
    lbl_title.pack()

    carHandlerWindow = Frame(master)
    carHandlerWindow.pack(side=TOP)
    text = Listbox(carHandlerWindow, width=640, bd=1, relief=SOLID)
    for i in sortedList:
        text.insert(END, "id: " + str(i[0]) + ". Модель авто: " +
                    str(i[1]) + " ФИО Водителя: " + str(i[3]) + " " + str(i[2]) + " " + str(i[4]))
    text.pack(side=TOP, pady=20)
    del_btn = Button(carHandlerWindow, text="Удалить",
                     font=('Arial', 14), command=lambda: DeleteSelectedObject(text, tempCarList, 1))
    del_btn.pack(side=LEFT, pady=10, padx=20)
    return_btn = Button(carHandlerWindow, text="Вернуться",
                        font=('Arial', 14), command=lambda: [carHandlerWindow.destroy(), handlerTitleFrame.destroy(), AdministratorDashboard()])
    return_btn.pack(side=LEFT, pady=10, padx=20)
    refresh_btn = Button(carHandlerWindow, text="Обновить",
                         font=('Arial', 14), command=lambda: [carHandlerWindow.destroy(), handlerTitleFrame.destroy(), CarsHandlerWindow()])
    refresh_btn.pack(side=LEFT, pady=10, padx=20)
    adduser_btn = Button(carHandlerWindow, text="Добавить", font=(
        'Arial', 14), command=lambda: CarAdditionWindow(adduser_btn))
    adduser_btn.pack(side=LEFT, pady=10, padx=20)


def CarAdditionWindow(button):
    global carAddingWindow
    carAddingWindow = Toplevel(master)
    carAddingWindow.title("Добавить машину")
    carAddingWindow.geometry("640x520")
    carAddingWindow.resizable(False, False)
    carAddingWindow.iconphoto(False, icon)
    button["state"] = 'disabled'
    carAddingWindow.protocol(
        "WM_DELETE_WINDOW", lambda: deleteCarWindow(button))

    lbl_carmodel = Label(carAddingWindow, text="Введите марку авто:",
                         font=('courier', 14), bd=14)
    lbl_carmodel.grid(row=1)

    lbl_driverName = Label(carAddingWindow, text="Введите имя водителя:",
                           font=('courier', 14), bd=14)

    lbl_driverName.grid(row=2)

    lbl_driverSurname = Label(carAddingWindow, text="Введите фамилию водителя:",
                              font=('courier', 14), bd=14)

    lbl_driverSurname.grid(row=3)

    lbl_driverMidName = Label(carAddingWindow, text="Введите отчество водителя:",
                              font=('courier', 14), bd=14)

    lbl_driverMidName.grid(row=4)

    lbl_driverAge = Label(carAddingWindow, text="Введите возраст водителя:",
                          font=('courier', 14), bd=14)

    lbl_driverAge.grid(row=5)

    carmodel_entr = Entry(carAddingWindow, font=('verdana', 16),
                          textvariable=CARMODEL, width=15)
    carmodel_entr.grid(row=1, column=1)

    driverName_entr = Entry(carAddingWindow, font=('verdana', 16),
                            textvariable=DRIVERNAME, width=15)
    driverName_entr.grid(row=2, column=1)

    driverSurname_entr = Entry(carAddingWindow, font=('verdana', 16),
                               textvariable=DRIVERSURNAME, width=15)
    driverSurname_entr.grid(row=3, column=1)

    driverMidName_entr = Entry(carAddingWindow, font=('verdana', 16),
                               textvariable=DRIVERMIDDLENAME, width=15)
    driverMidName_entr.grid(row=4, column=1)

    driverAge_entr = Entry(carAddingWindow, font=('verdana', 16),
                           textvariable=DRIVERAGE, width=15)
    driverAge_entr.grid(row=5, column=1)

    btn_addition = Button(carAddingWindow, font=('arial', 16),
                          text="Добавить", command=lambda: NumberValidation())
    btn_addition.grid(row=6, columnspan=2)


def NumberValidation():
    Item1 = DRIVERAGE.get()
    if Item1.isdigit():
        SendCarQuery(0, CARMODEL, DRIVERNAME, DRIVERSURNAME,
                     DRIVERMIDDLENAME, DRIVERAGE)
        return True
    else:
        box.showerror(
            "Ошибка!", "Вы можете ввести только число в поле возраст")
        DRIVERAGE.set("")
        return False


def DashBoardWindow(balance):
    global dashboardFrame, dashboardTitleFrame
    dashboardTitleFrame = Frame(
        master, height=100, width=640, bd=1, relief=SOLID)
    dashboardTitleFrame.pack(side=TOP)

    dashboardFrame = Frame(master)
    dashboardFrame.pack(side=TOP, pady=20)

    lbl_title = Label(dashboardTitleFrame, text=f"Добро пожаловать, {LOGINUSER.get()}!",
                      font=('courier', 14), bd=1, width=640)
    lbl_title.pack()

    lbl_balance = Label(dashboardTitleFrame,
                        text=f"Ваш баланс, {balance} руб.", font=('courier', 14), bd=1)
    lbl_balance.pack()
    btn_add_balance = Button(dashboardFrame, text="Пополнить баланс", font=(
        'Arial', 14), command=lambda: [BalanceAddition(btn_add_balance)])
    btn_add_balance.pack(side=LEFT, pady=10, padx=20)
    refresh_balance_btn = Button(dashboardFrame, text="Обновить",
                                 font=('Arial', 14), command=lambda: [dashboardTitleFrame.destroy(), dashboardFrame.destroy(), DashBoardWindow(CURBALANCE)])
    refresh_balance_btn.pack(side=LEFT, pady=10, padx=20)


def BalanceAddition(button):
    global balanceFrame
    button["state"] = 'disabled'
    balanceFrame = Toplevel(master)
    balanceFrame.title("Пополнение баланса")
    balanceFrame.geometry("520x280")
    balanceFrame.resizable(False, False)
    balanceFrame.iconphoto(False, icon)
    balanceFrame.protocol(
        "WM_DELETE_WINDOW", lambda: deleteBalanceFrame(button))

    lbl_balance = Label(balanceFrame, text="Баланс: ", font=('Arial', 14))
    lbl_balance.grid(row=2)

    entr_balance = Entry(balanceFrame, font=(
        'verdana', 14), textvariable=BALANCE, width=15)
    entr_balance.grid(row=2, column=1)
    btn_balance = Button(balanceFrame, text="Пополнить", font=('Arial', 14),
                         command=lambda: [SendBalanceQuery(BALANCE)])
    btn_balance.grid(row=3, column=1, pady=20, padx=20)
    return_btn = Button(balanceFrame, text="Вернуться",
                        font=('Arial', 14), command=lambda: [balanceFrame.destroy(), balanceFrame.destroy()])
    return_btn.grid(row=3, column=2, pady=20, padx=20)


def SendBalanceQuery(balance):
    if balance.get() == "":
        box.showerror("Ошибка", "Поля не должны быть пустыми ")
        return
    else:
        tempBalance = balance.get()
        login = LOGINUSER.get()
        tempBalanceData = classes.QueryModel(
            login, "", "", 8,  float(tempBalance))

        JsonObject = tempBalanceData.toJSON()
        serialized = json.dumps(JsonObject)
        client.sendall(serialized.encode(FORMAT))

        received_answer = client.recv(1024).decode(FORMAT)
        print(received_answer)
        deserialized = json.loads(received_answer)
        res = json.loads(deserialized)
        if str(res["answer_message"]) == "balance_changed":
            box.showinfo("Успех", "Ваш баланс был успешно пополнен")
            CURBALANCE = float(res["balance"]) + BALANCE
            print(balance)
        elif str(res["answer_message"]) == "balance_not_changed":
            box.showerror("Ошибка", "При пополнении баланса возникла ошибка")
    return CURBALANCE


def UsersHandlerWindow():
    tempList = []
    tempList = RequestDataList(0)
    sortedList = sorted(tempList, key=lambda x: x[2])
    handlerTitleFrame = Frame(
        master, height=100, width=640, bd=1, relief=SOLID)
    handlerTitleFrame.pack(side=TOP)
    lbl_title = Label(handlerTitleFrame, text="Меню пользователей", font=(
        'courier', 14), bd=1, width=640)
    lbl_title.pack()

    userHandlerWindow = Frame(master)
    userHandlerWindow.pack(side=TOP)
    text = Listbox(userHandlerWindow, width=640, bd=1, relief=SOLID)
    for i in sortedList:
        textPermission = "Администратор" if i[3] == 1 else "Пользователь"
        text.insert(
            END, "id: " + str(i[2]) + ". Логин: " + i[0] + " Права доступа: " + textPermission + " Баланс: " + str(i[4]) + " руб.")
    text.pack(side=TOP, pady=20)

    del_btn = Button(userHandlerWindow, text="Удалить",
                     font=('Arial', 14), command=lambda: DeleteSelectedObject(text, sortedList, 0))
    del_btn.pack(side=LEFT, pady=10, padx=20)
    return_btn = Button(userHandlerWindow, text="Вернуться",
                        font=('Arial', 14), command=lambda: [userHandlerWindow.destroy(), handlerTitleFrame.destroy(), AdministratorDashboard()])
    return_btn.pack(side=LEFT, pady=10, padx=20)
    refresh_btn = Button(userHandlerWindow, text="Обновить",
                         font=('Arial', 14), command=lambda: [userHandlerWindow.destroy(), handlerTitleFrame.destroy(), UsersHandlerWindow()])
    refresh_btn.pack(side=LEFT, pady=10, padx=20)
    adduser_btn = Button(userHandlerWindow, text="Добавить", font=(
        'Arial', 14), command=lambda: RegistrationWindow(adduser_btn))
    adduser_btn.pack(side=LEFT, pady=10, padx=20)


def DeleteSelectedObject(text, tempList, token):
    if token == 0:
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
                    delObjectData = classes.QueryModel(
                        sortedList[list_index][0], sortedList[list_index][1], "", 4)
                    JsonObject = delObjectData.toJSON()
                    serialized = json.dumps(JsonObject)
                    client.sendall(serialized.encode(FORMAT))
                    del_answer_length = client.recv(HEADER).decode(FORMAT)
                    del_answer = client.recv(int(del_answer_length))
                    del_answer = del_answer.decode(FORMAT)
                    if str(del_answer == "successfully_deleted"):
                        box.showinfo(
                            "Успех!", "Вы успешно удалили пользователя!")
                        text.delete(i)
                    elif str(del_answer == "failed_deletion"):
                        box.showerror(
                            "Ошибка!", "Не удалось удалить пользователя!")
                    else:
                        box.showerror("Ошибка!", "Неизвестная ошибка!")
            else:
                box.showerror(
                    "Ошибка!", "Не удалось отправить данные на сервер!")
    elif token == 1:
        tempStr = ""
        sortedList = sorted(tempList, key=lambda x: x[0])
        print(sortedList)
        for i in text.curselection():
            tempStr = text.get(i)
            print(tempStr)
            regex_id = re.search('(?<=: )\w+', tempStr)
            id = int(regex_id.group(0))
            for list_index, i in enumerate(sortedList):
                if id == i[0]:
                    delObjectData = classes.TaxiModel(
                        sortedList[list_index][1], 7, sortedList[list_index][2], sortedList[list_index][3], sortedList[list_index][4], sortedList[list_index][5])
                    JsonObject = delObjectData.toJSON()
                    serialized = json.dumps(JsonObject)
                    client.sendall(serialized.encode(FORMAT))
                    del_answer_length = client.recv(HEADER).decode(FORMAT)
                    del_answer = client.recv(int(del_answer_length))
                    del_answer = del_answer.decode(FORMAT)
                    if str(del_answer == "car_successfully_deleted"):
                        box.showinfo(
                            "Успех!", "Вы успешно удалили автомобиль!")
                        text.delete(i)
                    elif str(del_answer == "failed_car_deletion"):
                        box.showerror(
                            "Ошибка!", "Не удалось удалить автомобиль!")
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