from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import askopenfilename


# TODO: Gerer les bonnes actions sur les boutons
# TODO: Passer sous class ?
# TODO: Améliorer le responsive
# TODO: Changer les couleurs de l'interface

class TextAndScrollBar(Text):

    def __init__(self, parent, *args, **kw):
        Text.__init__(self, parent, *args, **kw)
        scrollbar = Scrollbar(parent)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.configure(yscrollcommand=scrollbar.set)
        self.pack(fill=BOTH)


class Logger(Frame):

    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)
        self.__loggerText = TextAndScrollBar(self, state='disabled', height=8)
        self.__loggerText.tag_config("log", foreground="black")
        self.__loggerText.tag_config("warning", foreground="orange")
        self.__loggerText.tag_config("error", foreground="red")
        # self.grid(row=9, column=0, columnspan=3, sticky=N + S + E + W)

    def __commonLog(self, log: str, color: str):
        self.__loggerText.config(state=NORMAL)
        self.__loggerText.insert(END, log + '\n', color)
        self.__loggerText.config(state=DISABLED)

    def log(self, log: str):
        self.__commonLog(log, 'log')

    def warning(self, log: str):
        self.__commonLog(log, 'warning')

    def error(self, log: str):
        self.__commonLog(log, 'error')


"""
Création de la fenêtre
"""
fenetre: Tk = Tk()
fenetre.title('XatomeCoin')
fenetre.configure(bg='white')
try:
    fenetre.iconbitmap(r'./ressources/Ph03nyx-Super-Mario-Question-Coin.ico')
except TclError:
    print('Cannot load the icon')

"""
Création des tab (blockchaine et porte feuille)
"""
tab_control = ttk.Notebook(fenetre)
"""
Création du tab "blockchaine"
"""
tab_blockchaine = Frame(tab_control, width=300, height=300)  # Create a tab
tab_blockchaine.pack()

# Mining logs
mining_logger = Logger(tab_blockchaine)
mining_logger.grid(row=10, column=0, columnspan=4, sticky=S + E + W)
tab_blockchaine.grid_rowconfigure(10, weight=2)

# Mining action
buttonStartMining = Button(tab_blockchaine, text="Start mining", command=lambda: buttonStartMiningAction(), height=2)
buttonStartMining.grid(row=0, column=0, rowspan=2, columnspan=3, padx=5, pady=5, sticky=N + S + E + W)
buttonStopMining = Button(tab_blockchaine, text="Stop mining", command=lambda: buttonStopMiningAction(), height=2)

# Pending transactions
label_pending = Label(tab_blockchaine, text='Pending transaction', background='red', anchor=CENTER)
label_pending.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)
pending_transactions_frame = Frame(tab_blockchaine)
pending_transactions_frame.grid(row=3, column=0, rowspan=6, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)
pending_transactions = TextAndScrollBar(pending_transactions_frame, state='disabled')

# Generated blocks
label_blocks = Label(tab_blockchaine, text='Block généré', background='red', anchor=CENTER)
label_blocks.grid(row=2, column=2, padx=5, pady=5, sticky=N + S + E + W)
generated_blocks_frame = Frame(tab_blockchaine)
generated_blocks_frame.grid(row=3, column=2, rowspan=6, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)
generated_blocks = TextAndScrollBar(generated_blocks_frame, state='disabled')

tab_control.add(tab_blockchaine, text='BlockChain')
tab_control.pack(expand=1, fill="both", side=LEFT)

"""
Initialisation de la grille (pour le redimentionnement)
"""
tab_blockchaine.grid_columnconfigure(0, weight=1)
tab_blockchaine.grid_columnconfigure(1, weight=5)
tab_blockchaine.grid_columnconfigure(2, weight=5)


def buttonStartMiningAction():
    mining_logger.log('Mining in progress')
    buttonStartMining.grid_forget()
    buttonStopMining.grid(row=0, column=0, rowspan=2, columnspan=3, padx=5, pady=5, sticky=N + S + E + W)


def buttonStopMiningAction():
    mining_logger.log('Stop Mining')
    buttonStopMining.grid_forget()
    buttonStartMining.grid(row=0, column=0, rowspan=2, columnspan=3, padx=5, pady=5, sticky=N + S + E + W)


"""
Création du tab "Portefeuille"
"""
tab_wallet = Frame(tab_control)
tab_wallet.pack(expand=1, fill="both", side=LEFT)

# Charger une clé privée
l_private_wallet_key = Label(tab_wallet, text='Clé privée')
l_private_wallet_key.grid(row=0, column=0, sticky=N + S + E + W)
private_wallet_key = Text(tab_wallet, height=5)
private_wallet_key.grid(row=1, column=0, sticky=N + S + E + W)
button_open_private = Button(tab_wallet, text='Ouvrir une clé privée', width=25,
                             command=lambda: getPrivateKeyFile(private_wallet_key))
button_open_private.grid(row=1, column=1, padx=5, pady=5, sticky=N + S + E + W)

# Générer une paire de clé
l_key_gen = Label(tab_wallet, text='Générer une paire de clé', width=20)
l_key_gen.grid(row=0, column=2, sticky=N + S + E + W)
key_gen = Button(tab_wallet, text='Générer une paire de clé', width=25, command=lambda: generateKeys())
key_gen.grid(row=1, column=2, padx=5, pady=5, sticky=N + S + E + W)

# Charger la clé public du destinataire
l_public_key = Label(tab_wallet, text='Clé public destinataire')
l_public_key.grid(row=3, column=0, sticky=N + S + E + W)
public_key = Text(tab_wallet, height=5)
public_key.grid(row=4, column=0, sticky=N + S + E + W)

button_open_public = Button(tab_wallet, text='Ouvrir une clé public', width=25,
                            command=lambda: getPublicKeyFile(public_key))
button_open_public.grid(row=4, column=1, padx=5, pady=5, sticky=N + S + E + W)

# Montant de mon Portefeuille
l_amount_wallet = Label(tab_wallet, text='Portefeuille', width=20)
l_amount_wallet.grid(row=3, column=2, sticky=N + S + E + W)
amount_wallet = Label(tab_wallet, text='200')
amount_wallet.grid(row=4, column=2, sticky=N + S + E + W)

# Montant de la transaction
l_amount_transaction = Label(tab_wallet, text='Montant de la transaction')
l_amount_transaction.grid(row=6, column=0, sticky=N + S + E + W)
amount_transaction = Entry(tab_wallet, text='')
amount_transaction.grid(row=7, column=0, sticky=N + S + E + W)

# Effectuer la transaction
button_valid_transaction = Button(tab_wallet, text='Valider la transaction', height=2,
                                  command=lambda: createTransaction(private_wallet_key, public_key, amount_transaction))
button_valid_transaction.grid(row=7, column=1, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)

# Log de mes transactions en cours de traitement
wallet_logger = Logger(tab_wallet)
wallet_logger.grid(row=9, column=0, columnspan=3, sticky=S + E + W)
tab_wallet.grid_rowconfigure(9, weight=1)

tab_control.add(tab_wallet, text='Wallet')
tab_control.pack(expand=1, fill="both", side=LEFT)

"""
Initialisation de la grille (pour le redimentionnement)
"""
tab_wallet.grid_columnconfigure(0, weight=4)
tab_wallet.grid_columnconfigure(1, weight=1)
tab_wallet.grid_columnconfigure(2, weight=1)


def getPrivateKeyFile(entry_field: Text):
    filepath = askopenfilename(title="Ouvrir une clé privée", filetypes=[('pem files', '.pem'), ('all files', '*')])
    if filepath:
        with open(filepath) as file:
            value = file.read()
            entry_field.delete('1.0', END)
            entry_field.insert(INSERT, value)


def getPublicKeyFile(entry_field: Text):
    filepath = askopenfilename(title="Ouvrir uneclé public", filetypes=[('pub files', '.pub'), ('all files', '*')])
    if filepath:
        with open(filepath) as file:
            value = file.read()
            entry_field.delete('1.0', END)
            entry_field.insert(INSERT, value)


def createTransaction(private_key: Text, public_key: Text, amount: Entry):
    wallet_logger.log('Création de la transaction')
    wallet_logger.error('Création de la transaction')
    wallet_logger.warning('Création de la transaction')
    wallet_logger.log('Création de la transaction')


def generateKeys():
    if len(private_wallet_key.get("1.0", END)) > 1024 or len(public_key.get("1.0", END)) > 1024:
        if not messagebox.askyesno("Question", "Une clé privée/public existe déjà.\n"
                                               "Générer quand même une nouvelle paire ?"):
            return
    wallet_logger.log('Génération de la paire de clé en cours')

    private_wallet_key.delete('1.0', END)
    private_wallet_key.insert(INSERT, 'Clé privée')

    public_key.delete('1.0', END)
    public_key.insert(INSERT, 'Clé public')

    wallet_logger.log('Fin de la génération des clés')


fenetre.mainloop()
