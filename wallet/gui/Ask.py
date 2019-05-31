from tkinter import Toplevel


class Ask(Toplevel):

    def __init__(self, parent, ask: str = None, title=None):

        Toplevel.__init__(self, parent)
        self.transient(parent)
        self.title(title)
        self.configure(bg='white')

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        self.askstring(ask)

        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def askstring(self, ask: str):
        pass

    def ok(self, event=None):

        self.result = event

        if not self.validate():
            self.parent.focus_set()  # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel(event)

    def cancel(self, event=None):
        self.result = event

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):
        return True  # override

    def apply(self):
        pass  # override

    def askvalue(self):
        return self.result
