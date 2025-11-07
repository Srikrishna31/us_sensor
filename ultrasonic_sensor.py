import numpy

class UltrasonicSensor:
   def __init__(self, min_range, max_range, x, y, z, h, p, r, theta):
        self.min_range = min_range
        self.max_range = max_range
        self.x = x
        self.y = y
        self.z = z
        self.h = h
        self.p = p
        self.r = r
        self.theta = theta

if __name__=="__main__":
    print("Hello World")