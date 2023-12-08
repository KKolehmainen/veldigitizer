from tkinter import Tk
from ui import UI

class App(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Veldigitizer")
        self.geometry("2000x600")
        self.ui = UI(self)

        self.mainloop()



if __name__ == "__main__":
    app = App()
