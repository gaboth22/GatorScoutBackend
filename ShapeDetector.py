import cv2
import numpy as np
import io
from PIL import Image
from cStringIO import StringIO

class ShapeDetector:
    def __translate_contours(self, c, x, y):
        size = c.shape[0]
        for i in range(0,size):
            c[i][0][0] = c[i][0][0] + x
            c[i][0][1] = c[i][0][1] + y

    def __draw_contours_and_shape_name(self, c, shape_name, img_to_draw_on):
        M = cv2.moments(c)
        try:
            cX = int((M["m10"] / M["m00"]))
            cY = int((M["m01"] / M["m00"]))
        except:
            return

        c = c.astype("float")
        c = c.astype("int")

        cv2.drawContours(img_to_draw_on, [c], -1, (0, 255, 0), 2)
        cv2.putText(
            img_to_draw_on,
            shape_name,
            (cX, cY),
            cv2.FONT_HERSHEY_PLAIN,
            1,
            (0, 0, 255),
            2)

    def __contour_area_within_threshold(self, c, low_t, up_t):
        contour_area = cv2.contourArea(c)

        if(contour_area > low_t and contour_area < up_t):
            return True
        else:
            return False

    def __get_shape_name_and_contours(self, roi_bounds, img):
        roi = img[roi_bounds[0]:roi_bounds[1], roi_bounds[2]:roi_bounds[3]]
        img_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(img_gray, (5, 5), 0)
        thresh = \
            cv2.adaptiveThreshold(
                blurred,
                128,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY_INV,
                7,
                2)

        im2, contours, hierarchy = \
            cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        shape = 'unknown'
        c = None

        if contours:
            c = max(contours, key = cv2.contourArea)
            perimeter = cv2.arcLength(c, True)
            num_vert = cv2.approxPolyDP(c, 0.04 * perimeter, True)

            if len(num_vert) == 3:
                shape = 'Triangle'

            elif len(num_vert) == 4:
                shape = 'Square'

            elif len(num_vert) == 5:
                shape = 'Pentagon'

            else:
                shape = 'Circle'

        return (shape, c, thresh)

    def __get_cv_mat_from_jpg(self, jpg):
        cv_mat_img = None
        try:
            output = io.BytesIO()
            jpg.save(output, format='JPEG')
            img_hex_data = output.getvalue()
            img_bytes = np.asarray(bytearray(img_hex_data), dtype = np.uint8)
            cv_mat_img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
        except:
            pass

        return cv_mat_img

    def get_shape_and_highlited_image(self, jpg_img, output_img_size = [640, 480]):
        cv_mat_img = self.__get_cv_mat_from_jpg(jpg_img)
        jpg_img = cv_mat_img
        shape_name = 'unknown'

        if cv_mat_img is not None:
            shape_name, contours, thresh = self.__get_shape_name_and_contours([50, 120, 0, 160], cv_mat_img)
            if(contours is not None and self.__contour_area_within_threshold(contours, 600, 6500)):
                self.__translate_contours(contours, 0, 50)
                self.__draw_contours_and_shape_name(contours, shape_name, cv_mat_img)

            cv_mat_img = \
                cv2.resize(cv_mat_img, (output_img_size[0], output_img_size[1]), interpolation = cv2.INTER_AREA)
            small_thresh = \
                cv2.resize(thresh, (80, 60), interpolation = cv2.INTER_AREA)
            small_thresh = cv2.cvtColor(small_thresh, cv2.COLOR_GRAY2BGR)

            cv_mat_img[420:480, 560:640] = small_thresh

            jpg_img = cv2.imencode('.jpg', cv_mat_img)[1].tostring()
            img_as_mem_file = StringIO(jpg_img)
            jpg_img = Image.open(img_as_mem_file)

        return shape_name, jpg_img
