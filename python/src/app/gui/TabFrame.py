from tkinter import E
from tkinter import Frame
from tkinter import S
from tkinter import W

from gui.Logger import Logger


class TabFrame(Frame):

    def __init__(self, parent, **args):
        Frame.__init__(self, parent, **args)
        self.logger = Logger(self)

    def initLogger(self):
        # Mining logs
        self.logger.grid(row=10, column=0, columnspan=4, sticky=S + E + W)
        self.grid_rowconfigure(10, weight=2)
