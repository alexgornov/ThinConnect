#############################################################################
#
#
# need packet freerdp2-x11
# python3-tk
# pip install pillow
#
#############################################################################

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import socket
import yaml
import subprocess
import getpass

#Put image file name here
imagepath = "confi.png"

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
    "/p:" + password.get(),
    "/drive:USB,/media/" + username
           ]

    for i in (cfg["config"]):
        arg.append(i)

    if (cfg["servers"][server]["extendedconfig"]) != "":
        for i in (cfg["servers"][server]["extendedconfig"]):
            arg.append(i)

    print(arg)
    messagebox.showinfo("test", arg)
    # Clear Entry
    loginEntry.delete(0, END)
    passEntry.delete(0, END)
    # Run freerdp
    subprocess.run(arg)

#Window
root = Tk()
root.attributes('-fullscreen', True)

f_center = Frame(root)
f_center.place(relx=.5, rely=.5, anchor="c")

login = StringVar()
password = StringVar()

if imagepath != "":
    img = Image.open(imagepath)
    img = img.resize((500,100),Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    imgLabel = Label(f_center, image=img)
    imgLabel.image = img
    imgLabel.grid(row=0, column=0, sticky="w", columnspan=6)

loginLabel = Label(f_center, text="Логин: ")
passLabel = Label(f_center, text="Пароль: ")

loginLabel.grid(row=1, column=1, sticky="e")
passLabel.grid(row=2, column=1, sticky="e")

loginEntry = Entry(f_center, textvariable=login)
loginEntry.grid(row=1, column=2, padx=5, pady=5, sticky=N+S+W+E)

passEntry = Entry(f_center, textvariable=password, show="*")
passEntry.grid(row=2, column=2, padx=5, pady=5, sticky=N+S+W+E)

BtnConnect = Button(f_center, text="Подключиться", command=ConnectButton)
BtnConnect.grid(row=3, column=2, padx=5, pady=5, sticky=N+S+W+E)

BtnExit = Button(f_center, text="Выход", command=exit)
BtnExit.grid(row=4, column=2, padx=5, pady=5, sticky=N+S+W+E)

root.mainloop()