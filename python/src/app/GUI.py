from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo


# TODO: Gerer les bonnes actions sur les boutons
# TODO: Passer sous class ?
# TODO: Améliorer le responsive
# TODO: Changer les couleurs de l'interface


class GUI:

    def __init__(self):
        self.__fenetre: Tk = Tk()
        self.__entree: Entry = None
        self.__tab_control = ttk.Notebook(self.__fenetre)  # Create Tab Control
        self.__loggerFrame: Frame = None
        self.buttonStartMining: Button = None
        self.buttonStopMining: Button = None
        self.initGUI()

    def initGUI(self):
        self.initWindow()
        self.setBlockChainFrameTab()
        self.setWalletFrameTab()

    def initWindow(self):
        self.__fenetre.title('XatomeCoin')
        self.__fenetre.configure(bg='white')
        try:
            self.__fenetre.iconbitmap(r'./ressources/Ph03nyx-Super-Mario-Question-Coin.ico')
        except TclError:
            print('Cannot load the icon')
        # img = PhotoImage(file='./ressources/Ph03nyx-Super-Mario-Question-Coin.ico')
        # fenetre.tk.call('wm', 'iconphoto', fenetre._w, img)

    def alert(self):
        showinfo("alerte", "Bravo!")

    # def setMenu(self):
    #     menubar = Menu(self.__fenetre)
    #
    #     menu1 = Menu(menubar, tearoff=0)
    #     menu1.add_command(label="Créer", command=self.alert)
    #     menu1.add_command(label="Editer", command=self.alert)
    #     menu1.add_separator()
    #     menu1.add_command(label="Quitter", command=self.__fenetre.quit)
    #     menubar.add_cascade(label="Fichier", menu=menu1)
    #
    #     menu2 = Menu(menubar, tearoff=0)
    #     menu2.add_command(label="Couper", command=self.alert)
    #     menu2.add_command(label="Copier", command=self.alert)
    #     menu2.add_command(label="Coller", command=self.alert)
    #     menubar.add_cascade(label="Editer", menu=menu2)
    #
    #     menu3 = Menu(menubar, tearoff=0)
    #     menu3.add_command(label="A propos", command=self.alert)
    #     menubar.add_cascade(label="Aide", menu=menu3)
    #
    #     self.__fenetre.config(menu=menubar)

    def setBlockChainFrameTab(self):
        tab1 = Frame(self.__tab_control, width=300, height=300, background="white")  # Create a tab
        tab1.grid(row=0, column=0, sticky='nsew')
        # Mining logs
        self.setLoggerFrame(tab1)

        # Mining actions
        self.buttonStartMining = Button(tab1, text="Start mining", command=lambda: self.buttonStartMiningAction())
        self.buttonStartMining.grid(row=0, rowspan=2, padx=10, pady=5)

        self.buttonStopMining = Button(tab1, text="Stop mining", command=lambda: self.buttonStopMiningAction())

        # Pending transactions
        label = Label(tab1, text='Pending transaction', background='red', anchor=CENTER)
        label.grid(row=0, column=1, padx=5, pady=5)
        label = Label(tab1, text='Block généré', background='red', anchor=CENTER)
        label.grid(row=1, column=1, padx=5, pady=5)

        self.__tab_control.add(tab1, text='BlockChain')  # Add the tab
        self.__tab_control.pack(expand=1, fill="both", side=LEFT)  # Pack to make visible

    def buttonStartMiningAction(self):
        self.logger('Mining in progress')
        self.buttonStartMining.forget()
        self.buttonStopMining.grid(row=0, rowspan=2, padx=10, pady=5)

    def buttonStopMiningAction(self):
        self.logger('Stop Mining')
        self.buttonStopMining.forget()
        self.buttonStartMining.grid(row=0, rowspan=2, padx=10, pady=5)

    def setWalletFrameTab(self):
        tab1 = Frame(self.__tab_control)  # Create a tab
        self.__tab_control.add(tab1, text='Wallet')  # Add the tab
        self.__tab_control.pack(expand=1, fill="both", side=LEFT)  # Pack to make visible

    def recupere(self):
        showinfo("Alerte", self.__entree.get())

    def getFile(self):
        value = StringVar()
        value.set("Valeur")
        self.__entree = Entry(self.__fenetre, textvariable=value, width=30)
        self.__entree.pack()

        bouton = Button(self.__fenetre, text="Valider", command=self.recupere)
        bouton.pack()

        filepath = askopenfilename(title="Ouvrir une image", filetypes=[('png files', '.png'), ('all files', '.*')])
        photo = PhotoImage(file=filepath)
        canvas = Canvas(self.__fenetre, width=photo.width(), height=photo.height(), bg="yellow")
        canvas.create_image(0, 0, anchor=NW, image=photo)
        canvas.pack()

    def setLoggerFrame(self, parent_frame: Frame):
        self.__loggerFrame = Frame(parent_frame, borderwidth=2, relief=GROOVE, height=10)
        self.__loggerFrame.grid(row=2, columnspan=2)

    def logger(self, log: str):
        Label(self.__loggerFrame, text=log).pack()

    def launchGUI(self):
        self.__fenetre.mainloop()


# gui = GUI()
# gui.launchGUI()

###########

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
tab_blockchaine = Frame(tab_control, width=300, height=300, background="white")  # Create a tab
tab_blockchaine.pack()

# Mining logs
mining_logger = Logger(tab_blockchaine)
mining_logger.grid(row=10, column=0, columnspan=10, sticky=S + E + W)
tab_blockchaine.grid_rowconfigure(10, weight=2)

# Mining actions
buttonStartMining = Button(tab_blockchaine, text="Start mining", command=lambda: buttonStartMiningAction())
buttonStartMining.grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky=N + S + E + W)
buttonStopMining = Button(tab_blockchaine, text="Stop mining", command=lambda: buttonStopMiningAction())

# Pending transactions
label_pending = Label(tab_blockchaine, text='Pending transaction', background='red', anchor=CENTER)
label_pending.grid(row=0, column=1, padx=5, pady=5, sticky=N + S + E + W)
pending_transactions_frame = Frame(tab_blockchaine)
pending_transactions_frame.grid(row=1, column=1, rowspan=8, padx=5, pady=5, sticky=N + S + E + W)
pending_transactions = TextAndScrollBar(pending_transactions_frame, state='disabled')

# Generated blocks
label_blocks = Label(tab_blockchaine, text='Block généré', background='red', anchor=CENTER)
label_blocks.grid(row=0, column=2, padx=5, pady=5, sticky=N + S + E + W)
generated_blocks_frame = Frame(tab_blockchaine)
generated_blocks_frame.grid(row=1, column=2, rowspan=8, padx=5, pady=5, sticky=N + S + E + W)
generated_blocks = TextAndScrollBar(generated_blocks_frame, state='disabled')

tab_control.add(tab_blockchaine, text='BlockChain')
tab_control.pack(expand=1, fill="both", side=LEFT)

"""
Initialisation de la grille (pour le redimentionnement)
"""
tab_blockchaine.grid_columnconfigure(0, weight=4)
tab_blockchaine.grid_columnconfigure(1, weight=2)
tab_blockchaine.grid_columnconfigure(2, weight=2)


def buttonStartMiningAction():
    mining_logger.log('Mining in progress')
    buttonStartMining.grid_forget()
    buttonStopMining.grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky=N + S + E + W)


def buttonStopMiningAction():
    mining_logger.log('Stop Mining')
    buttonStopMining.grid_forget()
    buttonStartMining.grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky=N + S + E + W)


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
button_open_private = Button(tab_wallet, text='Ouvrir une clé privée',
                             command=lambda: getPrivateKeyFile(private_wallet_key))
button_open_private.grid(row=1, column=1, padx=5, pady=5, sticky=N + S + E + W)

# Générer une paire de clé
l_key_gen = Label(tab_wallet, text='Générer une paire de clé', width=20)
l_key_gen.grid(row=0, column=2, sticky=N + S + E + W)
key_gen = Button(tab_wallet, text='Générer une paire de clé', command=lambda: generateKeys())
key_gen.grid(row=1, column=2, padx=5, pady=5, sticky=N + S + E + W)

# Charger la clé public du destinataire
l_public_key = Label(tab_wallet, text='Clé public destinataire')
l_public_key.grid(row=3, column=0, sticky=N + S + E + W)
public_key = Text(tab_wallet, height=5)
public_key.grid(row=4, column=0, sticky=N + S + E + W)

button_open_public = Button(tab_wallet, text='Ouvrir une clé public', command=lambda: getPublicKeyFile(public_key))
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
pass

"""
Initialisation de la grille (pour le redimentionnement)
"""
tab_wallet.grid_columnconfigure(0, weight=4)
tab_wallet.grid_columnconfigure(1, weight=2)
tab_wallet.grid_columnconfigure(2, weight=2)


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
    pass


def generateKeys():
    wallet_logger.warning('Faire la génération de la paire de clé, demander ou enregistrer la paire de clé')


fenetre.mainloop()
