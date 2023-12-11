import math
from utils import point_at_distance
from tkinter import filedialog

class Digitized():
    def __init__(self) -> None:
        self.scale_coords = []  #canvas coordinates for scaling
        self.input_coords = []  #real coordinates for scaling
        self.depths = []  #depths for scaling
        self.veldata = []  #velocity data (x,y,z,vel)

    def clear_data(self):
        self.scale_coords = []
        self.input_coords = []
        self.depths = []
        self.veldata = []

    def add_scale_point(self, x, y, input_x, input_y):
        self.input_coords.append((input_x,input_y))
        self.scale_coords.append((x,y))

    def add_vel_point(self, x, y, vel):
        
        dist = math.dist(self.input_coords[0], self.input_coords[1])
        x1 = self.scale_coords[0][0]
        y1 = self.scale_coords[2][1]
        x2 = self.scale_coords[1][0]
        y2 = self.scale_coords[3][1]
        X_coord, Y_coord = point_at_distance(self.input_coords[0], self.input_coords[1], (x-x1)/(x2-x1) * dist)
        self.veldata.append((X_coord, Y_coord, (y-y1)/(y2-y1) * self.depths[1],vel))

    def add_depth(self, x, y, depth):
        self.depths.append(depth)
        self.scale_coords.append((x,y))

    def pop_veldata(self):
        return self.veldata.pop()

    def save_vel(self, convert_depths=True):
        self.save_file = filedialog.asksaveasfilename()
        try:
            with open(self.save_file, "wt") as f:
                if convert_depths:
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