"""
GrabberControls2GuiBackend
---------------------

Backend for the grabberControls2GUI

Author: David Estevez
Copyright: Universidad Carlos III de Madrid (C) 2017;
CopyPolicy: Released under the terms of the GNU GPL v2.0.
"""


import logging
import yarp


class GrabberControls2GuiBackend:
    def __init__(self, controls):
        self.controls = controls

    def init(self):
        pass

    def close(self):
        pass

    def set_zoom(self, zoom):
        logging.debug("Zoom set to {}".format(zoom))
        self.controls.setFeature(yarp.YARP_FEATURE_ZOOM, zoom)

    def has_zoom(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_ZOOM)

    def set_focus(self, focus):
        logging.debug("Focus set to {}".format(focus))
        self.controls.setFeature(yarp.YARP_FEATURE_FOCUS, focus)

    def has_focus(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_FOCUS)

    def set_gain(self, gain):
        logging.debug("Gain set to {}".format(gain))
        self.controls.setFeature(yarp.YARP_FEATURE_GAIN, gain)

    def has_gain(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_GAIN)

    def set_exposure(self, exposure):
        logging.debug("Exposure set to {}".format(exposure))
        self.controls.setFeature(yarp.YARP_FEATURE_EXPOSURE, exposure)

    def has_exposure(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_EXPOSURE)

    def set_FPS(self, fps):
        logging.debug("FPS set to {}".format(fps))
        self.controls.setFeature(yarp.YARP_FEATURE_FRAME_RATE, fps)

    def has_FPS(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_FRAME_RATE)

    def set_brightness(self, brightness):
        logging.debug("Brightness set to {}".format(brightness))
        self.controls.setFeature(yarp.YARP_FEATURE_BRIGHTNESS, brightness)

    def has_brightness(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_BRIGHTNESS)

    def set_shutter(self, shutter):
        logging.debug("Shutter set to {}".format(shutter))
        self.controls.setFeature(yarp.YARP_FEATURE_SHUTTER, shutter)

    def has_shutter(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_SHUTTER)

    def set_iris(self, iris):
        logging.debug("Iris set to {}".format(iris))
        self.controls.setFeature(yarp.YARP_FEATURE_IRIS, iris)

    def has_iris(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_IRIS)

    def set_temperature(self, temperature):
        logging.debug("Temperature set to {}".format(temperature))
        self.controls.setFeature(yarp.YARP_FEATURE_TEMPERATURE, temperature)

    def has_temperature(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_TEMPERATURE)

    def set_trigger(self, trigger):
        logging.debug("Trigger set to {}".format(trigger))
        self.controls.setFeature(yarp.YARP_FEATURE_TRIGGER, trigger)

    def has_trigger(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_TRIGGER)

    def set_trigger_delay(self, trigger_delay):
        logging.debug("Trigger Delay set to {}".format(trigger_delay))
        self.controls.setFeature(yarp.YARP_FEATURE_TRIGGER_DELAY, trigger_delay)

    def has_trigger_delay(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_TRIGGER_DELAY)

    def set_white_shading(self, white_shading):
        logging.debug("White Shading set to {}".format(white_shading))
        self.controls.setFeature(yarp.YARP_FEATURE_WHITE_SHADING, white_shading)

    def has_white_shading(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_WHITE_SHADING)

    def set_pan(self, pan):
        logging.debug("Pan set to {}".format(pan))
        self.controls.setFeature(yarp.YARP_FEATURE_PAN, pan)

    def has_pan(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_PAN)

    def set_tilt(self, tilt):
        logging.debug("Tilt set to {}".format(tilt))
        self.controls.setFeature(yarp.YARP_FEATURE_TILT, tilt)

    def has_tilt(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_TILT)

    def set_optical_filter(self, optical_filter):
        logging.debug("Optical Filter set to {}".format(optical_filter))
        self.controls.setFeature(yarp.YARP_FEATURE_OPTICAL_FILTER, optical_filter)

    def has_optical_filter(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_OPTICAL_FILTER)

    def set_capture_size(self, capture_size):
        logging.debug("Capture Size set to {}".format(capture_size))
        self.controls.setFeature(yarp.YARP_FEATURE_CAPTURE_SIZE, capture_size)

    def has_capture_size(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_CAPTURE_SIZE)

    def set_capture_quality(self, capture_quality):
        logging.debug("Capture Quality set to {}".format(capture_quality))
        self.controls.setFeature(yarp.YARP_FEATURE_CAPTURE_QUALITY, capture_quality)

    def has_capture_quality(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_CAPTURE_QUALITY)

    def set_mirror(self, mirror):
        logging.debug("Mirror set to {}".format(mirror))
        self.controls.setFeature(yarp.YARP_FEATURE_MIRROR, mirror)

    def has_mirror(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_MIRROR)

    def set_sharpness(self, sharpness):
        logging.debug("Sharpness set to {}".format(sharpness))
        self.controls.setFeature(yarp.YARP_FEATURE_SHARPNESS, sharpness)

    def has_sharpness(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_SHARPNESS)

    def set_white_balance(self, white_balance):
        logging.debug("White Balance set to {}".format(white_balance))
        self.controls.setFeature(yarp.YARP_FEATURE_WHITE_BALANCE, white_balance)

    def has_white_balance(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_WHITE_BALANCE)

    def set_hue(self, hue):
        logging.debug("Hue set to {}".format(hue))
        self.controls.setFeature(yarp.YARP_FEATURE_HUE, hue)

    def has_hue(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_HUE)

    def set_saturation(self, saturation):
        logging.debug("Saturation set to {}".format(saturation))
        self.controls.setFeature(yarp.YARP_FEATURE_SATURATION, saturation)

    def has_saturation(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_SATURATION)

    def set_gamma(self, gamma):
        logging.debug("Gamma set to {}".format(gamma))
        self.controls.setFeature(yarp.YARP_FEATURE_GAMMA, gamma)

    def has_gamma(self):
        return self.controls.hasFeature(yarp.YARP_FEATURE_GAMMA)
