import logging
import yarp


class GrabberControls2GuiBackend:
    def __init__(self, controls):
        self.controls = controls
        print("---------------", self.controls.setMode(yarp.YARP_FEATURE_GAIN, yarp.MODE_MANUAL))

    def init(self):
        pass

    def close(self):
        pass

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
        self.controls.getFeature2(yarp.YARP_FEATURE_ZOOM, value1, value2)
        return value1[0], value2[0]

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
        self.controls.getFeature2(yarp.YARP_FEATURE_FOCUS, value1, value2)
        return value1[0], value2[0]

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
        self.controls.getFeature2(yarp.YARP_FEATURE_GAIN, value1, value2)
        return value1[0], value2[0]

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
        self.controls.getFeature2(yarp.YARP_FEATURE_EXPOSURE, value1, value2)
        return value1[0], value2[0]

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
        self.controls.getFeature2(yarp.YARP_FEATURE_FRAME_RATE, value1, value2)
        return value1[0], value2[0]

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
        self.controls.getFeature2(yarp.YARP_FEATURE_BRIGHTNESS, value1, value2)
        return value1[0], value2[0]

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
        self.controls.getFeature2(yarp.YARP_FEATURE_SHUTTER, value1, value2)
        return value1[0], value2[0]

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
        self.controls.getFeature2(yarp.YARP_FEATURE_IRIS, value1, value2)
        return value1[0], value2[0]

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
        self.controls.getFeature2(yarp.YARP_FEATURE_TEMPERATURE, value1, value2)
        return value1[0], value2[0]

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
        self.controls.getFeature2(yarp.YARP_FEATURE_TRIGGER, value1, value2)
        return value1[0], value2[0]

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
        self.controls.getFeature2(yarp.YARP_FEATURE_TRIGGER_DELAY, value1, value2)
        return value1[0], value2[0]

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
        self.controls.getFeature2(yarp.YARP_FEATURE_WHITE_SHADING, value1, value2)
        return value1[0], value2[0]

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
        self.controls.getFeature2(yarp.YARP_FEATURE_PAN, value1, value2)
        return value1[0], value2[0]

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
        self.controls.getFeature2(yarp.YARP_FEATURE_TILT, value1, value2)
        return value1[0], value2[0]

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
        self.controls.getFeature2(yarp.YARP_FEATURE_OPTICAL_FILTER, value1, value2)
        return value1[0], value2[0]

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
        self.controls.getFeature2(yarp.YARP_FEATURE_CAPTURE_SIZE, value1, value2)
        return value1[0], value2[0]

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
        self.controls.getFeature2(yarp.YARP_FEATURE_CAPTURE_QUALITY, value1, value2)
        return value1[0], value2[0]

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
        self.controls.getFeature2(yarp.YARP_FEATURE_MIRROR, value1, value2)
        return value1[0], value2[0]

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
        self.controls.getFeature2(yarp.YARP_FEATURE_SHARPNESS, value1, value2)
        return value1[0], value2[0]

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
        self.controls.getFeature2(yarp.YARP_FEATURE_WHITE_BALANCE, value1, value2)
        return value1[0], value2[0]

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
        self.controls.getFeature2(yarp.YARP_FEATURE_HUE, value1, value2)
        return value1[0], value2[0]

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
        self.controls.getFeature2(yarp.YARP_FEATURE_SATURATION, value1, value2)
        return value1[0], value2[0]

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
        self.controls.getFeature2(yarp.YARP_FEATURE_GAMMA, value1, value2)
        return value1[0], value2[0]