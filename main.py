import RobotCommunicationArbiter as rca
import Gui as gui
import ShapeDetector as sd
import ScoutPlot as sp
from cStringIO import StringIO
from PIL import Image
import threading

GATORSCOUT_IP_ADDR = '192.168.4.100'

# def plot_new_map_frame(scout_plot, index):
#     plot_data = \
#         {
#             0 : ['f', 5, 5, 10],
#             1 : ['l', 5, 5, 20],
#             2 : ['l', 5, 5, 10],
#             3 : ['r', 5, 5, 25],
#             4 : ['r', 5, 5, 5],
#             5 : ['f', 5, 5, 10],
#             6 : ['l', 5, 5, 20],
#             7 : ['l', 5, 5, 10],
#             8 : ['r', 5, 5, 25],
#             9 : ['r', 5, 5, 5]
#         }
#     map_data = plot_data[index]
#     index = index + 1
#     index = index % 10
#     global map_frame_to_show 
#     map_frame_to_show = scout_plot.scout_plot_create_map(map_data[0], map_data[1], map_data[2], map_data[3])
#     threading.Timer(0.1, plot_new_map_frame, args = (scout_plot, index)).start()

def get_new_frame(robot_comm_arbiter, shape_dectector):
    robocam_frame = robot_comm_arbiter.get_new_cam_frame()
    shape_name, robocam_frame_with_shape = shape_dectector.get_shape_and_highlited_image(robocam_frame)
    global frame_to_show
    frame_to_show = robocam_frame_with_shape if robocam_frame_with_shape is not None else robocam_frame
    threading.Timer(0.3, get_new_frame, args = (robot_comm_arbiter, shape_dectector)).start()

def main():
    robot_comm_arbiter = rca.RobotCommunicationArbiter(robot_ip = GATORSCOUT_IP_ADDR)
    scout_plot = sp.ScoutPlot()
    shape_dectector = sd.ShapeDetector()
    placeholder_img = Image.open('uflogo.jpg')
    global frame_to_show
    global map_frame_to_show
    frame_to_show = placeholder_img
    map_frame_to_show = placeholder_img
    
    main_gui = \
        gui.Gui(
            fwd_button_callback = robot_comm_arbiter.request_forward_motion,
            right_button_callback = robot_comm_arbiter.request_right_motion,
            left_button_callback = robot_comm_arbiter.request_left_motion)
    main_gui.set_map_frame(placeholder_img)
    main_gui.set_robot_camera_frame(placeholder_img)

    # plot_new_map_frame(scout_plot, 0)
    index = 0
    get_new_frame(robot_comm_arbiter, shape_dectector)

    while True:
        main_gui.set_robot_camera_frame(frame_to_show)
        main_gui.set_map_frame(map_frame_to_show)
        robot_comm_arbiter.run()
        main_gui.run()

        plot_data = \
        {
            0 : ['f', 5, 5, 5],
            1 : ['f', 5, 5, 5],
            2 : ['f', 5, 5, 5],
            3 : ['f', 5, 5, 5],
            4 : ['f', 5, 5, 5],
            5 : ['f', 5, 5, 5],
            6 : ['f', 5, 5, 5],
            7 : ['f', 5, 5, 5],
            8 : ['f', 5, 5, 5],
            9 : ['f', 5, 5, 5],
            10 : ['f', 5, 5, 5],
            11 : ['l', 5, 5, 5],
            12 : ['f', 5, 5, 5],
            13 : ['f', 5, 5, 5],
            14 : ['f', 5, 5, 5],
            15 : ['f', 5, 5, 5],
            16 : ['f', 5, 5, 5],
            17 : ['f', 5, 5, 5],
            18 : ['f', 5, 5, 5],
            19 : ['f', 5, 5, 5],
            20 : ['f', 5, 5, 5],
            21 : ['l', 5, 5, 5],
            22 : ['f', 5, 5, 5],
            23 : ['f', 5, 5, 5],
            24 : ['f', 5, 5, 5],
            25 : ['f', 5, 5, 5],
            26 : ['f', 5, 5, 5],
            27 : ['f', 5, 5, 5],
            28 : ['f', 5, 5, 5],
            29 : ['l', 5, 5, 5],
            30 : ['f', 5, 5, 5],
            31 : ['f', 5, 5, 5],
            32 : ['f', 5, 5, 5],
            33 : ['f', 5, 5, 5],
            34 : ['f', 5, 5, 5],
            35 : ['f', 5, 5, 5],
            36 : ['f', 5, 5, 5],
            37 : ['f', 5, 5, 5],
            38 : ['l', 5, 5, 5],
            39 : ['f', 5, 5, 5],
            40 : ['f', 5, 5, 5],
            41 : ['f', 5, 5, 5],
            42 : ['f', 5, 5, 5],
            43 : ['f', 5, 5, 5],
            44 : ['f', 5, 5, 5],
            45 : ['f', 5, 5, 5],
            46 : ['f', 5, 5, 5],
            47 : ['f', 5, 5, 5]
        }

        map_data = plot_data[index]
        index = index + 1
        index = index % 48
        global map_frame_to_show 
        map_frame_to_show = scout_plot.scout_plot_create_map(map_data[0], map_data[1], map_data[2], map_data[3])

if __name__ == '__main__':
    main()
