from tkinter import Tk, ttk
from PIL import Image, ImageTk

class UI:
    def __init__(self, root) -> None:
        self._root = root

    def start(self):
        label = ttk.Label(master=self._root, text="Hello world!")
        label.pack()

window = Tk()
window.title("Tkinter example")

ui = UI(window)
ui.start()
window.mainloop()