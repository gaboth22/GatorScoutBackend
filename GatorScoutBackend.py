from cStringIO import StringIO
from PIL import Image
import Tkinter as tk
from PIL import ImageTk
from collections import OrderedDict
import json
import requests
import time
import urllib

GATORSCOUT_IP_ADDR = '192.168.4.100'
IMAGE_REQUEST_PATH = '/get_image'
MOTION_REQUEST_PATH = '/post_motion'

move_command = ''
new_command = False

def request_image(tk_panel):
    address = 'http://'+GATORSCOUT_IP_ADDR+IMAGE_REQUEST_PATH
    try:
        r = urllib.urlopen(address)
        if r.getcode() == 200:
            print 'Requesting from: ' + address
            print 'Status code: ' + str(r.getcode())
            meta_data = r.info()
            img_size = int(meta_data.getheaders("Content-Length")[0])
            img_data = r.read(img_size)
            img_as_mem_file = StringIO(img_data)
            image = Image.open(img_as_mem_file)
            image = image.resize((640,480))
            tk_img = ImageTk.PhotoImage(image)
            tk_panel.configure(image=tk_img)
            tk_panel.image = tk_img
    except:
        pass

def forward():
    global move_command
    global new_command
    move_command = 'f'
    new_command = True

def right():
    global move_command
    global new_command
    move_command = 'r'
    new_command = True

def left():
    global move_command
    global new_command
    move_command = 'l'
    new_command = True

def send_user_input_to_board():
    global new_command
    if new_command:
        new_command = False
        print 'New command: ' + move_command
        payload = None
        if move_command == 'f':
            payload = OrderedDict([('motion', 1)])
        elif move_command == 'r':
            payload = OrderedDict([('motion', 2)])
        elif move_command == 'l':
            payload = OrderedDict([('motion', 3)])

        headers = {'Content-Type':'application/json'}
        address = 'http://' + GATORSCOUT_IP_ADDR + MOTION_REQUEST_PATH
        print 'Requesting from: ' + address
        try:
            r = requests.post(address, headers=headers, data=json.dumps(payload))
            print 'Status code: ' + str(r.status_code)
            print r.content
        except:
            pass

def main():
    root = tk.Tk()
    tk_panel = tk.Label(root)
    tk_frame = tk.Frame(root)
    tk_fwd_button = tk.Button(tk_frame, text='Forward', command=forward)
    tk_right_button = tk.Button(tk_frame, text='Right', command=right)
    tk_left_button = tk.Button(tk_frame, text='Left', command=left)
    tk_fwd_button.pack(side='top')
    tk_left_button.pack(side='left')
    tk_right_button.pack(side='right')
    tk_frame.pack(side='bottom')
    tk_panel.pack(side='bottom', fill='both', expand='yes')

    while True:
        request_image(tk_panel)
        send_user_input_to_board()
        root.update_idletasks()
        root.update()

if __name__ == '__main__':
    main()
