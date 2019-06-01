from tkinter import E
from tkinter import END
from tkinter import INSERT
from tkinter import N
from tkinter import S
from tkinter import Text
from tkinter import W
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile

from Cryptodome.PublicKey import RSA

from gui.Ask import Ask


class AskPrivateKey(Ask):

    def __init__(self, parent, ask: str = None, title=None):
        Ask.__init__(self, parent, ask=ask, title=title)

    # construction hooks

    def askstring(self, ask: str):
        frame = ttk.Frame(self)
        frame.grid()
        l_private_wallet_key = ttk.Label(frame, text='Clé privée', padding=10)
        l_private_wallet_key.grid(row=0, column=0, sticky=N + S + E + W)

        private_wallet_key = Text(frame, height=5)
        private_wallet_key.grid(row=1, column=0, sticky=N + S + E + W)

        button_open_private = ttk.Button(frame, text='Ouvrir une clé privée', width=25,
                                         command=lambda: self.__getPrivateKeyFile(private_wallet_key))
        button_open_private.grid(row=1, column=1, padx=5, pady=5, sticky=N + S + E + W)

        key_gen = ttk.Button(frame, text='Générer une paire de clé', width=25,
                             command=lambda: self.__generateKeys(private_wallet_key))
        key_gen.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)

        button_ok = ttk.Button(frame, text='Valider', command=lambda: self.ok(private_wallet_key.get("1.0", END)))
        button_ok.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)

        self.bind("<Return>", (lambda event: self.ok(private_wallet_key.get("1.0", END))))

    def __getPrivateKeyFile(self, entry_field: Text):
        filepath = askopenfilename(title="Ouvrir une clé privée",
                                   filetypes=[('Fichiers pem', '.pem'), ('Tous les fichiers', '*')])
        if filepath:
            with open(filepath) as file:
                value = file.read()
                entry_field.delete('1.0', END)
                entry_field.insert(INSERT, value)

    def __generateKeys(self, private_wallet_key):
        if len(private_wallet_key.get("1.0", END)) > 800:
            if not messagebox.askyesno("Question", "Une clé privée existe déjà.\n"
                                                   "Générer quand même une nouvelle paire ?"):
                return
        # self.logger.log('Génération de la paire de clé en cours')

        private_wallet_key.delete('1.0', END)
        private_key = RSA.generate(1024)
        private_wallet_key.insert(INSERT, private_key.export_key())

        self.__file_save(private_wallet_key)

    def __file_save(self, private_wallet_key):
        f = asksaveasfile(mode='w', defaultextension=".pem")
        if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        text2save = str(private_wallet_key.get(1.0, END))  # starts from `1.0`, not `0.0`
        f.write(text2save)
        f.close()  # `()` was missing.

    #
    # command hooks

    def validate(self):
        return len(self.result) > 800
