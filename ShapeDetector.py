import cv2
import numpy as np

class ShapeDetector:
    def __get_color_threshold_image(self, img, low_t, up_t):
        mask = cv2.inRange(img, low_t, up_t)
        color_thresh = cv2.bitwise_and(img, img, mask = mask)
        return color_thresh

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
        ret, thresh = cv2.threshold(blurred, 0, 128, cv2.THRESH_BINARY)
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

        return (shape, c)

    def __get_cv_mat_from_jpg_string(self, jpg_string):
        img_bytes = np.asarray(bytearray(jpg_string), dtype = np.uint8)
        cv_mat_img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

        return cv_mat_img

    def get_shape_and_highlited_image(self, jpg_img, output_img_size = [640, 480]):
        cv_mat_img = self.__get_cv_mat_from_jpg_string(jpg_img)
        color_thresh = self.__get_color_threshold_image(cv_mat_img, np.array([0, 0, 0]), np.array([128, 128, 128]))
        shape_name, contours = self.__get_shape_name_and_contours([30, 90, 40,100], color_thresh)

        if(contours is not None and self.__contour_area_within_threshold(contours, 1000, 1800)):
            self.__translate_contours(contours, 40, 30)
            self.__draw_contours_and_shape_name(contours, shape_name, cv_mat_img)

        cv_mat_img = \
            cv2.resize(cv_mat_img, (output_img_size[0], output_img_size[1]), interpolation = cv2.INTER_AREA)
        jpg_img = cv2.imencode('.jpg', cv_mat_img)[1].tostring()

        return shape_name, jpg_img
