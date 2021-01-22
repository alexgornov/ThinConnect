#############################################################################
#
#
# Need:
# packet freerdp2-x11
# python3-tk
# pip3 install pillow
# pip3 install passlib
#############################################################################

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import socket
import yaml
import subprocess
import getpass
import os
from passlib.hash import pbkdf2_sha256

#Put image file name here
imagepath = "confi.png"
adminpass_hash = "$pbkdf2-sha256$29000$SckZQ8h5z9mbsxYCwDgHAA$ZM8GlKHnTFKHaWn3/.YjlvQKep7/xnoeIC.4JZ55Nc0" # sha256 hash pass

#Read config file
with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

#Get username for USB Mount
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


def ConnectButton(*args):
    #####Check input

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
    if os.path.isdir("/media/" + username):
        arg.append("/drive:USB,/media/" + username)

    for i in (cfg["config"]):
        arg.append(i)

    if (cfg["servers"][server]["extendedconfig"]) != "":
        for i in (cfg["servers"][server]["extendedconfig"]):
            arg.append(i)
    #For debug:
    #print(arg)
    #messagebox.showinfo("test", arg)
    # Clear Entry
    loginEntry.delete(0, END)
    passEntry.delete(0, END)
    loginEntry.configure(state=DISABLED)
    passEntry.configure(state=DISABLED)
    BtnConnect.configure(state=DISABLED, text="Подключение...")

    # Run freerdp
    process = subprocess.Popen(arg, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=False)
    process.wait()
    loginEntry.configure(state=NORMAL)
    passEntry.configure(state=NORMAL)
    BtnConnect.configure(state=NORMAL, text="Подключиться")
    ######Error processing:


def adminMenu():
    if pbkdf2_sha256.verify(adminpass.get(), adminpass_hash):
        f_menu = Frame(root)
        f_menu.place(relx=.5, rely=.8, anchor="c")
        BtnExit = Button(f_menu, text="Выход", command=exit)
        BtnExit.grid(row=0, column=0, padx=5, pady=5, sticky=N + S + W + E)
    else:
        messagebox.showerror("Ошибка", "Неверный пароль")

#Window
root = Tk()
root.attributes('-fullscreen', True)

f_center = Frame(root)
f_center.place(relx=.5, rely=.5, anchor="c")

login = StringVar()
password = StringVar()

#add imagelogo
if os.path.isfile(imagepath):
    img = Image.open(imagepath)
    img = img.resize((500, 100), Image.ANTIALIAS)
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
loginEntry.focus()

passEntry = Entry(f_center, textvariable=password, show="*")
passEntry.grid(row=2, column=2, padx=5, pady=5, sticky=N+S+W+E)

BtnConnect = Button(f_center, text="Подключиться", command=ConnectButton)
BtnConnect.grid(row=3, column=2, padx=5, pady=5, sticky=N+S+W+E)

root.bind('<Return>', ConnectButton)

#Adminmenu
adminpass = StringVar()

f_admin = Frame(root)
f_admin.place(relx=0.9, rely=0.9, anchor="c")
AdmPassword = Entry(f_admin, textvariable=adminpass, show="*")
AdmPassword.grid(row=0, column=0, sticky=N+S+W+E)
AdmPassword.config(background="#F0F0F0")
AdmButton = Button(f_admin, text="Admin", command=adminMenu)
AdmButton.grid(row=1, column=0, sticky=N+S+W+E)

root.mainloop()