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
from datetime import datetime
from pathlib import Path

# Put image file name here
imagepath = "confi.png"
logfile = str(Path.home()) + "/connect.log"
devicefile = str(Path.home()) + "/dev"
# sha256 hash pass
adminpass_hash = "$pbkdf2-sha256$29000$SckZQ8h5z9mbsxYCwDgHAA$ZM8GlKHnTFKHaWn3/.YjlvQKep7/xnoeIC.4JZ55Nc0"
freerdperrors = {
    # section 0-15: protocol-independent codes
    0: '0 XF_EXIT_SUCCESS',
    1: '1 XF_EXIT_DISCONNECT',
    2: '2 XF_EXIT_LOGOFF',
    3: '3 XF_EXIT_IDLE_TIMEOUT',
    4: '4 XF_EXIT_LOGON_TIMEOUT',
    5: '5 XF_EXIT_CONN_REPLACED',
    6: '6 XF_EXIT_OUT_OF_MEMORY',
    7: '7 XF_EXIT_CONN_DENIED',
    8: '8 XF_EXIT_CONN_DENIED_FIPS',
    9: '9 XF_EXIT_USER_PRIVILEGES',
    10: '10 XF_EXIT_FRESH_CREDENTIALS_REQUIRED',
    11: '11 XF_EXIT_DISCONNECT_BY_USER',
    # section 16-31: license error set
    16: '16 XF_EXIT_LICENSE_INTERNAL',
    17: '17 XF_EXIT_LICENSE_NO_LICENSE_SERVER',
    18: '18 XF_EXIT_LICENSE_NO_LICENSE',
    19: '19 XF_EXIT_LICENSE_BAD_CLIENT_MSG',
    20: '20 XF_EXIT_LICENSE_HWID_DOESNT_MATCH',
    21: '21 XF_EXIT_LICENSE_BAD_CLIENT',
    22: '22 XF_EXIT_LICENSE_CANT_FINISH_PROTOCOL',
    23: '23 XF_EXIT_LICENSE_CLIENT_ENDED_PROTOCOL',
    24: '24 XF_EXIT_LICENSE_BAD_CLIENT_ENCRYPTION',
    25: '25 XF_EXIT_LICENSE_CANT_UPGRADE',
    26: '26 XF_EXIT_LICENSE_NO_REMOTE_CONNECTIONS',
    # section 32-127: RDP protocol error set
    32: '32 XF_EXIT_RDP',
    # section 128-254: xfreerdp specific exit codes
    128: '128 XF_EXIT_PARSE_ARGUMENTS',
    129: '129 XF_EXIT_MEMORY',
    130: '130 XF_EXIT_PROTOCOL',
    131: '131 XF_EXIT_CONN_FAILED',
    132: '132 XF_EXIT_AUTH_FAILURE',
    255: '255 XF_EXIT_UNKNOWN',
}

# Read config file
with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

# Get username for USB Mount
username = getpass.getuser()
hostname = socket.gethostname()


def rundevicemenu():
    subprocess.run(['python3', 'devices.py', devicefile])


def clearlog():
    f = open(logfile, 'w').close()


def logging(info):
    f = open(logfile, 'a')
    f.write("["+str(datetime.now())+"] " + info + "\n")
    f.close()


# Check connect device in list
def getdevicesforredirect():
    f = open(devicefile, 'r')
    devfile = f.read().split('\n')
    devlist = []
    devices = subprocess.run("lsusb", stdout=subprocess.PIPE).stdout.decode("utf-8").split("\n")
    for i in devices:
        devlist.append(i[23:32])
    for i in devfile:
        if i not in devlist:
            devfile.remove(i)
    return devfile


def testconnection(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.01)
    try:
        sock.connect((host, port))
    except:
        return False
    else:
        return True


def connectbutton(*args):
    # Check input
    chars = set('~`!@#$%^&*()\'+| \\|/,;\"')
    if login.get() == "":
        messagebox.showerror("Ошибка", "Логин не может быть пустым")
        return
    if any((c in chars) for c in login.get()):
        messagebox.showerror("Ошибка", "Недопустимый логин")
        loginEntry.delete(0, END)
        passEntry.delete(0, END)
        return
    if password.get() == '':
        messagebox.showerror("Ошибка", "Пароль не может быть пустым")
        return
    for i in (cfg["servers"]):
        if testconnection((cfg["servers"][i]["ip"]), 3389):
            runfreerdp(i)
            break
    else:
        messagebox.showinfo("Ошибка", "Нет доступа к серверу")


def createrdpargs(server):
    arg = ["xfreerdp",
           "/v:" + (cfg["servers"][server]["ip"]),
           "/d:" + (cfg["domain"]),
           "/u:" + login.get()
           ]
    if os.path.isdir("/media/" + username):
        arg.append("/drive:USB,/media/" + username)
    for i in (cfg["config"]):
        arg.append(i)
    if (cfg["servers"][server]["extendedconfig"]) != "":
        for i in (cfg["servers"][server]["extendedconfig"]):
            arg.append(i)
    devices = getdevicesforredirect()
    if devices != ['']:
        for i in getdevicesforredirect():
            arg.append("/usb:id,dev:" + i)
    logging(' '.join(map(str, arg)))
    arg.append("/p:" + password.get())
    # For debug:
    # messagebox.showinfo("test", arg)
    return arg


def runfreerdp(server):
    # Run freerdp
    process = subprocess.run(createrdpargs(server), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    passEntry.delete(0, END)
    # Error processing freerdp:
    code = process.returncode
    for i in process.stdout.decode("utf-8").split("\n"):
        logging(i)

    if code == 0 or code == 13 or code == 1 or code == 2 or code == 12:
        True
    elif code == 131 or code == 132:
        messagebox.showerror("Повторите подключение", "Ошибка логина-пароля")
    elif code in freerdperrors:
        messagebox.showerror("Ошибка", "Ошибка = {}".format(freerdperrors[code]) + '\nПовторите подключение')
    else:
        messagebox.showerror("Ошибка", "Код ошибки = {}".format(code) + '\nПовторите подключение')


def adminmenu():
    if pbkdf2_sha256.verify(adminpass.get(), adminpass_hash):
        AdmPassword.delete(0, END)
        f_menu = Frame(root)
        f_menu.place(relx=.5, rely=.8, anchor="c")
        btnexit = Button(f_menu, text="Выход", command=exit)
        btnexit.grid(row=0, column=0, padx=5, pady=5, sticky=N + S + W + E)
        btnclose = Button(f_menu, text="Закрыть меню", command=f_menu.destroy)
        btnclose.grid(row=1, column=0, padx=5, pady=5, sticky=N + S + W + E)
    else:
        messagebox.showerror("Ошибка", "Неверный пароль")
        AdmPassword.delete(0, END)


def reboot():
    os.system('sudo systemctl reboot')


def poweroff():
    os.system('sudo systemctl poweroff')


# Create device file if not exist
if not os.path.isfile(devicefile):
    open(devicefile, 'w').close()
clearlog()
# Window
root = Tk()
root.attributes('-fullscreen', True)

f_center = Frame(root)
f_center.place(relx=.5, rely=.5, anchor="c")

login = StringVar()
password = StringVar()

# add imagelogo
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
loginEntry.grid(row=1, column=2, padx=5, pady=5, sticky=N + S + W + E)
loginEntry.focus()
passEntry = Entry(f_center, textvariable=password, show="*")
passEntry.grid(row=2, column=2, padx=5, pady=5, sticky=N + S + W + E)
BtnConnect = Button(f_center, text="Подключиться", command=connectbutton)
BtnConnect.grid(row=3, column=2, padx=5, pady=5, sticky=N + S + W + E)
root.bind('<Return>', connectbutton)

f_lf = Frame(root)
f_lf.place(relx=0.1, rely=0.9, anchor="c")
hostnameLabel = Label(f_lf, text="Имя компьютера: " + hostname)
hostnameLabel.grid(row=0, column=0, sticky=N + S + W + E)
devmenuBtn = Button(f_lf, text="Устройства", command=rundevicemenu)
devmenuBtn.grid(row=1, column=0, sticky=N + S + W + E)
rebootBtn = Button(f_lf, text="Перезагрузка", command=reboot)
rebootBtn.grid(row=2, column=0, sticky=N + S + W + E)
poweroffBtn = Button(f_lf, text="Выключение", command=poweroff)
poweroffBtn.grid(row=3, column=0, sticky=N + S + W + E)
# Admin menu
adminpass = StringVar()

f_admin = Frame(root)
f_admin.place(relx=0.9, rely=0.9, anchor="c")
AdmPassword = Entry(f_admin, textvariable=adminpass, show="*")
AdmPassword.grid(row=0, column=0, sticky=N + S + W + E)
AdmPassword.config(background="#F0F0F0")
AdmButton = Button(f_admin, text="Admin", command=adminmenu)
AdmButton.grid(row=1, column=0, sticky=N + S + W + E)

root.mainloop()
