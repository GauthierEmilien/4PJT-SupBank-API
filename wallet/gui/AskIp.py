import re
from tkinter import CENTER
from tkinter import E
from tkinter import N
from tkinter import S
from tkinter import W
from tkinter import ttk

from gui.Ask import Ask


class AskIp(Ask):

    def __init__(self, parent, ask: str = None, title=None):
        Ask.__init__(self, parent, ask=ask, title=title)

    #
    # construction hooks

    def ask_string(self, ask: str):
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, sticky=N + S + E + W)
        label = ttk.Label(frame, text=ask, anchor=CENTER)
        label.grid()

        entry = ttk.Entry(frame, text='')
        entry.grid()
        entry.focus()

        button_ok = ttk.Button(frame, text='Valider', command=lambda: self.ok(entry.get()))
        button_ok.grid()

        self.bind("<Return>", (lambda event: self.ok(entry.get())))

    #
    # command hooks

    def validate(self):
        p = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')

        return p.match(self.result)  # override
