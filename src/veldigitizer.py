from tkinter import Tk, ttk, Canvas
from PIL import Image, ImageTk

class App(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Veldigitizer")
        self.geometry("2000x600")

        self.ui = UI(self)

        self.mainloop()

class UI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="Model", font="Calibri 24").pack()
        self.pack()

        image = Image.open("../fennolora_d-i.png")
        global image_tk
        image_tk = ImageTk.PhotoImage(image)
        self.canvas = Canvas(self, width=image.size[0], height=image.size[1])
        self.canvas.create_image((0,0), anchor="nw", image=image_tk)
        self.canvas.pack()

        global prev
        prev = 0
        def get_coords(event):
            x, y = event.x, event.y
            print(x, y)
            r = 4
            global prev
            prev = self.canvas.create_oval(x-r,y-r,x+r,y+r, fill="blue", outline="blue")

        self.canvas.bind("<Button-1>", get_coords)

        def del_prev():
            global prev
            print(prev)
            if prev > 1:
                self.canvas.delete(prev)
                prev -= 1
            else:
                print("Already at oldest exchange!")

        self.undo = ttk.Button(self, text="Undo", command=del_prev)
        self.undo.pack()

app = App()
