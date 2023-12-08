import math
from utils import point_at_distance
from tkinter import ttk, Canvas, filedialog
import tkinter as tk
from PIL import Image, ImageTk

class UI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.file_open_window = tk.Toplevel(self)
        self.file_button = tk.Button(self.file_open_window, text="Open model file",
                                command=self.open_file_dialog)
        self.file_button.pack()
        self.wait_window(self.file_open_window)

        ttk.Label(self, text="Model", font="Calibri 24").pack()
        self.pack()

        self.image = Image.open(self.img_file)
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.canvas = Canvas(self, width=self.image.size[0], height=self.image.size[1])
        self.canvas.create_image((0,0), anchor="nw", image=self.image_tk)
        self.canvas.pack()

        self.scale_prevs = []
        self.vel_prevs = []
        self.scale_coords = []
        self.input_coords = []
        self.depths = []
        self.veldata = []

        self.entry = ttk.Entry(self)
        self.entry.pack()

        self.mode_label = ttk.Label(self, text="Scale mode on")
        self.mode_label.pack()
        self.scale_button = ttk.Button(self, text="Scale mode", state=tk.DISABLED, command=self.scale_dis)
        self.scale_button.pack()
        self.canvas.bind("<Button-1>", self.get_coords)
        self.undo = ttk.Button(self, text="Undo", state=tk.DISABLED, command=self.del_prev)
        self.undo.pack()

        self.tickbox_var = tk.IntVar()
        self.tickbox = tk.Checkbutton(self,
                                      text="Convert negative depths to zero",
                                      variable=self.tickbox_var,
                                      onvalue=1,
                                      offvalue=0)
        self.tickbox.select()
        self.tickbox.pack()
        self.save = ttk.Button(self, text="Save as", command=self.save_vel)
        self.save.pack()

    def open_file_dialog(self):
        self.img_file = filedialog.askopenfilename()
        self.file_open_window.destroy()

    def scale_dis(self):
        self.scale_button["state"] = tk.DISABLED
        self.undo["state"] = tk.DISABLED
        self.scale_coords.clear()
        self.input_coords.clear()
        self.depths.clear()
        self.veldata.clear()
        for _ in range(len(self.scale_prevs)):
            self.canvas.delete(self.scale_prevs.pop())
        for _ in range(len(self.vel_prevs)):
            self.canvas.delete(self.vel_prevs.pop())
        self.mode_label["text"] = "Scale mode on"

    def scale_ena(self):
        self.scale_button["state"] = tk.NORMAL
        self.undo["state"] = tk.NORMAL
        self.mode_label["text"] = "Velocity mode on"

    def get_input_xy(self):
        input_window = tk.Toplevel(self)
        x_entry = tk.Entry(input_window, text="X coordinate")
        x_entry.insert(0,"0")
        y_entry = tk.Entry(input_window, text="Y coordinate")
        y_entry.insert(0,"0")
        x_entry.pack()
        y_entry.pack()

        val1 = None
        val2 = None

        def submit_input():
            nonlocal val1, val2
            val1 = float(x_entry.get())
            val2 = float(y_entry.get())
            input_window.destroy()

        submit_button = tk.Button(input_window, text="Submit", command=submit_input)
        submit_button.pack()
        self.wait_window(input_window)
        return val1, val2

    def get_depth(self):
        input_window = tk.Toplevel(self)
        depth = tk.Entry(input_window, text="Depth")
        depth.insert(0,"0")
        depth.pack()
        depth_val = None

        def submit_input():
            nonlocal depth_val
            depth_val = float(depth.get())
            input_window.destroy()

        submit_button = tk.Button(input_window, text="Submit", command=submit_input)
        submit_button.pack()
        self.wait_window(input_window)
        return depth_val
        
    def get_coords(self, event):
        x, y = event.x, event.y
        r = 4
        if str(self.scale_button["state"]) == "disabled":
            if len(self.scale_coords) < 2:
                input_x, input_y = self.get_input_xy()
                self.input_coords.append((input_x,input_y))
            else:
                self.depths.append(self.get_depth())
            self.scale_coords.append((x,y))
            col = "blue"
            if len(self.scale_coords) > 3:
                self.scale_ena()
            self.scale_prevs.append(self.canvas.create_oval(x-r,y-r,x+r,y+r, fill=col, outline=col))
        else:
            try:
                vel = float(self.entry.get())
            except:
                print("Please enter a valid velocity value!")
                return
            dist = math.dist(self.input_coords[0], self.input_coords[1])
            x1 = self.scale_coords[0][0]
            y1 = self.scale_coords[2][1]
            x2 = self.scale_coords[1][0]
            y2 = self.scale_coords[3][1]
            X_coord, Y_coord = point_at_distance(self.input_coords[0], self.input_coords[1], (x-x1)/(x2-x1) * dist)
            self.veldata.append((X_coord, Y_coord, (y-y1)/(y2-y1) * self.depths[1],vel))
            col = "red"
            self.vel_prevs.append(self.canvas.create_oval(x-r,y-r,x+r,y+r, fill=col, outline=col))

    def del_prev(self):
        if len(self.vel_prevs) > 0:
            self.canvas.delete(self.vel_prevs.pop())
            self.veldata.pop()
        else:
            print("Already at oldest change!")

    def save_vel(self):
        self.save_file = filedialog.asksaveasfilename()
        try:
            with open(self.save_file, "wt") as f:
                if self.tickbox_var.get() == 1:
                    for row in self.veldata:
                        if row[2] < 0.0:
                            f.write(f"{row[0]} {row[1]} {0.0} {row[3]}\n")
                        else:
                            f.write(f"{row[0]} {row[1]} {row[2]} {row[3]}\n")
                else:
                    for row in self.veldata:
                        f.write(f"{row[0]} {row[1]} {row[2]} {row[3]}\n")
        except IOError:
            print("An error occurred while saving the file")