from tkinter import BOTH
from tkinter import RIGHT
from tkinter import Text
from tkinter import Y
from tkinter import ttk


class TextAndScrollBar(Text):

    def __init__(self, parent, *args, **kw):
        Text.__init__(self, parent, *args, **kw)
        scrollbar = ttk.Scrollbar(parent)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.configure(yscrollcommand=scrollbar.set)
        self.pack(fill=BOTH)
