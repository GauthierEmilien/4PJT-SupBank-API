import re
from tkinter import CENTER
from tkinter import DISABLED
from tkinter import END
from tkinter import NORMAL
from tkinter import NSEW
from tkinter import SUNKEN
from tkinter import ttk

from gui.TabFrame import TabFrame


class TabOption(TabFrame):
    """
    Création du tab "Portefeuille"
    """

    def __init__(self, parent, **args):
        TabFrame.__init__(self, parent.tab_control, **args)
        self.parent = parent
        self.currrent_theme = 'arc'
        self.__ip_server_ip = ttk.Entry(self, width=15, justify=CENTER, validate='all',
                                        validatecommand=(self.register(self.__is_valid_key_ip), '%S'))
        self.__ip_server_ip_group()

        self.__gui_theme_group_buttons()

        self.grid_columnconfigure(0, weight=10)
        self.grid_columnconfigure(2, weight=10)

    """
    IP part
    """

    def __ip_server_ip_group(self):
        l_ip_server_ip = ttk.Label(self, text='IP du serveurIP', anchor=CENTER)
        l_ip_server_ip.grid(row=0, column=1, sticky=NSEW)
        self.__ip_server_ip.grid(row=1, column=1, sticky=NSEW)
        value = self.__ip_server_ip.get()
        self.__is_valid_ip(value)

    def __is_valid_ip(self, ip: str):
        p = re.compile(r'(\d{1,3}\.){3}\d{1,3}')
        if ip:
            self.logger.info(p.match(ip))
            return p.match(ip)

    def __is_valid_key_ip(self, value: str):
        if value.isdigit() or value == '.':
            return True
        return False

    def set_ip(self, ip: str):
        self.__ip_server_ip.config(state=NORMAL)
        self.__delete_ip()
        for v in ip:
            self.__ip_server_ip.insert(END, v)
        self.__ip_server_ip.config(state=DISABLED)

    def __delete_ip(self):
        for i in range(len(self.__ip_server_ip.get())):
            self.__ip_server_ip.delete(0)

    """
    Theme part
    """

    def __gui_theme_group_buttons(self):
        frame = ttk.Frame(self, padding=5, relief=SUNKEN)
        frame.grid(row=2, column=1, sticky=NSEW)

        l_ip_server_ip = ttk.Label(frame, text='Changer le mode', anchor=CENTER)
        l_ip_server_ip.grid(row=2, column=1, sticky=NSEW)

        radio_button_jour = ttk.Radiobutton(frame, text='Thème jour', value='arc',
                                            command=lambda: self.set_theme_jour())
        radio_button_jour.grid(row=3, column=1, sticky=NSEW)
        radio_button_jour.invoke()

        radio_button_nuit = ttk.Radiobutton(frame, text='Thème nuit', value='equilux',
                                            command=lambda: self.set_theme_nuit())
        radio_button_nuit.grid(row=4, column=1, sticky=NSEW)

    def set_theme_jour(self):
        self.currrent_theme = 'arc'
        self.parent.style.set_theme('arc')
        self.__set_text_widget_theme(self.parent.winfo_children(), background='white', foreground='grey')

    def set_theme_nuit(self):
        self.currrent_theme = 'equilux'
        self.parent.style.set_theme('equilux')
        self.__set_text_widget_theme(self.parent.winfo_children(), background='#464646', foreground='#9a9a9a')

    def __set_text_widget_theme(self, childs, **args):
        for child in childs:
            if child.widgetName == 'ttk::frame' or child.widgetName == 'ttk::notebook' or child.widgetName == 'text':
                self.__set_text_widget_theme(child.winfo_children(), **args)
            if child.widgetName == 'text':
                child.configure({**args})

    def udtade_theme(self):
        if self.currrent_theme == 'equilux':
            self.set_theme_nuit()
        else:
            self.set_theme_jour()
