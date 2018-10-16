from cStringIO import StringIO
from collections import OrderedDict
from PIL import Image
import json
import requests
import time
import urllib

IMAGE_REQUEST_PATH = '/get_image'
MOTION_REQUEST_PATH = '/post_motion'
MOVE_NONE = 0
MOVE_FORWARD = 1
MOVE_RIGHT = 2
MOVE_LEFT = 3

class RobotCommunicationArbiter:
    camera_frame = None
    current_move_command = MOVE_NONE
    new_move_command = False
    robot_ip_address = ''

    def __init__(self, robot_ip):
        self.camera_frame = Image.open('uflogo.jpg')
        self.robot_ip_address = robot_ip

    def get_new_cam_frame(self):
        address = 'http://' + self.robot_ip_address + IMAGE_REQUEST_PATH
        try:
            r = urllib.urlopen(address)
            code = r.getcode()
            if code == 200:
                print 'Requesting from: ' + address
                print 'Status code: ' + str(code)
                meta_data = r.info()
                img_size = int(meta_data.getheaders("Content-Length")[0])
                img_data = r.read(img_size)
                img_as_mem_file = StringIO(img_data)
                self.camera_frame = Image.open(img_as_mem_file)
        except:
            pass

        return self.camera_frame

    def request_forward_motion(self):
        self.new_move_command = True
        self.current_move_command = MOVE_FORWARD

    def request_right_motion(self):
        self.new_move_command = True
        self.current_move_command = MOVE_RIGHT

    def request_left_motion(self):
        self.new_move_command = True
        self.current_move_command = MOVE_LEFT

    def run(self):
        if self.new_move_command:
            self.new_move_command = False
            payload = OrderedDict([('motion', self.current_move_command)])
            headers = {'Content-Type':'application/json'}
            address = 'http://' + self.robot_ip_address + MOTION_REQUEST_PATH
            print 'Requesting from: ' + address
            try:
                r = requests.post(address, headers=headers, data=json.dumps(payload))
                print 'Status code: ' + str(r.status_code)
                print r.content
            except:
                pass
