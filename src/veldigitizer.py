import math
from tkinter import Tk, ttk, Canvas
import tkinter as tk
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

        scale_prevs = []
        vel_prevs = []
        scale_coords = []
        input_coords = []
        depths = []
        veldata = []

        entry = ttk.Entry(self)
        entry.pack()

        def scale_dis():
            scale_button["state"] = tk.DISABLED
            self.undo["state"] = tk.DISABLED
            scale_coords.clear()
            input_coords.clear()
            depths.clear()
            veldata.clear()
            for _ in range(len(scale_prevs)):
                self.canvas.delete(scale_prevs.pop())
            for _ in range(len(vel_prevs)):
                self.canvas.delete(vel_prevs.pop())
            self.mode_label["text"] = "Scale mode on"

        def scale_ena():
            scale_button["state"] = tk.NORMAL
            self.undo["state"] = tk.NORMAL
            self.mode_label["text"] = "Velocity mode on"

        self.mode_label = ttk.Label(self, text="Scale mode on")
        self.mode_label.pack()
        scale_button = ttk.Button(self, text="Scale mode", state=tk.DISABLED, command=scale_dis)
        scale_button.pack()

        def get_input_xy():
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

        def get_depth():
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
        
        def point_at_distance(point1, point2, distance):
            """
            Find the coordinates of a point at a given distance from a given point along a line defined by two points.
            
            Args:
                point1 (tuple): (x, y) coordinates of the first point.
                point2 (tuple): (x, y) coordinates of the second point.
                distance (float): Distance from the given point to the desired point.
                
            Returns:
                tuple: (x, y) coordinates of the point at the given distance.
            """
            x1, y1 = point1
            x2, y2 = point2
            
            dx = x2 - x1
            dy = y2 - y1
            line_length = math.sqrt(dx**2 + dy**2)
            
            if line_length == 0:
                return None  # Invalid case: the two points are the same
            
            ratio = distance / line_length
            x = x1 + ratio * dx
            y = y1 + ratio * dy
            
            return (x, y)

        def get_coords(event):
            x, y = event.x, event.y
            r = 4
            if str(scale_button["state"]) == "disabled":
                if len(scale_coords) < 2:
                    input_x, input_y = get_input_xy()
                    input_coords.append((input_x,input_y))
                else:
                    depths.append(get_depth())
                scale_coords.append((x,y))
                col = "blue"
                if len(scale_coords) > 3:
                    scale_ena()
                scale_prevs.append(self.canvas.create_oval(x-r,y-r,x+r,y+r, fill=col, outline=col))
            else:
                try:
                    vel = float(entry.get())
                except:
                    print("Please enter a valid velocity value!")
                    return
                dist = math.dist(input_coords[0], input_coords[1])
                x1 = scale_coords[0][0]
                y1 = scale_coords[2][1]
                x2 = scale_coords[1][0]
                y2 = scale_coords[3][1]
                X_coord, Y_coord = point_at_distance(input_coords[0], input_coords[1], (x-x1)/(x2-x1) * dist)
                veldata.append((X_coord, Y_coord, (y-y1)/(y2-y1) * depths[1],vel))
                col = "red"
                vel_prevs.append(self.canvas.create_oval(x-r,y-r,x+r,y+r, fill=col, outline=col))

        self.canvas.bind("<Button-1>", get_coords)

        def del_prev():
            if len(vel_prevs) > 0:
                self.canvas.delete(vel_prevs.pop())
                veldata.pop()
            else:
                print("Already at oldest exchange!")

        self.undo = ttk.Button(self, text="Undo", state=tk.DISABLED, command=del_prev)
        self.undo.pack()

        def save_vel():
            with open("testfile.txt", "wt") as f:
                for row in veldata:
                    f.write(f"{row[0]} {row[1]} {row[2]} {row[3]}\n")

        self.save = ttk.Button(self, text="Save velocities", command=save_vel)
        self.save.pack()

if __name__ == "__main__":
    app = App()
