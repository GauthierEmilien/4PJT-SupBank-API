from _tkinter import TclError
from tkinter import END
from tkinter import Menu
from tkinter import SEL


class ClickActions:

    def __init__(self):
        pass

    def r_clicker(self, e):
        """
        right click context menu for all Tk Entry and Text widgets
        """

        try:
            def r_click_select_all(e):
                e.widget.event_generate('<Control-a>')
                e.widget.tag_add(SEL, "1.0", END)

            def r_click_copy(e, apnd=0):
                e.widget.event_generate('<Control-c>')

            def r_click_cut(e):
                e.widget.event_generate('<Control-x>')

            def r_click_paste(e):
                e.widget.event_generate('<Control-v>')

            e.widget.focus()

            nclst = [
                (' Tout selectionner', lambda e=e: r_click_select_all(e)),
                (' Couper', lambda e=e: r_click_cut(e)),
                (' Copier', lambda e=e: r_click_copy(e)),
                (' Coller', lambda e=e: r_click_paste(e)),
            ]

            rmenu = Menu(None, tearoff=0, takefocus=0)

            for (txt, cmd) in nclst:
                rmenu.add_command(label=txt, command=cmd)

            rmenu.tk_popup(e.x_root + 40, e.y_root + 10, entry="0")

        except TclError:
            print(' - rClick menu, something wrong')
            pass

        return "break"

    def r_clickbinder(self, r):

        try:
            for b in ['Text', 'Entry', 'Listbox', 'Label']:  #
                r.bind_class(b, sequence='<Button-3>',
                             func=self.r_clicker, add='')
        except TclError:
            print(' - r_clickbinder, something wrong')
            pass
