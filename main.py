#############################################################################
#
#
# need packet freerdp2-x11
# python3-tk
#
#
#############################################################################

from tkinter import *
from tkinter import messagebox
import socket, yaml, subprocess, getpass

#Read config file
with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

#Get username
username = getpass.getuser()

def TestConnection(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.01)
    try:
        sock.connect((host, port))
    except:
        return False
    else:
        return True

def ConnectButton():
    for i in (cfg["servers"]):
        if TestConnection((cfg["servers"][i]["ip"]), 3389):
            messagebox.showinfo("Подключение...", "Подключение к " + (cfg["servers"][i]["name"]))
            RunFreerdp(i)
            break
    else:
        messagebox.showinfo("Ошибка", "Нет доступа к серверу")

def RunFreerdp(server):
    arg = ["xfreerdp",
    "/v:" + (cfg["servers"][server]["ip"]),
    "/d:" + (cfg["domain"]),
    "/u:" + login.get(),
    "/p:" + password.get()
           ]

    for i in (cfg["config"]):
        arg.append(i)

    if (cfg["servers"][server]["extendedconfig"]) != "":
        for i in (cfg["servers"][server]["extendedconfig"]):
            arg.append(i)

    print(arg)
    messagebox.showinfo("test", arg)
    # Очищаем поля
    loginEntry.delete(0, END)
    passEntry.delete(0, END)
    subprocess.run(arg)

root = Tk()
root.attributes('-fullscreen', True)

login = StringVar()
password = StringVar()

loginLabel = Label(text="Логин: ")
passLabel = Label(text="Пароль: ")

loginLabel.grid(row=0, column=0, sticky="w")
passLabel.grid(row=1, column=0, sticky="w")

loginEntry = Entry(textvariable=login)
loginEntry.grid(row=0, column=1, padx=5, pady=5)

passEntry = Entry(textvariable=password, show="*")
passEntry.grid(row=1, column=1, padx=5, pady=5)

BtnConnect = Button(text="Подключиться", command=ConnectButton)
BtnConnect.grid(row=2, column=1, padx=5, pady=5, sticky="e")

BtnExit = Button(text="Выход", command=exit)
BtnExit.grid(row=3, column=1, padx=5, pady=5, sticky="e")

root.mainloop()