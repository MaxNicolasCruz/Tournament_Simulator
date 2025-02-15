import tkinter as tk
import random

class BackgroundEffect:
    def __init__(self, parent, width=1000, height=650):
        self.bg = None
        self.parent = parent
        
    def create_point(self, x, y, size):
        """
        Creates a point on the canvas and initiates its shrinking process
        
        Args:
            x (int): The x-coordinate for the point
            y (int): The y-coordinate for the point
            size (int): The initial size of the point
        """
        point = self.bg.create_oval(x, y, x + size, y + size,fill='white', outline='white')
        self.shrink_point(point, x, y, size)

    def shrink_point(self, point, x, y, size):
        """
        Recursively shrinks a point on the canvas until it disappears
        
        Args:
            point (int): The canvas object ID of the point
            x (int): The x-coordinate of the point
            y (int): The y-coordinate of the point
            size (int): The current size of the point
        """
        if size > 0:
            size -= 1
            self.bg.coords(point, x, y, x + size, y + size)
            self.parent.after(50,self.shrink_point,point,x,y,size)
        else:
            self.bg.delete(point)        
            

    def start_effect(self,count):
        """
        
        Creates a background effect by randomly generating points on the canvas
        
        Args:
            count (int): The number of points to generate
        """

        # Initialize canvas if not already done 
        if self.bg is None:
            bg = tk.Canvas(self.parent, bg='black', width=1000, height=650)
            bg.pack()
            self.bg = bg
            
        # Get window dimensions
        w_width = self.parent.winfo_width()
        w_height = self.parent.winfo_height()
        
        # Generate points if window dimensions are valid
        if w_width > 1 and w_height > 1:
            for i in range(count):
                x = random.randint(0, w_width)
                y = random.randint(0, w_height)
                size = random.randint(4, 9)
                self.create_point(x, y, size)
        
        # Schedule the next effect
        self.parent.after(random.randint(100, 300), self.start_effect, count)

