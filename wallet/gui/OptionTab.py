import re
from tkinter import CENTER
from tkinter import E
from tkinter import N
from tkinter import S
from tkinter import W
from tkinter import ttk

from wallet.gui.TabFrame import TabFrame


class OptionTab(TabFrame):
    """
    Création du tab "Portefeuille"
    """

    def __init__(self, parent, **args):
        TabFrame.__init__(self, parent, **args)
        self.__ip_server_ip = ttk.Entry(self, width=15, validate='key',
                                    validatecommand=(self.register(self.isValidKeyIp), '%S'))
        self.setIpServerIP()

        self.grid_columnconfigure(0, weight=10)
        self.grid_columnconfigure(2, weight=10)

    def setIpServerIP(self):
        l_ip_server_ip = ttk.Label(self, text='IP du serveurIP', anchor=CENTER)
        l_ip_server_ip.grid(row=0, column=1, sticky=N + S + E + W)
        self.__ip_server_ip.grid(row=1, column=1, sticky=N + S + E + W)
        value = self.__ip_server_ip.get()
        self.isValidIp(value)

    def isValidIp(self, ip: str):
        p = re.compile(r'(\d{1,3}\.){3}\d{1,3}')
        if ip:
            self.logger.info(p.match(ip))
            return p.match(ip)

    @staticmethod
    def isValidKeyIp(value: str):
        if value.isdigit() or value == '.':
            return True
        return False
