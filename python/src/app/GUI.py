from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo


class GUI:

    def __init__(self):
        self.__fenetre: Tk = Tk()
        self.__entree: Entry = None
        self.__tab_control = ttk.Notebook(self.__fenetre)  # Create Tab Control
        self.__loggerFrame: Frame = None
        self.initGUI()

    def initGUI(self):
        self.initWindow()
        self.setBlockChainFrameTab()
        self.setWalletFrameTab()

    def initWindow(self):
        self.__fenetre.title('XatomeCoin')
        try:
            self.__fenetre.iconbitmap(r'./ressources/Ph03nyx-Super-Mario-Question-Coin.ico')
        except TclError:
            print('Cannot load the icon')
        # img = PhotoImage(file='./ressources/Ph03nyx-Super-Mario-Question-Coin.ico')
        # fenetre.tk.call('wm', 'iconphoto', fenetre._w, img)

    def alert(self):
        showinfo("alerte", "Bravo!")

    def setMenu(self):
        menubar = Menu(self.__fenetre)

        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Créer", command=self.alert)
        menu1.add_command(label="Editer", command=self.alert)
        menu1.add_separator()
        menu1.add_command(label="Quitter", command=self.__fenetre.quit)
        menubar.add_cascade(label="Fichier", menu=menu1)

        menu2 = Menu(menubar, tearoff=0)
        menu2.add_command(label="Couper", command=self.alert)
        menu2.add_command(label="Copier", command=self.alert)
        menu2.add_command(label="Coller", command=self.alert)
        menubar.add_cascade(label="Editer", menu=menu2)

        menu3 = Menu(menubar, tearoff=0)
        menu3.add_command(label="A propos", command=self.alert)
        menubar.add_cascade(label="Aide", menu=menu3)

        self.__fenetre.config(menu=menubar)

    def setBlockChainFrameTab(self):
        tab1 = ttk.Frame(self.__tab_control)  # Create a tab
        bouton = Button(tab1, text="Start mining", command=print('Mining'))
        bouton.pack()
        bouton = Button(tab1, text="Stop mining", command=print('Mining'))
        bouton.pack()
        self.__tab_control.add(tab1, text='BlockChain')  # Add the tab
        self.__tab_control.pack(expand=1, fill="both", side=LEFT)  # Pack to make visible
        self.setLoggerFrame(tab1)
        self.logger('test 1')
        self.logger('test 2')
        self.logger('test 2')
        self.logger('test 2')
        self.logger('test 2')

    def setWalletFrameTab(self):
        tab1 = ttk.Frame(self.__tab_control)  # Create a tab
        self.__tab_control.add(tab1, text='Wallet')  # Add the tab
        self.__tab_control.pack(expand=1, fill="both", side=LEFT)  # Pack to make visible

    # label = Label(fenetre, text="Hello World")
    # label.pack()
    #
    # # bouton de sortie
    # bouton = Button(fenetre, text="Fermer", command=fenetre.quit)
    # bouton.pack()
    #
    # # checkbutton
    # bouton = Checkbutton(fenetre, text="Nouveau?")
    # bouton.pack()
    #
    # p = PanedWindow(fenetre, orient=HORIZONTAL)
    # p.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)
    # p.add(Label(p, text='Volet 1', background='blue', anchor=CENTER))
    # p.add(Label(p, text='Volet 2', background='white', anchor=CENTER))
    # p.add(Label(p, text='Volet 3', background='red', anchor=CENTER))
    # p.pack()
    #
    # Canvas(fenetre, width=250, height=100, bg='ivory').pack(side=TOP, padx=5, pady=5)
    # Button(fenetre, text='Bouton 1').pack(side=LEFT, padx=5, pady=5)
    # Button(fenetre, text='Bouton 2').pack(side=RIGHT, padx=5, pady=5)

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
        self.__loggerFrame.pack(side=BOTTOM)

    def logger(self, log: str):
        Label(self.__loggerFrame, text=log).pack()

    def launchGUI(self):
        self.__fenetre.mainloop()


gui = GUI()
gui.launchGUI()
