from tkinter import ttk, filedialog
import tkinter as tk
from PIL import Image
from digitized import Digitized
from imagecanvas import Image_canvas

class UI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()
        self.image = self.get_file()
        self.canvas = Image_canvas(self, self.image)
        self.create_widgets()
        self.canvas.bind("<Button-1>", self.get_coords)
        self.digitized = Digitized()

    def get_file(self):
        self.file_button = tk.Button(self, text="Open model file",
                                command=self.open_file_dialog)
        self.file_button.pack()
        self.wait_window(self.file_button)
        return Image.open(self.img_file)
    
    def open_file_dialog(self):
        self.img_file = filedialog.askopenfilename()
        self.file_button.destroy()

    def create_widgets(self):
        ttk.Label(self, text="Model", font="Calibri 24").pack()

        self.entry = ttk.Entry(self)
        self.entry.pack()

        self.mode_label = ttk.Label(self, text="Scale mode on")
        self.mode_label.pack()
        self.scale_button = ttk.Button(self, text="Scale mode", state=tk.DISABLED, command=self.scale_dis)
        self.scale_button.pack()
        self.undo = ttk.Button(self, text="Undo", state=tk.DISABLED, command=self.del_prev)
        self.undo.pack()

        self.tickbox_var = tk.IntVar()
        self.tickbox = tk.Checkbutton(self,
                                      text="Convert negative depths to zero",
                                      variable=self.tickbox_var,
                                      onvalue=True,
                                      offvalue=False)
        self.tickbox.select()
        self.tickbox.pack()
        self.save = ttk.Button(self, text="Save as",
                               command=lambda: self.digitized.save_vel(self.tickbox_var.get()))
        self.save.pack()

    def get_coords(self, event):
        x, y = event.x, event.y
        if str(self.scale_button["state"]) == "disabled":
            if len(self.digitized.scale_coords) < 2:
                input_x, input_y = self.get_input_xy()
                self.digitized.add_scale_point(x, y, input_x, input_y)
            else:
                self.digitized.add_depth(x, y, self.get_depth())
            if len(self.digitized.scale_coords) > 3:
                self.scale_ena()
            self.canvas.add_scale_oval(x, y)
        else:
            try:
                vel = float(self.entry.get())
                self.digitized.add_vel_point(x, y, vel)
                self.canvas.add_vel_oval(x, y)
            except:
                print("Please enter a valid velocity value!")
                return

    def get_input_xy(self):
        input_window = tk.Toplevel(self)
        x_entry = tk.Entry(input_window, text="X coordinate")
        x_entry.insert(0,"0")
        y_entry = tk.Entry(input_window, text="Y coordinate")
        y_entry.insert(0,"0")
        x_entry.pack()
        y_entry.pack()

        submit_button = tk.Button(input_window,
                                  text="Submit",
                                  command=lambda: self.submit_input(input_window, x_entry, y_entry))
        submit_button.pack()
        self.wait_window(input_window)
        return tuple(self.vals)
    
    def get_depth(self):
        input_window = tk.Toplevel(self)
        depth = tk.Entry(input_window, text="Depth")
        depth.insert(0,"0")
        depth.pack()

        submit_button = tk.Button(input_window,
                                  text="Submit",
                                  command=lambda: self.submit_input(input_window, depth)) 
        submit_button.pack()
        self.wait_window(input_window)
        return self.vals[0] 

    def submit_input(self, input_window, *entries):
        self.vals = []
        for entry in entries:
            self.vals.append(float(entry.get()))
        input_window.destroy()

    def scale_dis(self):
        self.mode_label["text"] = "Velocity mode on"
        self.scale_button["state"] = tk.DISABLED
        self.undo["state"] = tk.DISABLED
        self.digitized.clear_data()
        self.canvas.del_all_ovals()

    def scale_ena(self):
        self.mode_label["text"] = "Scale mode on"
        self.scale_button["state"] = tk.NORMAL
        self.undo["state"] = tk.NORMAL

    def del_prev(self):
        if len(self.canvas.vel_prevs) > 0 and len(self.digitized.veldata) > 0:
            self.digitized.pop_veldata()
            self.canvas.delete_oval()
        else:
            print("Already at oldest change!")



