from tkinter import *
import subprocess
root = Tk()

devices = subprocess.run("lsusb", stdout=subprocess.PIPE).stdout.decode("utf-8").split("\n")[0:-1]
dic = {a: 0 for a in devices}
print(dic)


def query_checkbuttons():
    for key, value in dic.items():
        if value.get() != 0:
            print(key)

for key in dic:
    dic[key] = IntVar()
    aCheckButton = Checkbutton(root, text=key, variable=dic[key])
    aCheckButton.grid(sticky='w')

submitButton = Button(root, text="Submit", command=query_checkbuttons)
submitButton.grid()

root.mainloop()
