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
import socket
import yaml
import subprocess

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

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
    arg=["xfreerdp",
    "/v:" + (cfg["servers"][server]["ip"]),
    "/d:" + (cfg["domain"]),
    "/load-balance-info:" + (cfg["servers"][server]["loadbalanceinfo"]),
    "/u:" + login.get(),
    "/p:" + password.get()]

    for i in (cfg["config"]).split():
        arg.append(i)

    if (cfg["servers"],[server],["extendedconfig"]) != "":
        for i in (cfg["servers"][server]["extendedconfig"]).split():
            arg.append(i)
    print(arg)
    messagebox.showinfo("123", arg)
    #subprocess.run(arg)

root = Tk()
root.attributes('-fullscreen', True)

login = StringVar()
password = StringVar()

loginLabel = Label(text="Логин: ")
passLabel = Label(text="Пароль: ")

loginLabel.grid(row=0, column=0, sticky="w")
passLabel.grid(row=1, column=0, sticky="w")

loginEntry = Entry(textvariable=login)
loginEntry.grid(row=0,column=1, padx=5, pady=5)

passEntry = Entry(textvariable=password,show="*")
passEntry.grid(row=1,column=1, padx=5, pady=5)

BtnConnect = Button(text="Подключиться",command=ConnectButton)
BtnConnect.grid(row=2,column=1, padx=5, pady=5, sticky="e")

BtnExit = Button(text="Выход", command=exit)
BtnExit.grid(row=3,column=1, padx=5, pady=5, sticky="e")

root.mainloop()