from tkinter import DISABLED
from tkinter import END
from tkinter import NORMAL
from tkinter import ttk

from wallet.gui.TextAndScrollBar import TextAndScrollBar


# TODO: Scroll auto vers le bas pour les logs


class Logger(ttk.Frame):

    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, **kw)
        self.__loggerText = TextAndScrollBar(self, state='disabled', height=8)
        self.__loggerText.tag_config("log", foreground="black")
        self.__loggerText.tag_config("success", foreground="green")
        self.__loggerText.tag_config("warning", foreground="orange")
        self.__loggerText.tag_config("error", foreground="red")
        # self.grid(row=9, column=0, columnspan=3, sticky=N + S + E + W)

    def __commonLog(self, log: str, color: str):
        self.__loggerText.config(state=NORMAL)
        self.__loggerText.insert(END, log + '\n', color)
        self.__loggerText.config(state=DISABLED)

    def log(self, log: str):
        self.__commonLog(log, 'log')

    def success(self, log: str):
        self.__commonLog(log, 'success')

    def warning(self, log: str):
        self.__commonLog(log, 'warning')

    def error(self, log: str):
        self.__commonLog(log, 'error')
