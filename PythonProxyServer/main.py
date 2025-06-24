from Proxy import Proxy
from GUI import GUI
import tkinter


def main():
    proxy = Proxy()

    # Used to communicate with proxy and vice versa
    g = GUI(proxy)
    proxy.start(g)


button1 = None
button2 = None
flag = True


def func():
    global flag
    flag = not flag

    button1.config(state=("disabled" if not flag else "normal"))
    button2.config(state=("normal" if not flag else "disabled"))

    # button1.pack()
    # button2.pack()


def test():
    global button1, button2
    root = tkinter.Tk()
    button1 = tkinter.Button(root, command=func, state="normal", text="button1")
    button2 = tkinter.Button(root, command=func, state="disabled", text="button2")

    button1.pack()
    button2.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
