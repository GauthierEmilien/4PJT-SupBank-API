from gui.GUI import GUI
import asyncio

if __name__ == '__main__':
    fenetre = GUI()
    # loop = asyncio.get_event_loop()
    # mainloop = loop.run_in_executor(None, fenetre.mainloop)
    # loop.run_until_complete(mainloop)
    fenetre.mainloop()
