import re
from tkinter import CENTER
from tkinter import E
from tkinter import N
from tkinter import S
from tkinter import Toplevel
from tkinter import W
from tkinter import ttk


class AskIp(Toplevel):

    def __init__(self, parent, ask: str, title=None):

        Toplevel.__init__(self, parent)
        self.transient(parent)
        self.title("Blocked fields")
        self.configure(bg='white')

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        self.askstring(ask)

        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def askstring(self, ask: str):
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, sticky=N + S + E + W)
        label = ttk.Label(frame, text=ask, anchor=CENTER)
        label.grid()

        entry = ttk.Entry(frame, text='')
        entry.grid()

        button_ok = ttk.Button(frame, text='Valider', command=lambda: self.ok(entry.get()))
        button_ok.grid()

        self.bind("<Return>", (lambda event: self.ok(entry.get())))

    def ok(self, event=None):

        self.result = event

        if not self.validate():
            self.parent.focus_set()  # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel(event)

    def cancel(self, event=None):
        self.result = event

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):
        p = re.compile(r'(\d{1,3}\.){3}\d{1,3}')

        return p.match(self.result)  # override

    def apply(self):

        pass  # override

    def askvalue(self):
        return self.result
