from cStringIO import StringIO
from collections import OrderedDict
from PIL import Image
import json
import requests
import time
import urllib
import struct
import numpy as np
import traceback
import logging
import binascii

IMAGE_REQUEST_PATH = '/get_image'
MOTION_REQUEST_PATH = '/post_motion'
MAPS_REQUEST_PATH = '/get_maps'
MOVE_NONE = 0
MOVE_FORWARD = 1
MOVE_RIGHT = 2
MOVE_LEFT = 3

class RobotCommunicationArbiter:
    camera_frame = None
    maps_data = None
    current_move_command = MOVE_NONE
    new_move_command = False
    robot_ip_address = ''

    def __init__(self, robot_ip):
        self.camera_frame = Image.open('uflogo.jpg')
        self.maps_data = []
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
                print 'Image size: ' + str(img_size)
                img_data = r.read(img_size)
                img_as_mem_file = StringIO(img_data)
                self.camera_frame = Image.open(img_as_mem_file)
        except:
            pass

        return self.camera_frame

    def get_new_map_data(self):
        address = 'http://' + self.robot_ip_address + MAPS_REQUEST_PATH
        try:
            r = urllib.urlopen(address)
            code = r.getcode()
            if code == 200:
                print 'Requesting from: ' + address
                print 'Status code: ' + str(code)
                meta_data = r.info()
                maps_size = int(meta_data.getheaders("Content-Length")[0])
                print 'Maps size received: ' + str(maps_size)
                data = r.read(maps_size)
                data = bytearray(str(data))
                data_as_ascii = binascii.hexlify(data)
                print 'Length of bytes: ' + str(len(data_as_ascii))

                data_list = []
                for i in range(0, len(data_as_ascii), 2):
                    str_byte = data_as_ascii[i:i+2]
                    byte = '{0:08b}'.format(int(str_byte, 16))
                    data_list.insert(0, byte)

                count = 0
                u64 = ''
                self.maps_data = []
                for byte in data_list:
                    u64 = u64 + byte
                    count = count + 1
                    if count == 8:
                        self.maps_data.append(u64)
                        count = 0
                        u64 = ''

                print 'Size of byte list: ' + str(len(self.maps_data))
        except Exception as e:
            logging.error(traceback.format_exc())

        return self.maps_data

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
