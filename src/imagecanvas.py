from tkinter import Canvas
from PIL import ImageTk

class Image_canvas(Canvas):
    def __init__(self, parent, image):
        super().__init__(parent, width=image.size[0], height=image.size[1])
        self.image_tk = ImageTk.PhotoImage(image)
        self.create_image((0,0), anchor="nw", image=self.image_tk)
        self.pack()
        self.scale_prevs = []
        self.vel_prevs = []

    def add_scale_oval(self, x, y):
        r = 4
        col = "blue"
        self.scale_prevs.append(self.create_oval(x-r,y-r,x+r,y+r, fill=col, outline=col))

    def add_vel_oval(self, x, y):
        r = 4
        col = "red"
        self.vel_prevs.append(self.create_oval(x-r,y-r,x+r,y+r, fill=col, outline=col))

    def delete_oval(self):
        self.delete(self.vel_prevs.pop())

    def del_all_ovals(self):
        for _ in range(len(self.scale_prevs)):
            self.delete(self.scale_prevs.pop())
        for _ in range(len(self.vel_prevs)):
            self.delete(self.vel_prevs.pop())