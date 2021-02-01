from tkinter import *
import subprocess
import sys

devfile = sys.argv[1]

root = Tk()

devices = subprocess.run("lsusb", stdout=subprocess.PIPE).stdout.decode("utf-8").split("\n")[0:-1]
dic = {a: 0 for a in devices}


def query_checkbuttons():
    str = ''
    for key, value in dic.items():
        if value.get() != 0:
            str = str + key[23:32] + '\n'
    str = str[:-1]
    f = open(devfile, "w")
    f.write(str)
    f.close()
    root.destroy()


for key in dic:
    dic[key] = IntVar()
    aCheckButton = Checkbutton(root, text=key, variable=dic[key])
    aCheckButton.grid(sticky='w')

submitButton = Button(root, text="Сохранить", command=query_checkbuttons)
submitButton.grid()
root.resizable(0, 0)
root.mainloop()
