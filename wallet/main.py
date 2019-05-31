from gui.GUI import GUI

if __name__ == '__main__':
    # # fenetre = GUI()
    # # ip = fenetre.getIpServerIP()
    #
    # # ip = str(input('Which ip : '))
    # # pa défaut contact le localhost
    # client_server_ip = Client('127.0.0.1', 'server_ip_connection')
    #
    # client_server_ip.start()
    # # client_server_ip.join()
    # node_ip = client_server_ip.get_node_ip()
    # server = Server()
    # server.start(node_ip, 8000)

    fenetre = GUI()
    # fenetre.setClient(client_server_ip)
    # fenetre.setServer(server)
    fenetre.mainloop()

#
# from threading import Thread
# from time import sleep
# from tkinter import Button
# from tkinter import Label
# from tkinter import Tk
#
#
# class App(Tk):
#     def __init__(self):
#         Tk.__init__(self)
#         self.label = Label(self, text="Stopped.")
#         self.label.pack()
#         self.play_button = Button(self, text="Play", command=self.play)
#         self.play_button.pack(side="left", padx=2, pady=2)
#         self.stop_button = Button(self, text="Stop", command=self.stop)
#         self.stop_button.pack(side="left", padx=2, pady=2)
#         self._thread, self._pause, self._stop = None, False, True
#
#     def action(self):
#         for i in range(1000):
#             if self._stop:
#                 break
#             while self._pause:
#                 self.label["text"] = "Pause... (count: {})".format(i)
#                 sleep(0.1)
#             self.label["text"] = "Playing... (count: {})".format(i)
#             sleep(0.1)
#         self.label["text"] = "Stopped."
#
#     def play(self):
#         if self._thread is None:
#             self._stop = False
#             self._thread = Thread(target=self.action)
#             self._thread.start()
#         self._pause = False
#         self.play_button.configure(text="Pause", command=self.pause)
#
#     def pause(self):
#         self._pause = True
#         self.play_button.configure(text="Play", command=self.play)
#
#     def stop(self):
#         if self._thread is not None:
#             self._thread, self._pause, self._stop = None, False, True
#         self.play_button.configure(text="Play", command=self.play)
#
#
# App().mainloop()
