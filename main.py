import RobotCommunicationArbiter as rca
import Gui as gui
import ShapeDetector as sd
from cStringIO import StringIO
from PIL import Image, ImageDraw
from PIL import ImageOps
import threading

GATORSCOUT_IP_ADDR = '192.168.4.100'

def get_maps_as_image(blocked):
    img = Image.new('RGB', (100, 100), color = (0, 0, 0))
    d = ImageDraw.Draw(img)

    xoffset = 40
    yoffset = 10

    for x in range(0, 64):
        b = blocked[x]
        for y in range(63, -1, -1):
            if(b[y] == '1'):
                d.text((x + xoffset, y + yoffset), '.', fill=(255,255,0)),
            else:
                d.text((x + xoffset, y + yoffset), '.', fill=(0,0,0)),

    img = img.rotate(270)
    img = ImageOps.mirror(img)
    return img

def get_new_frame(robot_comm_arbiter, shape_dectector):
    robocam_frame = robot_comm_arbiter.get_new_cam_frame()
    shape_name, robocam_frame_with_shape = shape_dectector.get_shape_and_highlited_image(robocam_frame)
    global cam_frame_to_show
    cam_frame_to_show = robocam_frame_with_shape if robocam_frame_with_shape is not None else robocam_frame
    threading.Timer(0.3, get_new_frame, args = (robot_comm_arbiter, shape_dectector,)).start()

def get_new_map_data(robot_comm_arbiter):
    maps_data = robot_comm_arbiter.get_new_map_data()
    global map_frame_to_show
    map_frame_to_show = get_maps_as_image(maps_data)
    threading.Timer(0.5, get_new_map_data, args = (robot_comm_arbiter,)).start()

def main():
    robot_comm_arbiter = rca.RobotCommunicationArbiter(robot_ip = GATORSCOUT_IP_ADDR)
    shape_dectector = sd.ShapeDetector()
    placeholder_img = Image.open('uflogo.jpg')
    global cam_frame_to_show
    cam_frame_to_show = placeholder_img
    global map_frame_to_show
    map_frame_to_show = placeholder_img
    main_gui = \
        gui.Gui(
            fwd_button_callback = robot_comm_arbiter.request_forward_motion,
            right_button_callback = robot_comm_arbiter.request_right_motion,
            left_button_callback = robot_comm_arbiter.request_left_motion)
    main_gui.set_map_frame(placeholder_img)
    main_gui.set_robot_camera_frame(placeholder_img)

    get_new_frame(robot_comm_arbiter, shape_dectector)
    get_new_map_data(robot_comm_arbiter)

    while True:
        main_gui.set_robot_camera_frame(cam_frame_to_show)
        main_gui.set_map_frame(map_frame_to_show)
        robot_comm_arbiter.run()
        main_gui.run()

if __name__ == '__main__':
    main()
