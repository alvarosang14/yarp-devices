import logging
import yarp


class GrabberControls2GuiBackend:
    def __init__(self, controls):
        self.controls = controls

    def init(self):
        pass

    def close(self):
        pass

    # ===== ZOOM RELATED FUNCTIONS =====
    def set_zoom(self, zoom):
        logging.debug("Zoom set to {}".format(zoom))
        self.controls.setFeature(yarp.YARP_FEATURE_ZOOM, zoom)

    def has_zoom(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_ZOOM)

    def get_zoom(self):
        return self.controls.getFeature(yarp.YARP_FEATURE_ZOOM)

    def get_zoom_range(self):
        value1 = yarp.DVector(1)
        value2 = yarp.DVector(1)
        self.controls.getFeature(yarp.YARP_FEATURE_ZOOM, value1, value2)
        return value1[0], value2[0]

    def get_zoom_mode(self):
        return 1 if self.controls.getMode(yarp.YARP_FEATURE_ZOOM)==2 else 0

    def set_zoom_mode(self, mode):
        logging.debug("Zoom mode set to {}".format(mode))
        self.controls.setMode(yarp.YARP_FEATURE_ZOOM, mode)

    def has_zoom_auto(self):
        return self.controls.hasAuto(yarp.YARP_FEATURE_ZOOM)

    # ===== FOCUS RELATED FUNCTIONS =====
    def set_focus(self, focus):
        logging.debug("Focus set to {}".format(focus))
        self.controls.setFeature(yarp.YARP_FEATURE_FOCUS, focus)

    def has_focus(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_FOCUS)

    def get_focus(self):
        return self.controls.getFeature(yarp.YARP_FEATURE_FOCUS)

    def get_focus_range(self):
        value1 = yarp.DVector(1)
        value2 = yarp.DVector(1)
        self.controls.getFeature(yarp.YARP_FEATURE_FOCUS, value1, value2)
        return value1[0], value2[0]

    def get_focus_mode(self):
        return 1 if self.controls.getMode(yarp.YARP_FEATURE_FOCUS)==2 else 0

    def set_focus_mode(self, mode):
        logging.debug("Focus mode set to {}".format(mode))
        self.controls.setMode(yarp.YARP_FEATURE_FOCUS, mode)

    def has_focus_auto(self):
        return self.controls.hasAuto(yarp.YARP_FEATURE_FOCUS)

    # ===== GAIN RELATED FUNCTIONS =====
    def set_gain(self, gain):
        logging.debug("Gain set to {}".format(gain))
        self.controls.setFeature(yarp.YARP_FEATURE_GAIN, gain)

    def has_gain(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_GAIN)

    def get_gain(self):
        return self.controls.getFeature(yarp.YARP_FEATURE_GAIN)

    def get_gain_range(self):
        value1 = yarp.DVector(1)
        value2 = yarp.DVector(1)
        self.controls.getFeature(yarp.YARP_FEATURE_GAIN, value1, value2)
        return value1[0], value2[0]

    def get_gain_mode(self):
        return 1 if self.controls.getMode(yarp.YARP_FEATURE_GAIN)==2 else 0

    def set_gain_mode(self, mode):
        logging.debug("Gain mode set to {}".format(mode))
        self.controls.setMode(yarp.YARP_FEATURE_GAIN, mode)

    def has_gain_auto(self):
        return self.controls.hasAuto(yarp.YARP_FEATURE_GAIN)

    # ===== EXPOSURE RELATED FUNCTIONS =====
    def set_exposure(self, exposure):
        logging.debug("Exposure set to {}".format(exposure))
        self.controls.setFeature(yarp.YARP_FEATURE_EXPOSURE, exposure)

    def has_exposure(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_EXPOSURE)

    def get_exposure(self):
        return self.controls.getFeature(yarp.YARP_FEATURE_EXPOSURE)

    def get_exposure_range(self):
        value1 = yarp.DVector(1)
        value2 = yarp.DVector(1)
        self.controls.getFeature(yarp.YARP_FEATURE_EXPOSURE, value1, value2)
        return value1[0], value2[0]

    def get_exposure_mode(self):
        return 1 if self.controls.getMode(yarp.YARP_FEATURE_EXPOSURE)==2 else 0

    def set_exposure_mode(self, mode):
        logging.debug("Exposure mode set to {}".format(mode))
        self.controls.setMode(yarp.YARP_FEATURE_EXPOSURE, mode)

    def has_exposure_auto(self):
        return self.controls.hasAuto(yarp.YARP_FEATURE_EXPOSURE)

    # ===== FPS RELATED FUNCTIONS =====
    def set_FPS(self, fps):
        logging.debug("FPS set to {}".format(fps))
        self.controls.setFeature(yarp.YARP_FEATURE_FRAME_RATE, fps)

    def has_FPS(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_FRAME_RATE)

    def get_FPS(self):
        return self.controls.getFeature(yarp.YARP_FEATURE_FRAME_RATE)

    def get_FPS_range(self):
        value1 = yarp.DVector(1)
        value2 = yarp.DVector(1)
        self.controls.getFeature(yarp.YARP_FEATURE_FRAME_RATE, value1, value2)
        return value1[0], value2[0]

    def get_FPS_mode(self):
        return 1 if self.controls.getMode(yarp.YARP_FEATURE_FRAME_RATE)==2 else 0

    def set_FPS_mode(self, mode):
        logging.debug("FPS mode set to {}".format(mode))
        self.controls.setMode(yarp.YARP_FEATURE_FRAME_RATE, mode)

    def has_FPS_auto(self):
        return self.controls.hasAuto(yarp.YARP_FEATURE_FRAME_RATE)

    # ===== BRIGHTNESS RELATED FUNCTIONS =====
    def set_brightness(self, brightness):
        logging.debug("Brightness set to {}".format(brightness))
        self.controls.setFeature(yarp.YARP_FEATURE_BRIGHTNESS, brightness)

    def has_brightness(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_BRIGHTNESS)

    def get_brightness(self):
        return self.controls.getFeature(yarp.YARP_FEATURE_BRIGHTNESS)

    def get_brightness_range(self):
        value1 = yarp.DVector(1)
        value2 = yarp.DVector(1)
        self.controls.getFeature(yarp.YARP_FEATURE_BRIGHTNESS, value1, value2)
        return value1[0], value2[0]

    def get_brightness_mode(self):
        return 1 if self.controls.getMode(yarp.YARP_FEATURE_BRIGHTNESS)==2 else 0

    def set_brightness_mode(self, mode):
        logging.debug("Brightness mode set to {}".format(mode))
        self.controls.setMode(yarp.YARP_FEATURE_BRIGHTNESS, mode)

    def has_brightness_auto(self):
        return self.controls.hasAuto(yarp.YARP_FEATURE_BRIGHTNESS)

    # ===== SHUTTER RELATED FUNCTIONS =====
    def set_shutter(self, shutter):
        logging.debug("Shutter set to {}".format(shutter))
        self.controls.setFeature(yarp.YARP_FEATURE_SHUTTER, shutter)

    def has_shutter(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_SHUTTER)

    def get_shutter(self):
        return self.controls.getFeature(yarp.YARP_FEATURE_SHUTTER)

    def get_shutter_range(self):
        value1 = yarp.DVector(1)
        value2 = yarp.DVector(1)
        self.controls.getFeature(yarp.YARP_FEATURE_SHUTTER, value1, value2)
        return value1[0], value2[0]

    def get_shutter_mode(self):
        return 1 if self.controls.getMode(yarp.YARP_FEATURE_SHUTTER)==2 else 0

    def set_shutter_mode(self, mode):
        logging.debug("Shutter mode set to {}".format(mode))
        self.controls.setMode(yarp.YARP_FEATURE_SHUTTER, mode)

    def has_shutter_auto(self):
        return self.controls.hasAuto(yarp.YARP_FEATURE_SHUTTER)

    # ===== IRIS RELATED FUNCTIONS =====
    def set_iris(self, iris):
        logging.debug("Iris set to {}".format(iris))
        self.controls.setFeature(yarp.YARP_FEATURE_IRIS, iris)

    def has_iris(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_IRIS)

    def get_iris(self):
        return self.controls.getFeature(yarp.YARP_FEATURE_IRIS)

    def get_iris_range(self):
        value1 = yarp.DVector(1)
        value2 = yarp.DVector(1)
        self.controls.getFeature(yarp.YARP_FEATURE_IRIS, value1, value2)
        return value1[0], value2[0]

    def get_iris_mode(self):
        return 1 if self.controls.getMode(yarp.YARP_FEATURE_IRIS)==2 else 0

    def set_iris_mode(self, mode):
        logging.debug("Iris mode set to {}".format(mode))
        self.controls.setMode(yarp.YARP_FEATURE_IRIS, mode)

    def has_iris_auto(self):
        return self.controls.hasAuto(yarp.YARP_FEATURE_IRIS)

    # ===== WHITE BALANCE RELATED FUNCTIONS =====
    def set_white_balance(self, white_balance):
        logging.debug("White Balance set to {}".format(white_balance))
        self.controls.setFeature(yarp.YARP_FEATURE_WHITE_BALANCE, white_balance)

    def has_white_balance(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_WHITE_BALANCE)

    def get_white_balance(self):
        return self.controls.getFeature(yarp.YARP_FEATURE_WHITE_BALANCE)

    def get_white_balance_range(self):
        value1 = yarp.DVector(1)
        value2 = yarp.DVector(1)
        self.controls.getFeature(yarp.YARP_FEATURE_WHITE_BALANCE, value1, value2)
        return value1[0], value2[0]

    def get_white_balance_mode(self):
        return 1 if self.controls.getMode(yarp.YARP_FEATURE_WHITE_BALANCE)==2 else 0

    def set_white_balance_mode(self, mode):
        logging.debug("White Balance mode set to {}".format(mode))
        self.controls.setMode(yarp.YARP_FEATURE_WHITE_BALANCE, mode)

    def has_white_balance_auto(self):
        return self.controls.hasAuto(yarp.YARP_FEATURE_WHITE_BALANCE)

    # ===== HUE RELATED FUNCTIONS =====
    def set_hue(self, hue):
        logging.debug("Hue set to {}".format(hue))
        self.controls.setFeature(yarp.YARP_FEATURE_HUE, hue)

    def has_hue(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_HUE)

    def get_hue(self):
        return self.controls.getFeature(yarp.YARP_FEATURE_HUE)

    def get_hue_range(self):
        value1 = yarp.DVector(1)
        value2 = yarp.DVector(1)
        self.controls.getFeature(yarp.YARP_FEATURE_HUE, value1, value2)
        return value1[0], value2[0]

    def get_hue_mode(self):
        return 1 if self.controls.getMode(yarp.YARP_FEATURE_HUE)==2 else 0

    def set_hue_mode(self, mode):
        logging.debug("Hue mode set to {}".format(mode))
        self.controls.setMode(yarp.YARP_FEATURE_HUE, mode)

    def has_hue_auto(self):
        return self.controls.hasAuto(yarp.YARP_FEATURE_HUE)

    # ===== SATURATION RELATED FUNCTIONS =====
    def set_saturation(self, saturation):
        logging.debug("Saturation set to {}".format(saturation))
        self.controls.setFeature(yarp.YARP_FEATURE_SATURATION, saturation)

    def has_saturation(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_SATURATION)

    def get_saturation(self):
        return self.controls.getFeature(yarp.YARP_FEATURE_SATURATION)

    def get_saturation_range(self):
        value1 = yarp.DVector(1)
        value2 = yarp.DVector(1)
        self.controls.getFeature(yarp.YARP_FEATURE_SATURATION, value1, value2)
        return value1[0], value2[0]

    def get_saturation_mode(self):
        return 1 if self.controls.getMode(yarp.YARP_FEATURE_SATURATION)==2 else 0

    def set_saturation_mode(self, mode):
        logging.debug("Saturation mode set to {}".format(mode))
        self.controls.setMode(yarp.YARP_FEATURE_SATURATION, mode)

    def has_saturation_auto(self):
        return self.controls.hasAuto(yarp.YARP_FEATURE_SATURATION)

    # ===== GAMMA RELATED FUNCTIONS =====
    def set_gamma(self, gamma):
        logging.debug("Gamma set to {}".format(gamma))
        self.controls.setFeature(yarp.YARP_FEATURE_GAMMA, gamma)

    def has_gamma(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_GAMMA)

    def get_gamma(self):
        return self.controls.getFeature(yarp.YARP_FEATURE_GAMMA)

    def get_gamma_range(self):
        value1 = yarp.DVector(1)
        value2 = yarp.DVector(1)
        self.controls.getFeature(yarp.YARP_FEATURE_GAMMA, value1, value2)
        return value1[0], value2[0]

    def get_gamma_mode(self):
        return 1 if self.controls.getMode(yarp.YARP_FEATURE_GAMMA)==2 else 0

    def set_gamma_mode(self, mode):
        logging.debug("Gamma mode set to {}".format(mode))
        self.controls.setMode(yarp.YARP_FEATURE_GAMMA, mode)

    def has_gamma_auto(self):
        return self.controls.hasAuto(yarp.YARP_FEATURE_GAMMA)

    # ===== TEMPERATURE RELATED FUNCTIONS =====
    def set_temperature(self, temperature):
        logging.debug("Temperature set to {}".format(temperature))
        self.controls.setFeature(yarp.YARP_FEATURE_TEMPERATURE, temperature)

    def has_temperature(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_TEMPERATURE)

    def get_temperature(self):
        return self.controls.getFeature(yarp.YARP_FEATURE_TEMPERATURE)

    def get_temperature_range(self):
        value1 = yarp.DVector(1)
        value2 = yarp.DVector(1)
        self.controls.getFeature(yarp.YARP_FEATURE_TEMPERATURE, value1, value2)
        return value1[0], value2[0]

    def get_temperature_mode(self):
        return 1 if self.controls.getMode(yarp.YARP_FEATURE_TEMPERATURE)==2 else 0

    def set_temperature_mode(self, mode):
        logging.debug("Temperature mode set to {}".format(mode))
        self.controls.setMode(yarp.YARP_FEATURE_TEMPERATURE, mode)

    def has_temperature_auto(self):
        return self.controls.hasAuto(yarp.YARP_FEATURE_TEMPERATURE)

    # ===== SHARPNESS RELATED FUNCTIONS =====
    def set_sharpness(self, sharpness):
        logging.debug("Sharpness set to {}".format(sharpness))
        self.controls.setFeature(yarp.YARP_FEATURE_SHARPNESS, sharpness)

    def has_sharpness(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_SHARPNESS)

    def get_sharpness(self):
        return self.controls.getFeature(yarp.YARP_FEATURE_SHARPNESS)

    def get_sharpness_range(self):
        value1 = yarp.DVector(1)
        value2 = yarp.DVector(1)
        self.controls.getFeature(yarp.YARP_FEATURE_SHARPNESS, value1, value2)
        return value1[0], value2[0]

    def get_sharpness_mode(self):
        return 1 if self.controls.getMode(yarp.YARP_FEATURE_SHARPNESS)==2 else 0

    def set_sharpness_mode(self, mode):
        logging.debug("Sharpness mode set to {}".format(mode))
        self.controls.setMode(yarp.YARP_FEATURE_SHARPNESS, mode)

    def has_sharpness_auto(self):
        return self.controls.hasAuto(yarp.YARP_FEATURE_SHARPNESS)

    # ===== TRIGGER RELATED FUNCTIONS =====
    def set_trigger(self, trigger):
        logging.debug("Trigger set to {}".format(trigger))
        self.controls.setFeature(yarp.YARP_FEATURE_TRIGGER, trigger)

    def has_trigger(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_TRIGGER)

    def get_trigger(self):
        return self.controls.getFeature(yarp.YARP_FEATURE_TRIGGER)

    def get_trigger_range(self):
        value1 = yarp.DVector(1)
        value2 = yarp.DVector(1)
        self.controls.getFeature(yarp.YARP_FEATURE_TRIGGER, value1, value2)
        return value1[0], value2[0]

    def get_trigger_mode(self):
        return 1 if self.controls.getMode(yarp.YARP_FEATURE_TRIGGER)==2 else 0

    def set_trigger_mode(self, mode):
        logging.debug("Trigger mode set to {}".format(mode))
        self.controls.setMode(yarp.YARP_FEATURE_TRIGGER, mode)

    def has_trigger_auto(self):
        return self.controls.hasAuto(yarp.YARP_FEATURE_TRIGGER)

    # ===== TRIGGER DELAY RELATED FUNCTIONS =====
    def set_trigger_delay(self, trigger_delay):
        logging.debug("Trigger Delay set to {}".format(trigger_delay))
        self.controls.setFeature(yarp.YARP_FEATURE_TRIGGER_DELAY, trigger_delay)

    def has_trigger_delay(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_TRIGGER_DELAY)

    def get_trigger_delay(self):
        return self.controls.getFeature(yarp.YARP_FEATURE_TRIGGER_DELAY)

    def get_trigger_delay_range(self):
        value1 = yarp.DVector(1)
        value2 = yarp.DVector(1)
        self.controls.getFeature(yarp.YARP_FEATURE_TRIGGER_DELAY, value1, value2)
        return value1[0], value2[0]

    def get_trigger_delay_mode(self):
        return 1 if self.controls.getMode(yarp.YARP_FEATURE_TRIGGER_DELAY)==2 else 0

    def set_trigger_delay_mode(self, mode):
        logging.debug("Trigger Delay mode set to {}".format(mode))
        self.controls.setMode(yarp.YARP_FEATURE_TRIGGER_DELAY, mode)

    def has_trigger_delay_auto(self):
        return self.controls.hasAuto(yarp.YARP_FEATURE_TRIGGER_DELAY)

    # ===== WHITE SHADING RELATED FUNCTIONS =====
    def set_white_shading(self, white_shading):
        logging.debug("White Shading set to {}".format(white_shading))
        self.controls.setFeature(yarp.YARP_FEATURE_WHITE_SHADING, white_shading)

    def has_white_shading(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_WHITE_SHADING)

    def get_white_shading(self):
        return self.controls.getFeature(yarp.YARP_FEATURE_WHITE_SHADING)

    def get_white_shading_range(self):
        value1 = yarp.DVector(1)
        value2 = yarp.DVector(1)
        self.controls.getFeature(yarp.YARP_FEATURE_WHITE_SHADING, value1, value2)
        return value1[0], value2[0]

    def get_white_shading_mode(self):
        return 1 if self.controls.getMode(yarp.YARP_FEATURE_WHITE_SHADING)==2 else 0

    def set_white_shading_mode(self, mode):
        logging.debug("White Shading mode set to {}".format(mode))
        self.controls.setMode(yarp.YARP_FEATURE_WHITE_SHADING, mode)

    def has_white_shading_auto(self):
        return self.controls.hasAuto(yarp.YARP_FEATURE_WHITE_SHADING)

    # ===== PAN RELATED FUNCTIONS =====
    def set_pan(self, pan):
        logging.debug("Pan set to {}".format(pan))
        self.controls.setFeature(yarp.YARP_FEATURE_PAN, pan)

    def has_pan(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_PAN)

    def get_pan(self):
        return self.controls.getFeature(yarp.YARP_FEATURE_PAN)

    def get_pan_range(self):
        value1 = yarp.DVector(1)
        value2 = yarp.DVector(1)
        self.controls.getFeature(yarp.YARP_FEATURE_PAN, value1, value2)
        return value1[0], value2[0]

    def get_pan_mode(self):
        return 1 if self.controls.getMode(yarp.YARP_FEATURE_PAN)==2 else 0

    def set_pan_mode(self, mode):
        logging.debug("Pan mode set to {}".format(mode))
        self.controls.setMode(yarp.YARP_FEATURE_PAN, mode)

    def has_pan_auto(self):
        return self.controls.hasAuto(yarp.YARP_FEATURE_PAN)

    # ===== TILT RELATED FUNCTIONS =====
    def set_tilt(self, tilt):
        logging.debug("Tilt set to {}".format(tilt))
        self.controls.setFeature(yarp.YARP_FEATURE_TILT, tilt)

    def has_tilt(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_TILT)

    def get_tilt(self):
        return self.controls.getFeature(yarp.YARP_FEATURE_TILT)

    def get_tilt_range(self):
        value1 = yarp.DVector(1)
        value2 = yarp.DVector(1)
        self.controls.getFeature(yarp.YARP_FEATURE_TILT, value1, value2)
        return value1[0], value2[0]

    def get_tilt_mode(self):
        return 1 if self.controls.getMode(yarp.YARP_FEATURE_TILT)==2 else 0

    def set_tilt_mode(self, mode):
        logging.debug("Tilt mode set to {}".format(mode))
        self.controls.setMode(yarp.YARP_FEATURE_TILT, mode)

    def has_tilt_auto(self):
        return self.controls.hasAuto(yarp.YARP_FEATURE_TILT)

    # ===== OPTICAL FILTER RELATED FUNCTIONS =====
    def set_optical_filter(self, optical_filter):
        logging.debug("Optical Filter set to {}".format(optical_filter))
        self.controls.setFeature(yarp.YARP_FEATURE_OPTICAL_FILTER, optical_filter)

    def has_optical_filter(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_OPTICAL_FILTER)

    def get_optical_filter(self):
        return self.controls.getFeature(yarp.YARP_FEATURE_OPTICAL_FILTER)

    def get_optical_filter_range(self):
        value1 = yarp.DVector(1)
        value2 = yarp.DVector(1)
        self.controls.getFeature(yarp.YARP_FEATURE_OPTICAL_FILTER, value1, value2)
        return value1[0], value2[0]

    def get_optical_filter_mode(self):
        return 1 if self.controls.getMode(yarp.YARP_FEATURE_OPTICAL_FILTER)==2 else 0

    def set_optical_filter_mode(self, mode):
        logging.debug("Optical Filter mode set to {}".format(mode))
        self.controls.setMode(yarp.YARP_FEATURE_OPTICAL_FILTER, mode)

    def has_optical_filter_auto(self):
        return self.controls.hasAuto(yarp.YARP_FEATURE_OPTICAL_FILTER)

    # ===== CAPTURE SIZE RELATED FUNCTIONS =====
    def set_capture_size(self, capture_size):
        logging.debug("Capture Size set to {}".format(capture_size))
        self.controls.setFeature(yarp.YARP_FEATURE_CAPTURE_SIZE, capture_size)

    def has_capture_size(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_CAPTURE_SIZE)

    def get_capture_size(self):
        return self.controls.getFeature(yarp.YARP_FEATURE_CAPTURE_SIZE)

    def get_capture_size_range(self):
        value1 = yarp.DVector(1)
        value2 = yarp.DVector(1)
        self.controls.getFeature(yarp.YARP_FEATURE_CAPTURE_SIZE, value1, value2)
        return value1[0], value2[0]

    def get_capture_size_mode(self):
        return 1 if self.controls.getMode(yarp.YARP_FEATURE_CAPTURE_SIZE)==2 else 0

    def set_capture_size_mode(self, mode):
        logging.debug("Capture Size mode set to {}".format(mode))
        self.controls.setMode(yarp.YARP_FEATURE_CAPTURE_SIZE, mode)

    def has_capture_size_auto(self):
        return self.controls.hasAuto(yarp.YARP_FEATURE_CAPTURE_SIZE)

    # ===== CAPTURE QUALITY RELATED FUNCTIONS =====
    def set_capture_quality(self, capture_quality):
        logging.debug("Capture Quality set to {}".format(capture_quality))
        self.controls.setFeature(yarp.YARP_FEATURE_CAPTURE_QUALITY, capture_quality)

    def has_capture_quality(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_CAPTURE_QUALITY)

    def get_capture_quality(self):
        return self.controls.getFeature(yarp.YARP_FEATURE_CAPTURE_QUALITY)

    def get_capture_quality_range(self):
        value1 = yarp.DVector(1)
        value2 = yarp.DVector(1)
        self.controls.getFeature(yarp.YARP_FEATURE_CAPTURE_QUALITY, value1, value2)
        return value1[0], value2[0]

    def get_capture_quality_mode(self):
        return 1 if self.controls.getMode(yarp.YARP_FEATURE_CAPTURE_QUALITY)==2 else 0

    def set_capture_quality_mode(self, mode):
        logging.debug("Capture Quality mode set to {}".format(mode))
        self.controls.setMode(yarp.YARP_FEATURE_CAPTURE_QUALITY, mode)

    def has_capture_quality_auto(self):
        return self.controls.hasAuto(yarp.YARP_FEATURE_CAPTURE_QUALITY)

    # ===== MIRROR RELATED FUNCTIONS =====
    def set_mirror(self, mirror):
        logging.debug("Mirror set to {}".format(mirror))
        self.controls.setFeature(yarp.YARP_FEATURE_MIRROR, mirror)

    def has_mirror(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_MIRROR)

    def get_mirror(self):
        return self.controls.getFeature(yarp.YARP_FEATURE_MIRROR)

    def get_mirror_range(self):
        value1 = yarp.DVector(1)
        value2 = yarp.DVector(1)
        self.controls.getFeature(yarp.YARP_FEATURE_MIRROR, value1, value2)
        return value1[0], value2[0]

    def get_mirror_mode(self):
        return 1 if self.controls.getMode(yarp.YARP_FEATURE_MIRROR)==2 else 0

    def set_mirror_mode(self, mode):
        logging.debug("Mirror mode set to {}".format(mode))
        self.controls.setMode(yarp.YARP_FEATURE_MIRROR, mode)

    def has_mirror_auto(self):
        return self.controls.hasAuto(yarp.YARP_FEATURE_MIRROR)