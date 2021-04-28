from tkinter import *
import psycopg2
import tkinter.messagebox as box


def Database():
    global conn, cursor
    conn = psycopg2.connect(database="decadence", user="decadence",
                            password="12345", host="localhost", port="5432")
    cursor = conn.cursor()


print("Database opened successfully")


root = Tk()
root.title("Taxipark")
width = 640
height = 480
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)


# =======================================VARIABLES=====================================
USER = StringVar()
PASS = StringVar()


# =======================================METHODS=======================================


def Exit():
    result = tkMessageBox.askquestion(
        'System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()


def Login():
    Database()
    cursor.execute('SELECT "user", pass, id FROM public."user"')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        if USER.get() == row[0] and PASS.get() == row[1]:
            lbl_result.config(text="Successfully Entered!", fg="green")
            conn.commit()
            cursor.close()
            conn.close()
            break
        else:
            lbl_result.config(text="Incorrect credentials!", fg="red")


def Register():
    Database()
    if USER.get == "" or PASS.get() == "":
        lbl_result.config(
            text="Please complete the required field!", fg="orange")
    else:
        cursor.execute('SELECT * FROM public."user"')
        cursor.execute('INSERT INTO public."user" ("user", pass) VALUES (%s, %s)', (str(
            USER.get()), str(PASS.get())))
        conn.commit()
        USER.set("")
        PASS.set("")
        lbl_result.config(text="Successfully Created!", fg="green")
        cursor.close()
        conn.close()


# =====================================FRAMES====================================
TitleFrame = Frame(root, height=100, width=640, bd=1, relief=SOLID)
TitleFrame.pack(side=TOP)
RegisterFrame = Frame(root)
RegisterFrame.pack(side=TOP, pady=20)


lbl_title = Label(TitleFrame, text="Таксопарк",
                  font=('arial', 18), bd=1, width=640)
lbl_title.pack()
lbl_username = Label(RegisterFrame, text="Username:",
                     font=('arial', 18), bd=18)
lbl_username.grid(row=1)
lbl_password = Label(RegisterFrame, text="Password:",
                     font=('arial', 18), bd=18)
lbl_password.grid(row=2)
lbl_result = Label(RegisterFrame, text="", font=('arial', 18))
lbl_result.grid(row=5, columnspan=2)


user = Entry(RegisterFrame, font=('arial', 20),
             textvariable=USER, width=15)
user.grid(row=1, column=1)
pass1 = Entry(RegisterFrame, font=('arial', 20),
              textvariable=PASS, width=15, show="*")
pass1.grid(row=2, column=1)

btn_register = Button(RegisterFrame, font=('arial', 20),
                      text="Register", command=Register)
btn_register.grid(row=6, columnspan=2)

btn_login = Button(RegisterFrame, font=('arial', 20),
                   text="Login", command=Login)
btn_login.grid(row=6, columnspan=1)


# ========================================INITIALIZATION===================================
if __name__ == '__main__':
    root.mainloop()
