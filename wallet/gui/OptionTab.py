import re
from tkinter import CENTER
from tkinter import E
from tkinter import END
from tkinter import N
from tkinter import NORMAL
from tkinter import S
from tkinter import SUNKEN
from tkinter import W
from tkinter import ttk

from wallet.gui.TabFrame import TabFrame


# TODO : Finir le mode nuit

class OptionTab(TabFrame):
    """
    Création du tab "Portefeuille"
    """

    def __init__(self, parent, **args):
        TabFrame.__init__(self, parent.tab_control, **args)
        self.parent = parent
        self.__ip_server_ip = ttk.Entry(self, width=15, justify=CENTER, validate='all',
                                        validatecommand=(self.register(self.is_valid_key_ip), '%S'))
        self.set_ip_server_ip()

        self.set_gui_theme()

        self.grid_columnconfigure(0, weight=10)
        self.grid_columnconfigure(2, weight=10)

    def set_ip_server_ip(self):
        l_ip_server_ip = ttk.Label(self, text='IP du serveurIP', anchor=CENTER)
        l_ip_server_ip.grid(row=0, column=1, sticky=N + S + E + W)
        self.__ip_server_ip.grid(row=1, column=1, sticky=N + S + E + W)
        value = self.__ip_server_ip.get()
        self.is_valid_ip(value)

    def is_valid_ip(self, ip: str):
        p = re.compile(r'(\d{1,3}\.){3}\d{1,3}')
        if ip:
            self.logger.info(p.match(ip))
            return p.match(ip)

    @staticmethod
    def is_valid_key_ip(value: str):
        if value.isdigit() or value == '.':
            return True
        return False

    def set_ip(self, ip: str):
        self.setvar('state', NORMAL)
        self.__ip_server_ip.delete(0, END)
        for v in ip:
            self.__ip_server_ip.insert(0, v)

    def set_gui_theme(self):
        frame = ttk.Frame(self, padding=5, relief=SUNKEN)
        frame.grid(row=2, column=1, sticky=N + S + E + W)

        l_ip_server_ip = ttk.Label(frame, text='Changer le mode', anchor=CENTER)
        l_ip_server_ip.grid(row=2, column=1, sticky=N + S + E + W)

        radio_button_jour = ttk.Radiobutton(frame, text='Thème jour', value='arc',
                                            command=lambda: self.set_theme_jour())
        radio_button_jour.grid(row=3, column=1, sticky=N + S + E + W)
        radio_button_jour.invoke()

        radio_button_nuit = ttk.Radiobutton(frame, text='Thème nuit', value='equilux',
                                            command=lambda: self.set_theme_nuit())
        radio_button_nuit.grid(row=4, column=1, sticky=N + S + E + W)

    def set_theme_jour(self):
        self.parent.style.set_theme('arc')

    def set_theme_nuit(self):
        self.parent.style.set_theme('equilux')
        # self.parent.configure(bg='black', background="black", foreground="white")
