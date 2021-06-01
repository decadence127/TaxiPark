import socket
from tkinter import *
import tkinter.messagebox as box
import json
from tkinter import ttk
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

METHODPOSITIVE = StringVar()
METHODNEGATIVE = StringVar()
METHODMONEYLOSS = StringVar()
METHODMONEYGAIN = StringVar()

METHODPOSITIVE1 = StringVar()
METHODNEGATIVE1 = StringVar()
METHODMONEYLOSS1 = StringVar()
METHODMONEYGAIN1 = StringVar()

METHODPOSITIVE2 = StringVar()
METHODNEGATIVE2 = StringVar()
METHODMONEYLOSS2 = StringVar()
METHODMONEYGAIN2 = StringVar()

DESTINATION = StringVar()
SEARCHSTR = StringVar()


def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


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


def SendMethodQuery(token, methodPosProb, methodNegProg, methodMoneyLoss, methodMoneyGain, methodPosProb1, methodNegProg1, methodMoneyLoss1, methodMoneyGain1, methodPosProb2, methodNegProg2, methodMoneyLoss2, methodMoneyGain2):
    tempPosProb = methodPosProb.get()
    tempNegProb = methodNegProg.get()
    tempMoneyLoss = methodMoneyLoss.get()
    tempMoneyGain = methodMoneyGain.get()

    tempPosProb1 = methodPosProb1.get()
    tempNegProb1 = methodNegProg1.get()
    tempMoneyLoss1 = methodMoneyLoss1.get()
    tempMoneyGain1 = methodMoneyGain1.get()

    tempPosProb2 = methodPosProb2.get()
    tempNegProb2 = methodNegProg2.get()
    tempMoneyLoss2 = methodMoneyLoss2.get()
    tempMoneyGain2 = methodMoneyGain2.get()

    if token == 0:
        if tempPosProb == "" or tempNegProb == "" or tempMoneyLoss == "" or tempMoneyGain == "" or tempPosProb1 == "" or tempNegProb1 == "" or tempMoneyLoss1 == "" or tempMoneyGain1 == "":
            box.showerror("Ошибка", "Поля не могут быть пустыми!")
            return
        if float(tempPosProb) + float(tempNegProb) == 1 and float(tempPosProb1) + float(tempNegProb1) == 1:
            project1 = classes.Project(tempPosProb, tempNegProb,
                                       tempMoneyLoss, tempMoneyGain)
            project2 = classes.Project(tempPosProb1, tempNegProb1,
                                       tempMoneyLoss1, tempMoneyGain1)
            methodQuery = classes.MethodQuery(9)
            methodQuery.addProject(project1, project2)
            JsonObject = methodQuery.toJSON()
            serialized = json.dumps(JsonObject)
            client.sendall(serialized.encode(FORMAT))
            received_answer = client.recv(1024).decode(FORMAT)
            deserialized = json.loads(received_answer)
            res = json.loads(deserialized)
            print(res)
            if str(res["answer_message"]) == "method1_best":
                box.showinfo("Метод", "Стратегия 1 будет наилучшим выбором")
            elif str(res["answer_message"]) == "method2_best":
                box.showinfo("Метод", "Стратегия 2 будет наилучшим выбором")
            elif str(res["answer_message"]) == "variables_equal":
                box.showinfo(
                    "Метод", "Коэффиценты равны. Можно выбрать любую стратегию")
            elif str(res["answer_message"]) == "calc_error":
                box.showinfo(
                    "Метод", "При подсчете коэффицентов произошла ошибка. \nПерепроверьте введенные данные")

        else:
            box.showerror(
                "Ошибка", "Сумма вероятностей должна равняться 1!")

    elif token == 1:
        if tempPosProb == "" or tempNegProb == "" or tempMoneyLoss == "" or tempMoneyGain == "" or tempPosProb1 == "" or tempNegProb1 == "" or tempMoneyLoss1 == "" or tempMoneyGain1 == "" or tempPosProb2 == "" or tempNegProb2 == "" or tempMoneyLoss2 == "" or tempMoneyGain2 == "":
            box.showerror("Ошибка", "Поля не могут быть пустыми!")
            return
        if float(tempPosProb) + float(tempNegProb) == 1 and float(tempPosProb1) + float(tempNegProb1) == 1 or float(tempPosProb2) + float(tempNegProb2) == 1:
            project1 = classes.Project(tempPosProb, tempNegProb,
                                       tempMoneyLoss, tempMoneyGain)
            project2 = classes.Project(tempPosProb1, tempNegProb1,
                                       tempMoneyLoss1, tempMoneyGain1)
            project3 = classes.Project(tempPosProb2, tempNegProb2,
                                       tempMoneyLoss2, tempMoneyGain2)

            methodQuery = classes.MethodQuery(9)
            methodQuery.addProject(project1, project2, project3)
            JsonObject = methodQuery.toJSON()
            serialized = json.dumps(JsonObject)
            client.sendall(serialized.encode(FORMAT))
            received_answer = client.recv(1024).decode(FORMAT)
            deserialized = json.loads(received_answer)
            res = json.loads(deserialized)
            if str(res["answer_message"]) == "method1_best":
                box.showinfo("Метод", "Стратегия 1 будет наилучшим выбором")
            elif str(res["answer_message"]) == "method2_best":
                box.showinfo("Метод", "Стратегия 2 будет наилучшим выбором")
            elif str(res["answer_message"]) == "method3_best":
                box.showinfo("Метод", "Стратегия 3 будет наилучшим выбором")
            elif str(res["answer_message"]) == "variables_equal":
                box.showinfo(
                    "Метод", "Коэффиценты равны. Можно выбрать любую стратегию")
            elif str(res["answer_message"]) == "calc_error":
                box.showinfo(
                    "Метод", "При подсчете коэффицентов произошла ошибка. \nПерепроверьте введенные данные")
        else:
            box.showerror(
                "Ошибка", "Сумма вероятностей не должна превышать 1!")


def SendQuery(login, password, token, secret_key):
    if login.get() == "" or login.get() == "":
        box.showerror("Ошибка", "Поля не должны быть пустыми ")
        LoginPanel()
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
                userProfile = classes.QueryModel(
                    res["balance"], res["permission"])
                DashBoardWindow(userProfile)
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


def SearchObjectFrame(keystr, titleFrame, mainFrame, token):
    if token == 0:
        titleFrame.destroy()
        mainFrame.destroy()
        search_string = keystr.get()
        searchQuery = classes.QueryModel(search_string, 0, 11)
        JsonObject = searchQuery.toJSON()
        serialized = json.dumps(JsonObject)
        client.sendall(serialized.encode(FORMAT))

        received_answer = client.recv(1024).decode(FORMAT)
        deserialized = json.loads(received_answer)
        res = json.loads(deserialized)
        tempList = res[0]
        print(tempList)
        searchTitleFrame = Frame(
            master, height=100, width=640, bd=1, relief=SOLID)
        searchTitleFrame.pack(side=TOP)
        lbl_title = Label(searchTitleFrame, text=f"Результат поиска по: {SEARCHSTR.get()}", font=(
            'courier', 14), bd=1, width=640)
        lbl_title.pack()

        carHandlerWindow = Frame(master)
        carHandlerWindow.pack(side=TOP)
        text = Listbox(carHandlerWindow, width=640, bd=1, relief=SOLID)
        for i in tempList:
            text.insert(END, "id: " + str(i[0]) + ". Модель авто: " +
                        str(i[1]) + " ФИО Водителя: " + str(i[3]) + " " + str(i[2]) + " " + str(i[4]))
        text.grid(pady=20)
        return_btn = Button(carHandlerWindow, text="Вернуться",
                            font=('Arial', 14), command=lambda: [carHandlerWindow.destroy(), searchTitleFrame.destroy(), CarsHandlerWindow()])
        return_btn.grid(row=8, sticky=W, pady=10, padx=20)
    elif token == 1:
        titleFrame.destroy()
        mainFrame.destroy()
        search_string = keystr.get()
        searchQuery = classes.QueryModel(search_string, 0, 12)
        JsonObject = searchQuery.toJSON()
        serialized = json.dumps(JsonObject)
        client.sendall(serialized.encode(FORMAT))

        received_answer = client.recv(1024).decode(FORMAT)
        deserialized = json.loads(received_answer)
        res = json.loads(deserialized)
        tempList = res[0]
        print(tempList)
        searchTitleFrame = Frame(
            master, height=100, width=640, bd=1, relief=SOLID)
        searchTitleFrame.pack(side=TOP)
        lbl_title = Label(searchTitleFrame, text=f"Результат поиска по: {SEARCHSTR.get()}", font=(
            'courier', 14), bd=1, width=640)
        lbl_title.pack()

        userHandlerWindow = Frame(master)
        userHandlerWindow.pack(side=TOP)
        text = Listbox(userHandlerWindow, width=640, bd=1, relief=SOLID)
        for i in tempList:
            textPermission = "Администратор" if i[
                3] == 1 else f"Пользователь Баланс: {str(i[4])} руб."
            text.insert(
                END, "id: " + str(i[2]) + ". Логин: " + i[0] + " Права доступа: " + textPermission)
        text.grid(pady=20)
        return_btn = Button(userHandlerWindow, text="Вернуться",
                            font=('Arial', 14), command=lambda: [userHandlerWindow.destroy(), searchTitleFrame.destroy(), UsersHandlerWindow()])
        return_btn.grid(row=8, sticky=W, pady=10, padx=20)


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


def deleteMethodWindow(button):
    methodWindow.destroy()
    CleanVariables()
    button["state"] = 'normal'


def deleteBalanceFrame(button):
    balanceFrame.destroy()
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
    text.grid(pady=20)
    del_btn = Button(carHandlerWindow, text="Удалить",
                     font=('Arial', 14), command=lambda: DeleteSelectedObject(text, tempCarList, 1))
    del_btn.grid(row=8, sticky=W, pady=10, padx=20)
    return_btn = Button(carHandlerWindow, text="Вернуться",
                        font=('Arial', 14), command=lambda: [carHandlerWindow.destroy(), handlerTitleFrame.destroy(), AdministratorDashboard()])
    return_btn.grid(row=8, sticky=W, pady=10, padx=140)
    refresh_btn = Button(carHandlerWindow, text="Обновить",
                         font=('Arial', 14), command=lambda: [carHandlerWindow.destroy(), handlerTitleFrame.destroy(), CarsHandlerWindow()])
    refresh_btn.grid(row=8, sticky=W, pady=10, padx=280)
    adduser_btn = Button(carHandlerWindow, text="Добавить", font=(
        'Arial', 14), command=lambda: CarAdditionWindow(adduser_btn))
    adduser_btn.grid(row=8, sticky=W, pady=10, padx=420)
    search_entr = Entry(carHandlerWindow, font=(
        'verdana', 14), textvariable=SEARCHSTR, width=15)
    search_entr.grid(row=9, sticky=W, pady=10, padx=40)
    search_btn = Button(carHandlerWindow, text="Найти",
                        font=('Arial', 12), command=lambda: [SearchObjectFrame(SEARCHSTR, handlerTitleFrame, carHandlerWindow, 0)])
    search_btn.grid(row=9, sticky=W, pady=10, padx=260)


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


def DashBoardWindow(userProfile):
    global dashboardFrame, dashboardTitleFrame, method_btn
    dashboardTitleFrame = Frame(
        master, height=100, width=640, bd=1, relief=SOLID)
    dashboardTitleFrame.pack(side=TOP)

    dashboardFrame = Frame(master)
    dashboardFrame.pack(side=TOP, pady=20)

    lbl_title = Label(dashboardTitleFrame, text=f"Добро пожаловать, {LOGINUSER.get()}!",
                      font=('courier', 14), bd=1, width=640)
    lbl_title.pack()

    btn_logout = Button(dashboardFrame, text="Выйти", font=(
        'Arial', 14), command=lambda: [dashboardFrame.destroy(), dashboardTitleFrame.destroy(), LoginPanel()])
    btn_logout.grid(row=5, columnspan=2, padx=520)
    profile_btn = Button(dashboardFrame, text="Профиль",
                         font=('Arial', 14), command=lambda: [dashboardFrame.destroy(), dashboardTitleFrame.destroy(), ProfilePageFrame(userProfile)])
    profile_btn.grid(row=3, column=0, sticky=W, padx=80, pady=10)
    order_btn = Button(dashboardFrame, text="Заказать такси", font=(
        'Arial', 14), command=lambda: [dashboardFrame.destroy(), dashboardTitleFrame.destroy(), TaxiOrder(userProfile)])
    order_btn.grid(row=4, column=0, sticky=W, padx=80, pady=10)
    method_btn = Button(dashboardFrame, text="Метод", font=(
        'Arial', 14), command=lambda: [MethodWindow(method_btn)])
    method_btn.grid(row=5, column=0, sticky=W, padx=80, pady=10)


def MethodWindow(button):
    global methodWindow, variable, choice_box
    choices = ('2 Проекта', '3 Проекта')
    variable = StringVar()
    methodWindow = Toplevel(master)
    methodWindow.title("Экспертный метод")
    methodWindow.geometry("520x680")
    methodWindow.resizable(False, False)
    methodWindow.iconphoto(False, icon)
    methodWindow.protocol(
        "WM_DELETE_WINDOW", lambda: deleteMethodWindow(button))
    choice_box = ttk.Combobox(methodWindow, textvariable=variable)
    choice_box['values'] = choices
    choice_box.grid(pady=20)
    choice_box["state"] = 'readonly'
    choice_box.bind('<<ComboboxSelected>>', ComboboxAction)
    return_btn = Button(methodWindow, text="Вернуться",
                        font=('Arial', 14), command=lambda: [CleanVariables(), methodWindow.destroy(), choice_box.set("")])
    return_btn.grid(row=18, sticky=W, padx=10, pady=10)


def CleanVariables():
    METHODPOSITIVE.set("")
    METHODNEGATIVE.set("")
    METHODMONEYLOSS.set("")
    METHODMONEYGAIN.set("")

    METHODPOSITIVE1.set("")
    METHODNEGATIVE1.set("")
    METHODMONEYLOSS1.set("")
    METHODMONEYGAIN1.set("")

    METHODPOSITIVE2.set("")
    METHODNEGATIVE2.set("")
    METHODMONEYLOSS2.set("")
    METHODMONEYGAIN2.set("")


def ComboboxAction(event):
    if variable.get() == '2 Проекта':
        choice_box["state"] = 'disabled'
        lbl_project = Label(methodWindow, text="Расширить охват на юг города: ",
                            font=('courier', 10), bd=8)
        lbl_project.grid(row=1, sticky=W)
        lbl_positive = Label(methodWindow, text="Введите шанс на успех:",
                             font=('courier', 10), bd=8)
        lbl_positive.grid(row=2, sticky=W)

        lbl_negative = Label(methodWindow, text="Введите шанс на неудачу:",
                             font=('courier', 10), bd=8)
        lbl_negative.grid(row=3, sticky=W)

        lbl_revenue = Label(methodWindow, text="Введите сумму прибыли:",
                            font=('courier', 10), bd=8)
        lbl_revenue.grid(row=4, sticky=W)

        lbl_loss = Label(methodWindow, text="Введите сумму потерь:",
                         font=('courier', 10), bd=8)
        lbl_loss.grid(row=5, sticky=W)

        entr_positive = Entry(methodWindow, font=('verdana', 10),
                              textvariable=METHODPOSITIVE, width=15)
        entr_positive.grid(row=2, column=1)

        entr_negative = Entry(methodWindow, font=('verdana', 10),
                              textvariable=METHODNEGATIVE, width=15)
        entr_negative.grid(row=3, column=1)

        entr_revenue = Entry(methodWindow, font=('verdana', 10),
                             textvariable=METHODMONEYGAIN, width=15)
        entr_revenue.grid(row=4, column=1)

        entr_loss = Entry(methodWindow, font=('verdana', 10),
                          textvariable=METHODMONEYLOSS, width=15)
        entr_loss.grid(row=5, column=1)
        lbl_project = Label(methodWindow, text="Расширить охват на север города: ",
                            font=('courier', 10), bd=8)
        lbl_project.grid(row=7, sticky=W)
        lbl_positive = Label(methodWindow, text="Введите шанс на успех:",
                             font=('courier', 10), bd=8)
        lbl_positive.grid(row=8, sticky=W)

        lbl_negative = Label(methodWindow, text="Введите шанс на неудачу:",
                             font=('courier', 10), bd=8)
        lbl_negative.grid(row=9, sticky=W)

        lbl_revenue = Label(methodWindow, text="Введите сумму прибыли:",
                            font=('courier', 10), bd=8)
        lbl_revenue.grid(row=10, sticky=W)

        lbl_loss = Label(methodWindow, text="Введите сумму потерь:",
                         font=('courier', 10), bd=8)
        lbl_loss.grid(row=11, sticky=W)

        entr_positive = Entry(methodWindow, font=('verdana', 10),
                              textvariable=METHODPOSITIVE1, width=15)
        entr_positive.grid(row=8, column=1)

        entr_negative = Entry(methodWindow, font=('verdana', 10),
                              textvariable=METHODNEGATIVE1, width=15)
        entr_negative.grid(row=9, column=1)

        entr_revenue = Entry(methodWindow, font=('verdana', 10),
                             textvariable=METHODMONEYGAIN1, width=15)
        entr_revenue.grid(row=10, column=1)

        entr_loss = Entry(methodWindow, font=('verdana', 10),
                          textvariable=METHODMONEYLOSS1, width=15)
        entr_loss.grid(row=11, column=1)
        two_btn = Button(methodWindow, text="Отправить", font=(
            'verdana', 14), command=lambda: [SendMethodQuery(0, METHODPOSITIVE, METHODNEGATIVE, METHODMONEYLOSS, METHODMONEYGAIN, METHODPOSITIVE1, METHODNEGATIVE1, METHODMONEYLOSS1, METHODMONEYGAIN1, METHODPOSITIVE2, METHODNEGATIVE2, METHODMONEYLOSS2, METHODMONEYGAIN2)])
        two_btn.grid(row=18, column=1, padx=10, pady=10)

    if variable.get() == '3 Проекта':
        choice_box["state"] = 'disabled'
        lbl_project = Label(methodWindow, text="Расширить охват на юг города: ",
                            font=('courier', 10), bd=8)
        lbl_project.grid(row=1, sticky=W)
        lbl_positive = Label(methodWindow, text="Введите шанс на успех:",
                             font=('courier', 10), bd=8)
        lbl_positive.grid(row=2, sticky=W)

        lbl_negative = Label(methodWindow, text="Введите шанс на неудачу:",
                             font=('courier', 10), bd=8)
        lbl_negative.grid(row=3, sticky=W)

        lbl_revenue = Label(methodWindow, text="Введите сумму прибыли:",
                            font=('courier', 10), bd=8)
        lbl_revenue.grid(row=4, sticky=W)

        lbl_loss = Label(methodWindow, text="Введите сумму потерь:",
                         font=('courier', 10), bd=8)
        lbl_loss.grid(row=5, sticky=W)

        entr_positive = Entry(methodWindow, font=('verdana', 10),
                              textvariable=METHODPOSITIVE, width=15)
        entr_positive.grid(row=2, column=1)

        entr_negative = Entry(methodWindow, font=('verdana', 10),
                              textvariable=METHODNEGATIVE, width=15)
        entr_negative.grid(row=3, column=1)

        entr_revenue = Entry(methodWindow, font=('verdana', 10),
                             textvariable=METHODMONEYGAIN, width=15)
        entr_revenue.grid(row=4, column=1)

        entr_loss = Entry(methodWindow, font=('verdana', 10),
                          textvariable=METHODMONEYLOSS, width=15)
        entr_loss.grid(row=5, column=1)

        lbl_project = Label(methodWindow, text="Расширить охват на север города: ",
                            font=('courier', 10), bd=8)
        lbl_project.grid(row=7, sticky=W)
        lbl_positive = Label(methodWindow, text="Введите шанс на успех:",
                             font=('courier', 10), bd=8)
        lbl_positive.grid(row=8, sticky=W)

        lbl_negative = Label(methodWindow, text="Введите шанс на неудачу:",
                             font=('courier', 10), bd=8)
        lbl_negative.grid(row=9, sticky=W)

        lbl_revenue = Label(methodWindow, text="Введите сумму прибыли:",
                            font=('courier', 10), bd=8)
        lbl_revenue.grid(row=10, sticky=W)

        lbl_loss = Label(methodWindow, text="Введите сумму потерь:",
                         font=('courier', 10), bd=8)
        lbl_loss.grid(row=11, sticky=W)

        entr_positive = Entry(methodWindow, font=('verdana', 10),
                              textvariable=METHODPOSITIVE1, width=15)
        entr_positive.grid(row=8, column=1)

        entr_negative = Entry(methodWindow, font=('verdana', 10),
                              textvariable=METHODNEGATIVE1, width=15)
        entr_negative.grid(row=9, column=1)

        entr_revenue = Entry(methodWindow, font=('verdana', 10),
                             textvariable=METHODMONEYGAIN1, width=15)
        entr_revenue.grid(row=10, column=1)

        entr_loss = Entry(methodWindow, font=('verdana', 10),
                          textvariable=METHODMONEYLOSS1, width=15)
        entr_loss.grid(row=11, column=1)
        lbl_project = Label(methodWindow, text="Расширить охват за городом: ",
                            font=('courier', 10), bd=8)
        lbl_project.grid(row=13, sticky=W)
        lbl_positive = Label(methodWindow, text="Введите шанс на успех:",
                             font=('courier', 10), bd=8)
        lbl_positive.grid(row=14, sticky=W)

        lbl_negative = Label(methodWindow, text="Введите шанс на неудачу:",
                             font=('courier', 10), bd=8)
        lbl_negative.grid(row=15, sticky=W)

        lbl_revenue = Label(methodWindow, text="Введите сумму прибыли:",
                            font=('courier', 10), bd=8)
        lbl_revenue.grid(row=16, sticky=W)

        lbl_loss = Label(methodWindow, text="Введите сумму потерь:",
                         font=('courier', 10), bd=8)
        lbl_loss.grid(row=17, sticky=W)

        entr_positive = Entry(methodWindow, font=('verdana', 10),
                              textvariable=METHODPOSITIVE2, width=15)
        entr_positive.grid(row=14, column=1)

        entr_negative = Entry(methodWindow, font=('verdana', 10),
                              textvariable=METHODNEGATIVE2, width=15)
        entr_negative.grid(row=15, column=1)

        entr_revenue = Entry(methodWindow, font=('verdana', 10),
                             textvariable=METHODMONEYGAIN2, width=15)
        entr_revenue.grid(row=16, column=1)

        entr_loss = Entry(methodWindow, font=('verdana', 10),
                          textvariable=METHODMONEYLOSS2, width=15)
        entr_loss.grid(row=17, column=1)

        three_btn = Button(methodWindow, text="Отправить", font=(
            'verdana', 14), command=lambda: [SendMethodQuery(1, METHODPOSITIVE, METHODNEGATIVE, METHODMONEYLOSS, METHODMONEYGAIN, METHODPOSITIVE1, METHODNEGATIVE1, METHODMONEYLOSS1, METHODMONEYGAIN1, METHODPOSITIVE2, METHODNEGATIVE2, METHODMONEYLOSS2, METHODMONEYGAIN2)])
        three_btn.grid(row=18, column=1, padx=10, pady=10)


def ProfilePageFrame(userProfile):
    profileFrame = Frame(master, height=150, width=640, bd=1, relief=SOLID)
    profileFrame.pack(side=TOP)

    profileButtonsFrame = Frame(master)
    profileButtonsFrame.pack(side=TOP, pady=20)

    permissions = "Администратор" if userProfile.permission == 1 else "Пользователь/Эксперт"
    lbl_maininfo = Label(profileFrame,
                         text=f"Логин: {LOGINUSER.get()}. \n{permissions}\n Ваш баланс: {toFixed(userProfile.balance, 1)} руб.", font=('courier', 14), bd=1, width=640)
    lbl_maininfo.pack()
    btn_add_balance = Button(profileButtonsFrame, text="Пополнить баланс", font=(
        'Arial', 14), command=lambda: [BalanceAddition(btn_add_balance, userProfile)])
    btn_add_balance.grid(row=3, column=0, sticky=W, padx=80, pady=10)
    return_btn = Button(profileButtonsFrame, text="Вернуться",
                        font=('Arial', 14), command=lambda: [profileFrame.destroy(), profileButtonsFrame.destroy(), DashBoardWindow(userProfile)])
    return_btn.grid(row=3, column=1, sticky=W, padx=80, pady=10)


def TaxiOrder(userProfile):
    tempCarList = []
    tempCarList = RequestDataList(1)
    sortedList = sorted(tempCarList, key=lambda x: x[0])
    print(sortedList)
    print(sortedList[0][0])
    handlerTitleFrame = Frame(
        master, height=100, width=640, bd=1, relief=SOLID)
    handlerTitleFrame.pack(side=TOP)
    lbl_title = Label(handlerTitleFrame, text="Список доступных водителей", font=(
        'courier', 14), bd=1, width=640)
    lbl_title.pack()

    taxiOrderFrame = Frame(master)
    taxiOrderFrame.pack(side=TOP)
    text = Listbox(taxiOrderFrame, width=640, bd=1, relief=SOLID)
    for i in sortedList:
        text.insert(END, "id: " + str(i[0]) + ". Модель авто: " +
                    str(i[1]) + " ФИО Водителя: " + str(i[3]) + " " + str(i[2]) + " " + str(i[4]))
    text.grid()
    lbl_destination = Label(taxiOrderFrame, text="Введите пункт назначения:",
                            font=('courier', 14), bd=14)
    lbl_destination.grid(row=8, sticky=W, pady=10, padx=20)

    reg_user = Entry(taxiOrderFrame, font=('verdana', 16),
                     textvariable=DESTINATION, width=15)
    reg_user.grid(sticky=W, row=8, pady=10, padx=330)
    order_btn = Button(taxiOrderFrame, text="Заказать",
                       font=('Arial', 14), command=lambda: OrderSelectedTaxi(text, tempCarList, userProfile))
    order_btn.grid(sticky=W, row=9, pady=10, padx=20)
    return_btn = Button(taxiOrderFrame, text="Вернуться",
                        font=('Arial', 14), command=lambda: [taxiOrderFrame.destroy(), handlerTitleFrame.destroy(), DashBoardWindow(userProfile)])
    return_btn.grid(sticky=W, row=9, pady=10, padx=140)
    refresh_btn = Button(taxiOrderFrame, text="Обновить",
                         font=('Arial', 14), command=lambda: [taxiOrderFrame.destroy(), handlerTitleFrame.destroy(), TaxiOrder(userProfile)])
    refresh_btn.grid(sticky=W, row=9, pady=10, padx=280)


def BalanceAddition(button, userProfile):
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
    lbl_balance.grid(row=3)

    entr_balance = Entry(balanceFrame, font=(
        'verdana', 14), textvariable=BALANCE, width=15)
    entr_balance.grid(row=3, column=1)
    btn_balance = Button(balanceFrame, text="Пополнить", font=('Arial', 14),
                         command=lambda: [SendBalanceQuery(BALANCE, userProfile)])
    btn_balance.grid(row=5, column=1, pady=20, padx=20)
    return_btn = Button(balanceFrame, text="Вернуться",
                        font=('Arial', 14), command=lambda: [deleteBalanceFrame(button)])
    return_btn.grid(row=5, column=2, pady=20, padx=20)


def SendBalanceQuery(balance, userProfile):
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
            userProfile.balance = float(res["balance"]) + float(tempBalance)
            print(balance)
        elif str(res["answer_message"]) == "balance_not_changed":
            box.showerror("Ошибка", "При пополнении баланса возникла ошибка")


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
        textPermission = "Администратор" if i[
            3] == 1 else f"Пользователь Баланс: { str(i[4])} руб."
        text.insert(
            END, "id: " + str(i[2]) + ". Логин: " + i[0] + " Права доступа: " + textPermission)
    text.grid(pady=20)

    del_btn = Button(userHandlerWindow, text="Удалить",
                     font=('Arial', 14), command=lambda: DeleteSelectedObject(text, sortedList, 0))
    del_btn.grid(row=8, sticky=W, pady=10, padx=20)
    return_btn = Button(userHandlerWindow, text="Вернуться",
                        font=('Arial', 14), command=lambda: [userHandlerWindow.destroy(), handlerTitleFrame.destroy(), AdministratorDashboard()])
    return_btn.grid(row=8, sticky=W, pady=10, padx=140)
    refresh_btn = Button(userHandlerWindow, text="Обновить",
                         font=('Arial', 14), command=lambda: [userHandlerWindow.destroy(), handlerTitleFrame.destroy(), UsersHandlerWindow()])
    refresh_btn.grid(row=8, sticky=W, pady=10, padx=280)
    adduser_btn = Button(userHandlerWindow, text="Добавить", font=(
        'Arial', 14), command=lambda: RegistrationWindow(adduser_btn))
    adduser_btn.grid(row=8, sticky=W, pady=10, padx=420)
    search_entr = Entry(userHandlerWindow, font=(
        'verdana', 14), textvariable=SEARCHSTR, width=15)
    search_entr.grid(row=9, sticky=W, pady=10, padx=40)
    search_btn = Button(userHandlerWindow, text="Найти",
                        font=('Arial', 12), command=lambda: [SearchObjectFrame(SEARCHSTR, handlerTitleFrame, userHandlerWindow, 1)])
    search_btn.grid(row=9, sticky=W, pady=10, padx=260)


def OrderSelectedTaxi(text, tempList, userProfile):
    if DESTINATION.get() == "" or DESTINATION.get() == "":
        box.showerror("Ошибка", "Введите пункт назначения ")
        return
    sortedList = sorted(tempList, key=lambda x: x[2])
    print(sortedList)
    userLogin = LOGINUSER.get()
    userBalance = userProfile.balance
    for i in text.curselection():
        tempStr = text.get(i)
        print(tempStr)
        orderObjectData = classes.QueryModel(
            userLogin, userBalance, 10)
        print(orderObjectData)
        JsonObject = orderObjectData.toJSON()
        serialized = json.dumps(JsonObject)
        client.sendall(serialized.encode(FORMAT))

        order_answer = client.recv(1024).decode(FORMAT)
        try:
            order_list = json.loads(order_answer)
        except (TypeError, ValueError) as e:
            raise Exception('Data received was not in JSON format')
        res = json.loads(order_list)
        print(res)
        print(res["answer_message"])
        if str(res["answer_message"]) == "ordered_successfully":
            est_driver_time = str(res["driver_delay"])
            ride_cost = str(res["ride_cost"])
            userProfile.balance = userBalance - float(ride_cost)
            answerString = f"Ваш заказ был принят! \nОжидайте водителя в течение {toFixed(float(est_driver_time), 2)} мин.\nСтоимость поездки - {toFixed(float(ride_cost),2)} руб."
            box.showinfo(
                "Успех!", answerString)
            text.delete(i)
        elif str(res["answer_message"]) == "order_denied":
            box.showerror(
                "Ошибка!", "Во время обработки заказа произошла ошибка либо у вас на балансе недостаточно средств!")
        else:
            box.showerror("Ошибка!", "Неизвестная ошибка!")
    return userProfile


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
