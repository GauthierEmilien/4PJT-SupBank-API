from tkinter import CENTER
from tkinter import E
from tkinter import N
from tkinter import S
from tkinter import Toplevel
from tkinter import W
from tkinter import ttk


class AskIp(Toplevel):

    def __init__(self, parent, **args):
        Toplevel.__init__(self, parent, **args)
        self.title("Blocked fields")
        self.configure(bg='white')

    def askstring(self):
        frame = ttk.Frame(self)
        frame.grid(sticky=N + S + E + W)
        label = ttk.Label(frame, text='Impossible de contacter le server IP.\n'
                                      'Entrez l\'ip du server x.x.x.x : ', anchor=CENTER)
        label.grid()

        entry = ttk.Entry(frame, text='')
        entry.grid()

        buttonOk = ttk.Button(frame, text='Valider', command=lambda: self.ok(entry.get()))
        buttonOk.grid()

    def ok(self, value: str):
        print(value)
        self.destroy()
