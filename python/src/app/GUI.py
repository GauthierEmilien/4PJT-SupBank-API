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

class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """

    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', _configure_canvas)


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
# TODO: passer de pack à grid
# Mining logs
m_logger_frame = VerticalScrolledFrame(tab_blockchaine, height=75)
m_logger_frame.pack(side=BOTTOM, fill=X, expand=False)
m_logger_frame.pack_propagate(False)

# Mining actions
buttonStartMining = Button(tab_blockchaine, text="Start mining", command=lambda: buttonStartMiningAction())
buttonStartMining.pack(side=LEFT, padx=10, pady=5)
buttonStopMining = Button(tab_blockchaine, text="Stop mining", command=lambda: buttonStopMiningAction())

# Pending transactions
label = Label(tab_blockchaine, text='Pending transaction', background='red', anchor=CENTER)
label.pack(side=RIGHT, padx=5, pady=5)
label = Label(tab_blockchaine, text='Block généré', background='red', anchor=CENTER)
label.pack(side=RIGHT, padx=5, pady=5)

tab_control.add(tab_blockchaine, text='BlockChain')
tab_control.pack(expand=1, fill="both", side=LEFT)


def buttonStartMiningAction():
    mLogger('Mining in progress')
    buttonStartMining.forget()
    buttonStopMining.pack(side=LEFT, padx=5, pady=5)


def buttonStopMiningAction():
    mLogger('Stop Mining')
    buttonStopMining.forget()
    buttonStartMining.pack(side=LEFT, padx=5, pady=5)


def mLogger(log: str):
    Label(m_logger_frame.interior, text=log).pack(side=BOTTOM)


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

# Montant de mon Portefeuille
l_amount_wallet = Label(tab_wallet, text='Portefeuille', width=20)
l_amount_wallet.grid(row=0, column=2, sticky=N + S + E + W)
amount_wallet = Label(tab_wallet, text='200')
amount_wallet.grid(row=1, column=2, sticky=N + S + E + W)

# Charger la clé public du destinataire
l_public_key = Label(tab_wallet, text='Clé public destinataire')
l_public_key.grid(row=3, column=0, sticky=N + S + E + W)
public_key = Text(tab_wallet, height=5)
public_key.grid(row=4, column=0, sticky=N + S + E + W)

button_open_public = Button(tab_wallet, text='Ouvrir une clé public', command=lambda: getPublicKeyFile(public_key))
button_open_public.grid(row=4, column=1, padx=5, pady=5, sticky=N + S + E + W)

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
w_logger_frame = VerticalScrolledFrame(tab_wallet, height=50)
w_logger_frame.grid(row=9, column=0, columnspan=3, sticky=N + S + E + W)
tab_wallet.grid_rowconfigure(9, weight=1)

tab_control.add(tab_wallet, text='Wallet')
tab_control.pack(expand=1, fill="both", side=LEFT)

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
    wLogger('Création de la transaction')
    pass


def wLogger(log: str):
    Label(w_logger_frame.interior, text=log).pack(side=BOTTOM)


fenetre.mainloop()
