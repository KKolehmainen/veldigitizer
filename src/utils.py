import math

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