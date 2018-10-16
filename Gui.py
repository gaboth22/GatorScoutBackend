import Tkinter as tk
from PIL import ImageTk
from cStringIO import StringIO
from PIL import Image

class Gui:
    root = None
    robot_cam_panel = None
    map_plot_panel = None

    def __init__(self, fwd_button_callback, right_button_callback, left_button_callback):
        self.root = tk.Tk()
        tk_frame = tk.Frame(self.root )
        tk_fwd_button = tk.Button(tk_frame, text = 'FORWARD', command = fwd_button_callback)
        tk_right_button = tk.Button(tk_frame, text = 'RIGHT', command = right_button_callback)
        tk_left_button = tk.Button(tk_frame, text = 'LEFT', command = left_button_callback)
        self.robot_cam_panel = tk.Label(self.root )
        self.map_plot_panel = tk.Label(self.root )
        tk_fwd_button.pack(side='top')
        tk_left_button.pack(side='left')
        tk_right_button.pack(side='right')
        tk_frame.pack(side='bottom')
        self.robot_cam_panel.pack(side='left', fill='both', expand='yes')
        self.map_plot_panel.pack(side='right', fill='both', expand='yes')

    def set_robot_camera_frame(self, new_robocam_frame):
        image = new_robocam_frame.resize((640,480))
        tk_img = ImageTk.PhotoImage(image)
        self.robot_cam_panel.configure(image=tk_img)
        self.robot_cam_panel.image = tk_img

    def set_map_frame(self, new_map_frame):
        image = new_map_frame.resize((640,480))
        tk_img = ImageTk.PhotoImage(image)
        self.map_plot_panel.configure(image=tk_img)
        self.map_plot_panel.image = tk_img

    def run(self):
        self.root.update_idletasks()
        self.root.update()
