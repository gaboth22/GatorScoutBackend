import RobotCommunicationArbiter as rca
import Gui as gui
import ShapeDetector as sd
from cStringIO import StringIO
from PIL import Image

GATORSCOUT_IP_ADDR = '192.168.4.100'

def main():
    robot_comm_arbiter = rca.RobotCommunicationArbiter(robot_ip = GATORSCOUT_IP_ADDR)
    shape_dectector = sd.ShapeDetector()
    placeholder_img = Image.open('uflogo.jpg')
    main_gui = \
        gui.Gui(
            fwd_button_callback = robot_comm_arbiter.request_forward_motion,
            right_button_callback = robot_comm_arbiter.request_right_motion,
            left_button_callback = robot_comm_arbiter.request_left_motion)
    main_gui.set_map_frame(placeholder_img)
    main_gui.set_robot_camera_frame(placeholder_img)

    while True:
        robot_comm_arbiter.run()
        robocam_frame = robot_comm_arbiter.get_new_cam_frame()
        shape_name, robocam_frame_with_shape = shape_dectector.get_shape_and_highlited_image(robocam_frame)
        frame_to_show = robocam_frame_with_shape if robocam_frame_with_shape is not None else robocam_frame
        main_gui.set_robot_camera_frame(frame_to_show)
        main_gui.run()

if __name__ == '__main__':
    main()
