from tkinter import E
from tkinter import N
from tkinter import S
from tkinter import W
from tkinter import ttk


class MiningButton(ttk.Button):

    def __init__(self, parent, **args):
        ttk.Button.__init__(self, parent, **args)

    def show(self):
        self.grid(row=0, column=0, rowspan=2, columnspan=4, padx=5, pady=5, sticky=N + S + E + W)

    def hide(self):
        self.grid_forget()
