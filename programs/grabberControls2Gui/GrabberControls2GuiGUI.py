"""
AravisGigEController
---------------------

Frontend for the AravisGigEController

Author: David Estevez
Copyright: Universidad Carlos III de Madrid (C) 2017;
CopyPolicy: Released under the terms of the GNU GPL v2.0.
"""

import os
import sys
import ctypes
import yarp
import numpy as np
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2 import QtUiTools


def load_ui(file_name, where=None):
    """
    Loads a .UI file into the corresponding Qt Python object
    :param file_name: UI file path
    :param where: Use this parameter to load the UI into an existing class (i.e. to override methods)
    :return: loaded UI
    """
    # Create a QtLoader
    loader = QtUiTools.QUiLoader()

    # Open the UI file
    ui_file = QtCore.QFile(file_name)
    ui_file.open(QtCore.QFile.ReadOnly)

    # Load the contents of the file
    ui = loader.load(ui_file, where)

    # Close the file
    ui_file.close()

    return ui


class GrabberControls2GuiGUI(QtWidgets.QWidget):
    def __init__(self, controller, remote_port, parent=None):
        super().__init__(parent)
        self.controller = controller

        # Configuración robusta del puerto de imágenes
        self.camera_port = yarp.BufferedPortImageRgb()

        if not self.camera_port.open("/viewer") or not yarp.Network.connect(remote_port, "/viewer"):
            return

        self.camera_port.setStrict(False)
        self.camera_port.setReadOnly()

        self.zoomSlider = None
        self.zoomSpinBox = None
        self.focusSlider = None
        self.focusSpinBox = None
        self.gainSlider = None
        self.gainSpinBox = None
        self.exposureSlider = None
        self.exposureSpinBox = None
        self.fpsSlider = None
        self.fpsSpinBox = None

        self.brightnessSlider = None
        self.brightnessSpinBox = None
        self.shutterSlider = None
        self.shutterSpinBox = None
        self.irisSlider = None
        self.irisSpinBox = None
        self.temperatureSlider = None
        self.temperatureSpinBox = None
        self.whiteShadingSlider = None
        self.whiteShadingSpinBox = None
        self.captureSizeSlider = None
        self.captureSizeSpinBox = None
        self.captureQualitySlider = None
        self.captureQualitySpinBox = None
        self.mirrorSlider = None
        self.mirrorSpinBox = None
        self.sharpnessSlider = None
        self.sharpnessSpinBox = None
        self.whiteBalanceSlider = None
        self.whiteBalanceSpinBox = None
        self.hueSlider = None
        self.hueSpinBox = None
        self.saturationSlider = None
        self.saturationSpinBox = None
        self.gammaSlider = None
        self.gammaSpinBox = None
        self.triggerSlider = None
        self.triggerSpinBox = None
        self.triggerDelaySlider = None
        self.triggerDelaySpinBox = None
        self.panSlider = None
        self.panSpinBox = None
        self.tiltSlider = None
        self.tiltSpinBox = None
        self.opticalFilterSlider = None
        self.opticalFilterSpinBox = None

        self.zoomLayout = None
        self.focusLayout = None
        self.gainLayout = None
        self.exposureLayout = None
        self.fpsLayout = None
        self.brightnessLayout = None
        self.shutterLayout = None
        self.irisLayout = None
        self.temperatureLayout = None
        self.whiteShadingLayout = None
        self.captureSizeLayout = None
        self.captureQualityLayout = None
        self.mirrorLayout = None
        self.sharpnessLayout = None
        self.whiteBalanceLayout = None
        self.hueLayout = None
        self.saturationLayout = None
        self.gammaLayout = None
        self.triggerLayout = None
        self.triggerDelayLayout = None
        self.panLayout = None
        self.tiltLayout = None
        self.opticalFilterLayout = None
        self.current_pixmap = None
        self.cameraView = None

        self.setupUI()
        self.resetValues()
        self.startCameraReading()

    def setupUI(self):
        # Load UI and set it as main layout
        ui_file_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'templates', 'GrabberControls2GuiGUI.ui')
        main_widget = load_ui(ui_file_path, self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(main_widget)
        self.setLayout(layout)

        # Get a reference to all required widgets
        self.zoomSlider = self.findChild(QtWidgets.QSlider, 'zoomSlider')
        self.zoomSpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'zoomSpinBox')
        self.focusSlider = self.findChild(QtWidgets.QSlider, 'focusSlider')
        self.focusSpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'focusSpinBox')
        self.gainSlider = self.findChild(QtWidgets.QSlider, 'gainSlider')
        self.gainSpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'gainSpinBox')
        self.exposureSlider = self.findChild(QtWidgets.QSlider, 'exposureSlider')
        self.exposureSpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'exposureSpinBox')
        self.fpsSlider = self.findChild(QtWidgets.QSlider, 'fpsSlider')
        self.fpsSpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'fpsSpinBox')
        self.brightnessSlider = self.findChild(QtWidgets.QSlider, 'brightnessSlider')
        self.brightnessSpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'brightnessSpinBox')
        self.shutterSlider = self.findChild(QtWidgets.QSlider, 'shutterSlider')
        self.shutterSpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'shutterSpinBox')
        self.irisSlider = self.findChild(QtWidgets.QSlider, 'irisSlider')
        self.irisSpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'irisSpinBox')
        self.temperatureSlider = self.findChild(QtWidgets.QSlider, 'temperatureSlider')
        self.temperatureSpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'temperatureSpinBox')
        self.whiteShadingSlider = self.findChild(QtWidgets.QSlider, 'whiteShadingSlider')
        self.whiteShadingSpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'whiteShadingSpinBox')
        self.captureSizeSlider = self.findChild(QtWidgets.QSlider, 'captureSizeSlider')
        self.captureSizeSpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'captureSizeSpinBox')
        self.captureQualitySlider = self.findChild(QtWidgets.QSlider, 'captureQualitySlider')
        self.captureQualitySpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'captureQualitySpinBox')
        self.mirrorSlider = self.findChild(QtWidgets.QSlider, 'mirrorSlider')
        self.mirrorSpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'mirrorSpinBox')
        self.sharpnessSlider = self.findChild(QtWidgets.QSlider, 'sharpnessSlider')
        self.sharpnessSpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'sharpnessSpinBox')
        self.whiteBalanceSlider = self.findChild(QtWidgets.QSlider, 'whiteBalanceSlider')
        self.whiteBalanceSpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'whiteBalanceSpinBox')
        self.hueSlider = self.findChild(QtWidgets.QSlider, 'hueSlider')
        self.hueSpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'hueSpinBox')
        self.saturationSlider = self.findChild(QtWidgets.QSlider, 'saturationSlider')
        self.saturationSpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'saturationSpinBox')
        self.gammaSlider = self.findChild(QtWidgets.QSlider, 'gammaSlider')
        self.gammaSpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'gammaSpinBox')
        self.triggerSlider = self.findChild(QtWidgets.QSlider, 'triggerSlider')
        self.triggerSpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'triggerSpinBox')
        self.triggerDelaySlider = self.findChild(QtWidgets.QSlider, 'triggerDelaySlider')
        self.triggerDelaySpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'triggerDelaySpinBox')
        self.panSlider = self.findChild(QtWidgets.QSlider, 'panSlider')
        self.panSpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'panSpinBox')
        self.tiltSlider = self.findChild(QtWidgets.QSlider, 'tiltSlider')
        self.tiltSpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'tiltSpinBox')
        self.opticalFilterSlider = self.findChild(QtWidgets.QSlider, 'opticalFilterSlider')
        self.opticalFilterSpinBox = self.findChild(QtWidgets.QDoubleSpinBox, 'opticalFilterSpinBox')

        # Get a reference to all required layouts
        self.zoomLayout = self.findChild(QtWidgets.QHBoxLayout, 'zoomLayout')
        self.focusLayout = self.findChild(QtWidgets.QHBoxLayout, 'focusLayout')
        self.gainLayout = self.findChild(QtWidgets.QHBoxLayout, 'gainLayout')
        self.exposureLayout = self.findChild(QtWidgets.QHBoxLayout, 'exposureLayout')
        self.fpsLayout = self.findChild(QtWidgets.QHBoxLayout, 'fpsLayout')
        self.brightnessLayout = self.findChild(QtWidgets.QHBoxLayout, 'brightnessLayout')
        self.shutterLayout = self.findChild(QtWidgets.QHBoxLayout, 'shutterLayout')
        self.irisLayout = self.findChild(QtWidgets.QHBoxLayout, 'irisLayout')
        self.temperatureLayout = self.findChild(QtWidgets.QHBoxLayout, 'temperatureLayout')
        self.whiteShadingLayout = self.findChild(QtWidgets.QHBoxLayout, 'whiteShadingLayout')
        self.captureSizeLayout = self.findChild(QtWidgets.QHBoxLayout, 'captureSizeLayout')
        self.captureQualityLayout = self.findChild(QtWidgets.QHBoxLayout, 'captureQualityLayout')
        self.mirrorLayout = self.findChild(QtWidgets.QHBoxLayout, 'mirrorLayout')
        self.sharpnessLayout = self.findChild(QtWidgets.QHBoxLayout, 'sharpnessLayout')
        self.whiteBalanceLayout = self.findChild(QtWidgets.QHBoxLayout, 'whiteBalanceLayout')
        self.hueLayout = self.findChild(QtWidgets.QHBoxLayout, 'hueLayout')
        self.saturationLayout = self.findChild(QtWidgets.QHBoxLayout, 'saturationLayout')
        self.gammaLayout = self.findChild(QtWidgets.QHBoxLayout, 'gammaLayout')
        self.triggerLayout = self.findChild(QtWidgets.QHBoxLayout, 'triggerLayout')
        self.triggerDelayLayout = self.findChild(QtWidgets.QHBoxLayout, 'triggerDelayLayout')
        self.panLayout = self.findChild(QtWidgets.QHBoxLayout, 'panLayout')
        self.tiltLayout = self.findChild(QtWidgets.QHBoxLayout, 'tiltLayout')
        self.opticalFilterLayout = self.findChild(QtWidgets.QHBoxLayout, 'opticalFilterLayout')

        self.cameraView = self.findChild(QtWidgets.QLabel, 'cameraView')
        if self.cameraView is not None:
            self.cameraView.setText("Esperando imagen de la cámara...")

        self.setMinimumSize(640, 480)
        self.cameraView.setScaledContents(False)
        self.cameraView.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)

        # Set visibility of widgets based on controller features
        self.visibility()

        # Connect to signals:
        self.zoomSlider.valueChanged.connect(self.onZoomSliderChanged)
        self.zoomSpinBox.valueChanged.connect(self.onZoomSpinBoxChanged)
        self.focusSlider.valueChanged.connect(self.onFocusSliderChanged)
        self.focusSpinBox.valueChanged.connect(self.onFocusSpinBoxChanged)
        self.gainSlider.valueChanged.connect(self.onGainSliderChanged)
        self.gainSpinBox.valueChanged.connect(self.onGainSpinBoxChanged)
        self.exposureSlider.valueChanged.connect(self.onExposureSliderChanged)
        self.exposureSpinBox.valueChanged.connect(self.onExposureSpinBoxChanged)
        self.fpsSlider.valueChanged.connect(self.onfpsSliderChanged)
        self.fpsSpinBox.valueChanged.connect(self.onfpsSpinBoxChanged)
        self.brightnessSlider.valueChanged.connect(self.onBrightnessSliderChanged)
        self.brightnessSpinBox.valueChanged.connect(self.onBrightnessSpinBoxChanged)
        self.shutterSlider.valueChanged.connect(self.onShutterSliderChanged)
        self.shutterSpinBox.valueChanged.connect(self.onShutterSpinBoxChanged)
        self.irisSlider.valueChanged.connect(self.onIrisSliderChanged)
        self.irisSpinBox.valueChanged.connect(self.onIrisSpinBoxChanged)
        self.temperatureSlider.valueChanged.connect(self.onTemperatureSliderChanged)
        self.temperatureSpinBox.valueChanged.connect(self.onTemperatureSpinBoxChanged)
        self.whiteShadingSlider.valueChanged.connect(self.onWhiteShadingSliderChanged)
        self.whiteShadingSpinBox.valueChanged.connect(self.onWhiteShadingSpinBoxChanged)
        self.captureSizeSlider.valueChanged.connect(self.onCaptureSizeSliderChanged)
        self.captureSizeSpinBox.valueChanged.connect(self.onCaptureSizeSpinBoxChanged)
        self.captureQualitySlider.valueChanged.connect(self.onCaptureQualitySliderChanged)
        self.captureQualitySpinBox.valueChanged.connect(self.onCaptureQualitySpinBoxChanged)
        self.mirrorSlider.valueChanged.connect(self.onMirrorSliderChanged)
        self.mirrorSpinBox.valueChanged.connect(self.onMirrorSpinBoxChanged)
        self.sharpnessSlider.valueChanged.connect(self.onSharpnessSliderChanged)
        self.sharpnessSpinBox.valueChanged.connect(self.onSharpnessSpinBoxChanged)
        self.whiteBalanceSlider.valueChanged.connect(self.onWhiteBalanceSliderChanged)
        self.whiteBalanceSpinBox.valueChanged.connect(self.onWhiteBalanceSpinBoxChanged)
        self.hueSlider.valueChanged.connect(self.onHueSliderChanged)
        self.hueSpinBox.valueChanged.connect(self.onHueSpinBoxChanged)
        self.saturationSlider.valueChanged.connect(self.onSaturationSliderChanged)
        self.saturationSpinBox.valueChanged.connect(self.onSaturationSpinBoxChanged)
        self.gammaSlider.valueChanged.connect(self.onGammaSliderChanged)
        self.gammaSpinBox.valueChanged.connect(self.onGammaSpinBoxChanged)
        self.triggerSlider.valueChanged.connect(self.onTriggerSliderChanged)
        self.triggerSpinBox.valueChanged.connect(self.onTriggerSpinBoxChanged)
        self.triggerDelaySlider.valueChanged.connect(self.onTriggerDelaySliderChanged)
        self.triggerDelaySpinBox.valueChanged.connect(self.onTriggerDelaySpinBoxChanged)
        self.panSlider.valueChanged.connect(self.onPanSliderChanged)
        self.panSpinBox.valueChanged.connect(self.onPanSpinBoxChanged)
        self.tiltSlider.valueChanged.connect(self.onTiltSliderChanged)
        self.tiltSpinBox.valueChanged.connect(self.onTiltSpinBoxChanged)
        self.opticalFilterSlider.valueChanged.connect(self.onOpticalFilterSliderChanged)
        self.opticalFilterSpinBox.valueChanged.connect(self.onOpticalFilterSpinBoxChanged)

    def resetValues(self):
        self.zoomSlider.setValue(self.controller.get_zoom())
        self.zoomSpinBox.setValue(self.controller.get_zoom())
        self.focusSlider.setValue(self.controller.get_focus())
        self.focusSpinBox.setValue(self.controller.get_focus())
        self.gainSlider.setValue(self.controller.get_gain())
        self.gainSpinBox.setValue(self.controller.get_gain())
        self.exposureSlider.setValue(self.controller.get_exposure())
        self.exposureSpinBox.setValue(self.controller.get_exposure())
        self.fpsSlider.setValue(self.controller.get_FPS())
        self.fpsSpinBox.setValue(self.controller.get_FPS())
        self.brightnessSlider.setValue(self.controller.get_brightness())
        self.brightnessSpinBox.setValue(self.controller.get_brightness())
        self.shutterSlider.setValue(self.controller.get_shutter())
        self.shutterSpinBox.setValue(self.controller.get_shutter())
        self.irisSlider.setValue(self.controller.get_iris())
        self.irisSpinBox.setValue(self.controller.get_iris())
        self.temperatureSlider.setValue(self.controller.get_temperature())
        self.temperatureSpinBox.setValue(self.controller.get_temperature())
        self.whiteShadingSlider.setValue(self.controller.get_white_shading())
        self.whiteShadingSpinBox.setValue(self.controller.get_white_shading())
        self.captureSizeSlider.setValue(self.controller.get_capture_size())
        self.captureSizeSpinBox.setValue(self.controller.get_capture_size())
        self.captureQualitySlider.setValue(self.controller.get_capture_quality())
        self.captureQualitySpinBox.setValue(self.controller.get_capture_quality())
        self.mirrorSlider.setValue(self.controller.get_mirror())
        self.mirrorSpinBox.setValue(self.controller.get_mirror())
        self.sharpnessSlider.setValue(self.controller.get_sharpness())
        self.sharpnessSpinBox.setValue(self.controller.get_sharpness())
        self.whiteBalanceSlider.setValue(self.controller.get_white_balance())
        self.whiteBalanceSpinBox.setValue(self.controller.get_white_balance())
        self.hueSlider.setValue(self.controller.get_hue())
        self.hueSpinBox.setValue(self.controller.get_hue())
        self.saturationSlider.setValue(self.controller.get_saturation())
        self.saturationSpinBox.setValue(self.controller.get_saturation())
        self.gammaSlider.setValue(self.controller.get_gamma())
        self.gammaSpinBox.setValue(self.controller.get_gamma())
        self.triggerSlider.setValue(self.controller.get_trigger())
        self.triggerSpinBox.setValue(self.controller.get_trigger())
        self.triggerDelaySlider.setValue(self.controller.get_trigger_delay())
        self.triggerDelaySpinBox.setValue(self.controller.get_trigger_delay())
        self.panSlider.setValue(self.controller.get_pan())
        self.panSpinBox.setValue(self.controller.get_pan())
        self.tiltSlider.setValue(self.controller.get_tilt())
        self.tiltSpinBox.setValue(self.controller.get_tilt())
        self.opticalFilterSlider.setValue(self.controller.get_optical_filter())
        self.opticalFilterSpinBox.setValue(self.controller.get_optical_filter())

    def visibility(self):
        if not self.controller.has_brightness():
            self.brightnessSlider.setVisible(False)
            self.brightnessSpinBox.setVisible(False)
            self.findChild(QtWidgets.QLabel, 'brightnessLabel').setVisible(False)
        else:
            self.brightnessSlider.setEnabled(True)
            self.brightnessSpinBox.setEnabled(True)
            self.findChild(QtWidgets.QLabel, 'brightnessLabel').setEnabled(True)
            min_val, max_val = self.controller.get_brightness_range()
            self.brightnessSlider.setRange(int(min_val), int(max_val))  # Slider sigue usando enteros
            self.brightnessSpinBox.setRange(min_val, max_val)  # SpinBox usa valores decimales

        if not self.controller.has_shutter():
            self.shutterSlider.setVisible(False)
            self.shutterSpinBox.setVisible(False)
            self.findChild(QtWidgets.QLabel, 'shutterLabel').setVisible(False)
        else:
            self.shutterSlider.setEnabled(True)
            self.shutterSpinBox.setEnabled(True)
            self.findChild(QtWidgets.QLabel, 'shutterLabel').setEnabled(True)
            min_val, max_val = self.controller.get_shutter_range()
            self.shutterSlider.setRange(int(min_val), int(max_val))
            self.shutterSpinBox.setRange(min_val, max_val)

        if not self.controller.has_iris():
            self.irisSlider.setVisible(False)
            self.irisSpinBox.setVisible(False)
            self.findChild(QtWidgets.QLabel, 'irisLabel').setVisible(False)
        else:
            self.irisSlider.setEnabled(True)
            self.irisSpinBox.setEnabled(True)
            self.findChild(QtWidgets.QLabel, 'irisLabel').setEnabled(True)
            min_val, max_val = self.controller.get_iris_range()
            self.irisSlider.setRange(int(min_val), int(max_val))
            self.irisSpinBox.setRange(min_val, max_val)

        if not self.controller.has_focus():
            self.focusSlider.setVisible(False)
            self.focusSpinBox.setVisible(False)
            self.findChild(QtWidgets.QLabel, 'focusLabel').setVisible(False)
        else:
            self.focusSlider.setEnabled(True)
            self.focusSpinBox.setEnabled(True)
            self.findChild(QtWidgets.QLabel, 'focusLabel').setEnabled(True)
            min_val, max_val = self.controller.get_focus_range()
            self.focusSlider.setRange(int(min_val), int(max_val))
            self.focusSpinBox.setRange(min_val, max_val)

        if not self.controller.has_temperature():
            self.temperatureSlider.setVisible(False)
            self.temperatureSpinBox.setVisible(False)
            self.findChild(QtWidgets.QLabel, 'temperatureLabel').setVisible(False)
        else:
            self.temperatureSlider.setEnabled(True)
            self.temperatureSpinBox.setEnabled(True)
            self.findChild(QtWidgets.QLabel, 'temperatureLabel').setEnabled(True)
            min_val, max_val = self.controller.get_temperature_range()
            self.temperatureSlider.setRange(int(min_val), int(max_val))
            self.temperatureSpinBox.setRange(min_val, max_val)

        if not self.controller.has_white_shading():
            self.whiteShadingSlider.setVisible(False)
            self.whiteShadingSpinBox.setVisible(False)
            self.findChild(QtWidgets.QLabel, 'whiteShadingLabel').setVisible(False)
        else:
            self.whiteShadingSlider.setEnabled(True)
            self.whiteShadingSpinBox.setEnabled(True)
            self.findChild(QtWidgets.QLabel, 'whiteShadingLabel').setEnabled(True)
            min_val, max_val = self.controller.get_white_shading_range()
            self.whiteShadingSlider.setRange(int(min_val), int(max_val))
            self.whiteShadingSpinBox.setRange(min_val, max_val)

        if not self.controller.has_capture_size():
            self.captureSizeSlider.setVisible(False)
            self.captureSizeSpinBox.setVisible(False)
            self.findChild(QtWidgets.QLabel, 'captureSizeLabel').setVisible(False)
        else:
            self.captureSizeSlider.setEnabled(True)
            self.captureSizeSpinBox.setEnabled(True)
            self.findChild(QtWidgets.QLabel, 'captureSizeLabel').setEnabled(True)
            min_val, max_val = self.controller.get_capture_size_range()
            self.captureSizeSlider.setRange(int(min_val), int(max_val))
            self.captureSizeSpinBox.setRange(min_val, max_val)

        if not self.controller.has_capture_quality():
            self.captureQualitySlider.setVisible(False)
            self.captureQualitySpinBox.setVisible(False)
            self.findChild(QtWidgets.QLabel, 'captureQualityLabel').setVisible(False)
        else:
            self.captureQualitySlider.setEnabled(True)
            self.captureQualitySpinBox.setEnabled(True)
            self.findChild(QtWidgets.QLabel, 'captureQualityLabel').setEnabled(True)
            min_val, max_val = self.controller.get_capture_quality_range()
            self.captureQualitySlider.setRange(int(min_val), int(max_val))
            self.captureQualitySpinBox.setRange(min_val, max_val)

        if not self.controller.has_mirror():
            self.mirrorSlider.setVisible(False)
            self.mirrorSpinBox.setVisible(False)
            self.findChild(QtWidgets.QLabel, 'mirrorLabel').setVisible(False)
        else:
            self.mirrorSlider.setEnabled(True)
            self.mirrorSpinBox.setEnabled(True)
            self.findChild(QtWidgets.QLabel, 'mirrorLabel').setEnabled(True)
            min_val, max_val = self.controller.get_mirror_range()
            self.mirrorSlider.setRange(int(min_val), int(max_val))
            self.mirrorSpinBox.setRange(min_val, max_val)

        if not self.controller.has_sharpness():
            self.sharpnessSlider.setVisible(False)
            self.sharpnessSpinBox.setVisible(False)
            self.findChild(QtWidgets.QLabel, 'sharpnessLabel').setVisible(False)
        else:
            self.sharpnessSlider.setEnabled(True)
            self.sharpnessSpinBox.setEnabled(True)
            self.findChild(QtWidgets.QLabel, 'sharpnessLabel').setEnabled(True)
            min_val, max_val = self.controller.get_sharpness_range()
            self.sharpnessSlider.setRange(int(min_val), int(max_val))
            self.sharpnessSpinBox.setRange(min_val, max_val)

        if not self.controller.has_white_balance():
            self.whiteBalanceSlider.setVisible(False)
            self.whiteBalanceSpinBox.setVisible(False)
            self.findChild(QtWidgets.QLabel, 'whiteBalanceLabel').setVisible(False)
        else:
            self.whiteBalanceSlider.setEnabled(True)
            self.whiteBalanceSpinBox.setEnabled(True)
            self.findChild(QtWidgets.QLabel, 'whiteBalanceLabel').setEnabled(True)
            min_val, max_val = self.controller.get_white_balance_range()
            self.whiteBalanceSlider.setRange(int(min_val), int(max_val))
            self.whiteBalanceSpinBox.setRange(min_val, max_val)

        if not self.controller.has_hue():
            self.hueSlider.setVisible(False)
            self.hueSpinBox.setVisible(False)
            self.findChild(QtWidgets.QLabel, 'hueLabel').setVisible(False)
        else:
            self.hueSlider.setEnabled(True)
            self.hueSpinBox.setEnabled(True)
            self.findChild(QtWidgets.QLabel, 'hueLabel').setEnabled(True)
            min_val, max_val = self.controller.get_hue_range()
            self.hueSlider.setRange(int(min_val), int(max_val))
            self.hueSpinBox.setRange(min_val, max_val)

        if not self.controller.has_saturation():
            self.saturationSlider.setVisible(False)
            self.saturationSpinBox.setVisible(False)
            self.findChild(QtWidgets.QLabel, 'saturationLabel').setVisible(False)
        else:
            self.saturationSlider.setEnabled(True)
            self.saturationSpinBox.setEnabled(True)
            self.findChild(QtWidgets.QLabel, 'saturationLabel').setEnabled(True)
            min_val, max_val = self.controller.get_saturation_range()
            self.saturationSlider.setRange(int(min_val), int(max_val))
            self.saturationSpinBox.setRange(min_val, max_val)

        if not self.controller.has_gamma():
            self.gammaSlider.setVisible(False)
            self.gammaSpinBox.setVisible(False)
            self.findChild(QtWidgets.QLabel, 'gammaLabel').setVisible(False)
        else:
            self.gammaSlider.setEnabled(True)
            self.gammaSpinBox.setEnabled(True)
            self.findChild(QtWidgets.QLabel, 'gammaLabel').setEnabled(True)
            min_val, max_val = self.controller.get_gamma_range()
            self.gammaSlider.setRange(int(min_val), int(max_val))
            self.gammaSpinBox.setRange(min_val, max_val)

        if not self.controller.has_trigger():
            self.triggerSlider.setVisible(False)
            self.triggerSpinBox.setVisible(False)
            self.findChild(QtWidgets.QLabel, 'triggerLabel').setVisible(False)
        else:
            self.triggerSlider.setEnabled(True)
            self.triggerSpinBox.setEnabled(True)
            self.findChild(QtWidgets.QLabel, 'triggerLabel').setEnabled(True)
            min_val, max_val = self.controller.get_trigger_range()
            self.triggerSlider.setRange(int(min_val), int(max_val))
            self.triggerSpinBox.setRange(min_val, max_val)

        if not self.controller.has_trigger_delay():
            self.triggerDelaySlider.setVisible(False)
            self.triggerDelaySpinBox.setVisible(False)
            self.findChild(QtWidgets.QLabel, 'triggerDelayLabel').setVisible(False)
        else:
            self.triggerDelaySlider.setEnabled(True)
            self.triggerDelaySpinBox.setEnabled(True)
            self.findChild(QtWidgets.QLabel, 'triggerDelayLabel').setEnabled(True)
            min_val, max_val = self.controller.get_trigger_delay_range()
            self.triggerDelaySlider.setRange(int(min_val), int(max_val))
            self.triggerDelaySpinBox.setRange(min_val, max_val)

        if not self.controller.has_zoom():
            self.zoomSlider.setVisible(False)
            self.zoomSpinBox.setVisible(False)
            self.findChild(QtWidgets.QLabel, 'zoomLabel').setVisible(False)
        else:
            self.zoomSlider.setEnabled(True)
            self.zoomSpinBox.setEnabled(True)
            self.findChild(QtWidgets.QLabel, 'zoomLabel').setEnabled(True)
            min_val, max_val = self.controller.get_zoom_range()
            self.zoomSlider.setRange(int(min_val), int(max_val))
            self.zoomSpinBox.setRange(min_val, max_val)

        if not self.controller.has_pan():
            self.panSlider.setVisible(False)
            self.panSpinBox.setVisible(False)
            self.findChild(QtWidgets.QLabel, 'panLabel').setVisible(False)
        else:
            self.panSlider.setEnabled(True)
            self.panSpinBox.setEnabled(True)
            self.findChild(QtWidgets.QLabel, 'panLabel').setEnabled(True)
            min_val, max_val = self.controller.get_pan_range()
            self.panSlider.setRange(int(min_val), int(max_val))
            self.panSpinBox.setRange(min_val, max_val)

        if not self.controller.has_tilt():
            self.tiltSlider.setVisible(False)
            self.tiltSpinBox.setVisible(False)
            self.findChild(QtWidgets.QLabel, 'tiltLabel').setVisible(False)
        else:
            self.tiltSlider.setEnabled(True)
            self.tiltSpinBox.setEnabled(True)
            self.findChild(QtWidgets.QLabel, 'tiltLabel').setEnabled(True)
            min_val, max_val = self.controller.get_tilt_range()
            self.tiltSlider.setRange(int(min_val), int(max_val))
            self.tiltSpinBox.setRange(min_val, max_val)

        if not self.controller.has_optical_filter():
            self.opticalFilterSlider.setVisible(False)
            self.opticalFilterSpinBox.setVisible(False)
            self.findChild(QtWidgets.QLabel, 'opticalFilterLabel').setVisible(False)
        else:
            self.opticalFilterSlider.setEnabled(True)
            self.opticalFilterSpinBox.setEnabled(True)
            self.findChild(QtWidgets.QLabel, 'opticalFilterLabel').setEnabled(True)
            min_val, max_val = self.controller.get_optical_filter_range()
            self.opticalFilterSlider.setRange(int(min_val), int(max_val))
            self.opticalFilterSpinBox.setRange(min_val, max_val)

        if not self.controller.has_FPS():
            self.fpsSlider.setVisible(False)
            self.fpsSpinBox.setVisible(False)
            self.findChild(QtWidgets.QLabel, 'fpsLabel').setVisible(False)
        else:
            self.fpsSlider.setEnabled(True)
            self.fpsSpinBox.setEnabled(True)
            self.findChild(QtWidgets.QLabel, 'fpsLabel').setEnabled(True)
            min_val, max_val = self.controller.get_FPS_range()
            self.fpsSlider.setRange(int(min_val), int(max_val))
            self.fpsSpinBox.setRange(min_val, max_val)

    def updateCameraView(self):
        try:
            # Leer imagen del puerto YARP (non-blocking)
            yarp_img = self.camera_port.read(False)

            if yarp_img is None:
                return  # No hay nueva imagen disponible

            # Obtener dimensiones
            width = yarp_img.width()
            height = yarp_img.height()

            if width <= 0 or height <= 0:
                print("Dimensiones de imagen inválidas")
                return

            # Obtener el buffer de datos como bytes
            img_ptr = int(yarp_img.getRawImage())
            img_size = yarp_img.getRawImageSize()

            # Crear bytes usando ctypes (forma correcta)
            img_data = (ctypes.c_ubyte * img_size).from_address(img_ptr)
            img_bytes = bytes(img_data)

            # Crear QImage
            qimage = QtGui.QImage(img_bytes, width, height, yarp_img.getRowSize(), QtGui.QImage.Format_RGB888)

            if qimage.isNull():
                print("No se pudo crear QImage")
                return

            # Actualizar la visualización
            self.current_pixmap = QtGui.QPixmap.fromImage(qimage)
            self.updateScaledPixmap()

        except Exception as e:
            print(f"Error al procesar imagen: {str(e)}")

    def startCameraReading(self):
        """Inicia el streaming forzando la conexión"""
        # Enviar comando de inicio (si tu dispositivo lo soporta)
        if hasattr(self.controller, 'start'):
            self.controller.start()

        # Temporizador para actualización
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.updateCameraView)
        self._timer.start(33)  # ~30 fps

    def updateScaledPixmap(self):
        if self.current_pixmap is not None and self.cameraView is not None:
            scaled_pixmap = self.current_pixmap.scaled(
                self.cameraView.size(),
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
            self.cameraView.setPixmap(scaled_pixmap)

    # -------------------------------------------------------------------------
    # Slots de los sliders/spinBoxes -> llaman a métodos de controller (backend)
    # -------------------------------------------------------------------------
    def onZoomSliderChanged(self):
        zoom = self.zoomSlider.value()
        if zoom != self.zoomSpinBox.value():
            self.controller.set_zoom(zoom)
            self.zoomSpinBox.setValue(zoom)

    def onZoomSpinBoxChanged(self):
        zoom = self.zoomSpinBox.value()
        if zoom != self.zoomSlider.value():
            self.controller.set_zoom(zoom)
            self.zoomSlider.setValue(zoom)

    def onFocusSliderChanged(self):
        focus = self.focusSlider.value()
        if focus != self.focusSpinBox.value():
            self.controller.set_focus(focus)
            self.focusSpinBox.setValue(focus)

    def onFocusSpinBoxChanged(self):
        focus = self.focusSpinBox.value()
        if focus != self.focusSlider.value():
            self.controller.set_focus(focus)
            self.focusSlider.setValue(focus)

    def onGainSliderChanged(self):
        gain = self.gainSlider.value()
        if gain != self.gainSpinBox.value():
            self.controller.set_gain(gain)
            self.gainSpinBox.setValue(gain)

    def onGainSpinBoxChanged(self):
        gain = self.gainSpinBox.value()
        if gain != self.gainSlider.value():
            self.controller.set_gain(gain)
            self.gainSlider.setValue(gain)

    def onExposureSliderChanged(self):
        exposure = self.exposureSlider.value()
        if exposure != self.exposureSpinBox.value():
            self.controller.set_exposure(exposure)
            self.exposureSpinBox.setValue(exposure)

    def onExposureSpinBoxChanged(self):
        exposure = self.exposureSpinBox.value()
        if exposure != self.exposureSlider.value():
            self.controller.set_exposure(exposure)
            self.exposureSlider.setValue(exposure)

    def onfpsSliderChanged(self):
        fps = self.fpsSlider.value()
        if fps != self.fpsSpinBox.value():
            self.controller.set_FPS(fps)
            self.fpsSpinBox.setValue(fps)

    def onfpsSpinBoxChanged(self):
        fps = self.fpsSpinBox.value()
        if fps != self.fpsSlider.value():
            self.controller.set_FPS(fps)
            self.fpsSlider.setValue(fps)

    def onBrightnessSliderChanged(self):
        brightness = self.brightnessSlider.value()
        if brightness != self.brightnessSpinBox.value():
            self.controller.set_brightness(brightness)
            self.brightnessSpinBox.setValue(brightness)

    def onBrightnessSpinBoxChanged(self):
        brightness = self.brightnessSpinBox.value()
        if brightness != self.brightnessSlider.value():
            self.controller.set_brightness(brightness)
            self.brightnessSlider.setValue(brightness)

    def onShutterSliderChanged(self):
        shutter = self.shutterSlider.value()
        if shutter != self.shutterSpinBox.value():
            self.controller.set_shutter(shutter)
            self.shutterSpinBox.setValue(shutter)

    def onShutterSpinBoxChanged(self):
        shutter = self.shutterSpinBox.value()
        if shutter != self.shutterSlider.value():
            self.controller.set_shutter(shutter)
            self.shutterSlider.setValue(shutter)

    def onIrisSliderChanged(self):
        iris = self.irisSlider.value()
        if iris != self.irisSpinBox.value():
            self.controller.set_iris(iris)
            self.irisSpinBox.setValue(iris)

    def onIrisSpinBoxChanged(self):
        iris = self.irisSpinBox.value()
        if iris != self.irisSlider.value():
            self.controller.set_iris(iris)
            self.irisSlider.setValue(iris)

    def onTemperatureSliderChanged(self):
        temperature = self.temperatureSlider.value()
        if temperature != self.temperatureSpinBox.value():
            self.controller.set_temperature(temperature)
            self.temperatureSpinBox.setValue(temperature)

    def onTemperatureSpinBoxChanged(self):
        temperature = self.temperatureSpinBox.value()
        if temperature != self.temperatureSlider.value():
            self.controller.set_temperature(temperature)
            self.temperatureSlider.setValue(temperature)

    def onWhiteShadingSliderChanged(self):
        white_shading = self.whiteShadingSlider.value()
        if white_shading != self.whiteShadingSpinBox.value():
            self.controller.set_white_shading(white_shading)
            self.whiteShadingSpinBox.setValue(white_shading)

    def onWhiteShadingSpinBoxChanged(self):
        white_shading = self.whiteShadingSpinBox.value()
        if white_shading != self.whiteShadingSlider.value():
            self.controller.set_white_shading(white_shading)
            self.whiteShadingSlider.setValue(white_shading)

    def onCaptureSizeSliderChanged(self):
        capture_size = self.captureSizeSlider.value()
        if capture_size != self.captureSizeSpinBox.value():
            self.controller.set_capture_size(capture_size)
            self.captureSizeSpinBox.setValue(capture_size)

    def onCaptureSizeSpinBoxChanged(self):
        capture_size = self.captureSizeSpinBox.value()
        if capture_size != self.captureSizeSlider.value():
            self.controller.set_capture_size(capture_size)
            self.captureSizeSlider.setValue(capture_size)

    def onCaptureQualitySliderChanged(self):
        capture_quality = self.captureQualitySlider.value()
        if capture_quality != self.captureQualitySpinBox.value():
            self.controller.set_capture_quality(capture_quality)
            self.captureQualitySpinBox.setValue(capture_quality)

    def onCaptureQualitySpinBoxChanged(self):
        capture_quality = self.captureQualitySpinBox.value()
        if capture_quality != self.captureQualitySlider.value():
            self.controller.set_capture_quality(capture_quality)
            self.captureQualitySlider.setValue(capture_quality)

    def onMirrorSliderChanged(self):
        mirror = self.mirrorSlider.value()
        if mirror != self.mirrorSpinBox.value():
            self.controller.set_mirror(mirror)
            self.mirrorSpinBox.setValue(mirror)

    def onMirrorSpinBoxChanged(self):
        mirror = self.mirrorSpinBox.value()
        if mirror != self.mirrorSlider.value():
            self.controller.set_mirror(mirror)
            self.mirrorSlider.setValue(mirror)

    def onSharpnessSliderChanged(self):
        sharpness = self.sharpnessSlider.value()
        if sharpness != self.sharpnessSpinBox.value():
            self.controller.set_sharpness(sharpness)
            self.sharpnessSpinBox.setValue(sharpness)

    def onSharpnessSpinBoxChanged(self):
        sharpness = self.sharpnessSpinBox.value()
        if sharpness != self.sharpnessSlider.value():
            self.controller.set_sharpness(sharpness)
            self.sharpnessSlider.setValue(sharpness)

    def onWhiteBalanceSliderChanged(self):
        white_balance = self.whiteBalanceSlider.value()
        if white_balance != self.whiteBalanceSpinBox.value():
            self.controller.set_white_balance(white_balance)
            self.whiteBalanceSpinBox.setValue(white_balance)

    def onWhiteBalanceSpinBoxChanged(self):
        white_balance = self.whiteBalanceSpinBox.value()
        if white_balance != self.whiteBalanceSlider.value():
            self.controller.set_white_balance(white_balance)
            self.whiteBalanceSlider.setValue(white_balance)

    def onHueSliderChanged(self):
        hue = self.hueSlider.value()
        if hue != self.hueSpinBox.value():
            self.controller.set_hue(hue)
            self.hueSpinBox.setValue(hue)

    def onHueSpinBoxChanged(self):
        hue = self.hueSpinBox.value()
        if hue != self.hueSlider.value():
            self.controller.set_hue(hue)
            self.hueSlider.setValue(hue)

    def onSaturationSliderChanged(self):
        saturation = self.saturationSlider.value()
        if saturation != self.saturationSpinBox.value():
            self.controller.set_saturation(saturation)
            self.saturationSpinBox.setValue(saturation)

    def onSaturationSpinBoxChanged(self):
        saturation = self.saturationSpinBox.value()
        if saturation != self.saturationSlider.value():
            self.controller.set_saturation(saturation)
            self.saturationSlider.setValue(saturation)

    def onGammaSliderChanged(self):
        gamma = self.gammaSlider.value()
        if gamma != self.gammaSpinBox.value():
            self.controller.set_gamma(gamma)
            self.gammaSpinBox.setValue(gamma)

    def onGammaSpinBoxChanged(self):
        gamma = self.gammaSpinBox.value()
        if gamma != self.gammaSlider.value():
            self.controller.set_gamma(gamma)
            self.gammaSlider.setValue(gamma)

    def onTriggerSliderChanged(self):
        trigger = self.triggerSlider.value()
        if trigger != self.triggerSpinBox.value():
            self.controller.set_trigger(trigger)
            self.triggerSpinBox.setValue(trigger)

    def onTriggerSpinBoxChanged(self):
        trigger = self.triggerSpinBox.value()
        if trigger != self.triggerSlider.value():
            self.controller.set_trigger(trigger)
            self.triggerSlider.setValue(trigger)

    def onTriggerDelaySliderChanged(self):
        trigger_delay = self.triggerDelaySlider.value()
        if trigger_delay != self.triggerDelaySpinBox.value():
            self.controller.set_trigger_delay(trigger_delay)
            self.triggerDelaySpinBox.setValue(trigger_delay)

    def onTriggerDelaySpinBoxChanged(self):
        trigger_delay = self.triggerDelaySpinBox.value()
        if trigger_delay != self.triggerDelaySlider.value():
            self.controller.set_trigger_delay(trigger_delay)
            self.triggerDelaySlider.setValue(trigger_delay)

    def onPanSliderChanged(self):
        pan = self.panSlider.value()
        if pan != self.panSpinBox.value():
            self.controller.set_pan(pan)
            self.panSpinBox.setValue(pan)

    def onPanSpinBoxChanged(self):
        pan = self.panSpinBox.value()
        if pan != self.panSlider.value():
            self.controller.set_pan(pan)
            self.panSlider.setValue(pan)

    def onTiltSliderChanged(self):
        tilt = self.tiltSlider.value()
        if tilt != self.tiltSpinBox.value():
            self.controller.set_tilt(tilt)
            self.tiltSpinBox.setValue(tilt)

    def onTiltSpinBoxChanged(self):
        tilt = self.tiltSpinBox.value()
        if tilt != self.tiltSlider.value():
            self.controller.set_tilt(tilt)
            self.tiltSlider.setValue(tilt)

    def onOpticalFilterSliderChanged(self):
        optical_filter = self.opticalFilterSlider.value()
        if optical_filter != self.opticalFilterSpinBox.value():
            self.controller.set_optical_filter(optical_filter)
            self.opticalFilterSpinBox.setValue(optical_filter)

    def onOpticalFilterSpinBoxChanged(self):
        optical_filter = self.opticalFilterSpinBox.value()
        if optical_filter != self.opticalFilterSlider.value():
            self.controller.set_optical_filter(optical_filter)
            self.opticalFilterSlider.setValue(optical_filter)
