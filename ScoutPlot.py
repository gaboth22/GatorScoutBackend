import numpy as np
import io
from PIL import Image
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

x1 = 0
x2 = 0
y1 = 0
y2 = 0
dir_left = "left"
dir_right = "right"
dir_up = "up"
dir_down = "down"
current_dir = 'up'
last_heading = 'up'

class ScoutPlot:

    def scout_plot_correct_direction(self, direction, rightDist, leftDist, ticks):
        
        desired_dir = ''
        if direction is not 'f':
            if direction == 'r':
                desired_dir = 'right'
            elif direction == 'l':
                desired_dir = 'left'

        direction_mappings = \
            { 
                ('up', 'right') : 'right',
                ('right', 'right') : 'down',
                ('down', 'right') : 'left',
                ('left', 'right') : 'up',
                ('up', 'left') : 'left',
                ('left', 'left') : 'down',
                ('down', 'left') : 'right',
                ('right', 'left') : 'up'
            }

        if desired_dir:
            global last_heading
            global current_dir
            last_heading = direction_mappings[(current_dir, desired_dir)]
            current_dir = last_heading
        
        return last_heading
    
    def scout_plot_create_map(self, direction, rightUS, leftUS, ticks):
        global x1
        global x2
        global y1
        global y2

        direction = self.scout_plot_correct_direction(direction, rightUS, leftUS, ticks)

        if direction == dir_right: 
            plt.scatter([x1+ticks, x2+ticks], [y1-rightUS, y2+leftUS], color=['blue', 'red'], alpha = 0.1)
            x1 = x1 + ticks
            x2 = x2 + ticks
            
        if direction == dir_left:
            plt.scatter([x1-ticks, x2-ticks], [y1+rightUS, y2-leftUS], color=['blue', 'red'], alpha = 0.1)
            x1 = x1 - ticks
            x2 = x2 - ticks
            
        if direction == dir_down:
            plt.scatter([x1-rightUS, x2+leftUS], [y1-ticks, y2-leftUS], color=['blue', 'red'], alpha = 0.1)
            y1 = y1 - ticks
            y2 = y2 - leftUS

        if direction == dir_up:
            plt.scatter([x1 + rightUS, x2 - leftUS], [y1 + ticks, y2 + ticks],color=['blue', 'red'], alpha = 0.1)
            y1 = y1 + ticks
            y2 = y2 + ticks
        
        plt.xlim(-500, 500) #limit to this size
        plt.ylim(-500, 500)
        plt.axis('off')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        im = Image.open(buf)

        return im
