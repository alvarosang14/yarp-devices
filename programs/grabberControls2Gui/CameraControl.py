import yarp
import ctypes
from PySide2 import QtCore, QtGui, QtWidgets


class Camera(QtCore.QObject):
    def __init__(self, remote_port, parent_widget=None):
        super().__init__()
        self.cameraView = None
        self.current_pixmap = None
        self._timer = None
        self.parent_widget = parent_widget
        self.camera_port = None

        # Configuration
        self.setup_camera_port(remote_port)
        self.setup_camera_view()
        self.startCameraReading()

    def setup_camera_port(self, remote_port):
        """Configures the YARP port to receive images"""
        yarp.Network.init()  # Ensure YARP is initialized

        self.camera_port = yarp.BufferedPortImageRgb()
        local_port = "/viewer/image:i"

        if not self.camera_port.open(local_port):
            print(f"Error: Could not open port {local_port}")
            return False

        if not yarp.Network.connect(remote_port, local_port):
            print(f"Error: Could not connect {remote_port} to {local_port}")
            return False

        return True

    def setup_camera_view(self):
        """Sets up the display widget"""
        if self.parent_widget:
            self.cameraView = self.parent_widget.findChild(QtWidgets.QLabel, 'cameraView')

            self.cameraView.setText("Waiting for camera image...")
            self.cameraView.setAlignment(QtCore.Qt.AlignCenter)
            self.cameraView.setScaledContents(False)

    def updateCameraView(self):
        """Updates the view with a new frame"""
        yarp_img = self.camera_port.read(True)
        if yarp_img is None:
            print("Warning: No image available")
            return

        width, height = yarp_img.width(), yarp_img.height()
        if width <= 0 or height <= 0:
            return

        # Convert YARP image to QPixmap
        img_ptr = int(yarp_img.getRawImage())
        img_size = yarp_img.getRawImageSize()
        img_data = (ctypes.c_ubyte * img_size).from_address(img_ptr)

        qimage = QtGui.QImage(
            img_data,
            width,
            height,
            yarp_img.getRowSize(),
            QtGui.QImage.Format_RGB888
        )

        if not qimage.isNull():
            self.current_pixmap = QtGui.QPixmap.fromImage(qimage)
            self.updateScaledPixmap()

    def startCameraReading(self):
        """Starts the video stream"""
        if self._timer is not None:
            self._timer.stop()

        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.updateCameraView)
        self._timer.start(33)  # ~30 fps

    def updateScaledPixmap(self):
        """Scales the image to the widget size"""
        if self.current_pixmap and self.cameraView:
            scaled_pixmap = self.current_pixmap.scaled(
                self.cameraView.size(),
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
            self.cameraView.setPixmap(scaled_pixmap)

    def stop(self):
        """Stops image capture and releases resources"""
        if self._timer:
            self._timer.stop()
            self._timer = None

        if self.camera_port:
            yarp.Network.disconnect(self.camera_port.getName(),
                                    yarp.Network.getName(self.camera_port.getName()))
            self.camera_port.close()
            self.camera_port = None

    def resizeEvent(self, event):
        """Handles widget resizing"""
        self.updateScaledPixmap()
        event.accept()
