#!/usr/bin/env python3

"""
GrabberControls2Gui
---------------------

Simple GUI for controlling GigE cameras using Aravis and YARP

Author: David Estevez
Copyright: Universidad Carlos III de Madrid (C) 2017;
CopyPolicy: Released under the terms of the GNU GPL v2.0.
"""

import sys
import logging

import begin
import yarp
from PySide2 import QtWidgets

from .GrabberControls2GuiBackend import GrabberControls2GuiBackend
from .GrabberControls2GuiGUI import GrabberControls2GuiGUI


@begin.start(auto_convert=True)
@begin.logging
def main(remote_port: 'Remote port running the AravisGigE grabber'='/grabber'):
    # Check for YARP network
    yarp.Network.init()
    if not yarp.Network.checkNetwork():
        logging.error('Could not connect to YARP network. Please try running YARP server.')
        sys.exit(1)

    # Create and configure driver
    options = yarp.Property()
    options.put('device', 'frameGrabber_nwc_yarp')
    options.put('remote', remote_port)
    options.put('local', '/grabberControls2Gui')
    dd = yarp.PolyDriver(options)

    if not dd.isValid():
        logging.error("PolyDriver is not valid. Check if the remote port exists or is correct.")
        dd.close()
        yarp.Network.fini()
        sys.exit(1)

    # 3) Obtener interfaz de controles (zoom, focus, etc.). Puede ser None si no existe.
    controls = dd.viewIFrameGrabberControls()
    if controls is None:
        logging.warning("No IFrameGrabberControls interface found. Some features won't be available.")

    # 4) Abrir un puerto local para leer imágenes, igual que hace yarpview
    camera_port = yarp.Port()
    camera_port_name = "/viewer"
    camera_port.open(camera_port_name)

    # Conectar automáticamente al puerto remoto que emite imágenes.
    # NOTA: En tu caso, si `yarp connect /grabber /viewer` funciona,
    #       significa que `/grabber` es un puerto de tipo ImageOf<PixelRgb>.
    #       Así que conectamos /grabber --> /grabberControls2Gui/img:i
    yarp.Network.connect(remote_port, camera_port_name)

    # 5) Crear la app Qt
    app = QtWidgets.QApplication(sys.argv)

    # 6) Crear el backend (controles) y la GUI, pasándole el puerto de cámara
    backend = GrabberControls2GuiBackend(controls)
    gui = GrabberControls2GuiGUI(backend, camera_port)
    gui.show()

    # Run the app
    exit_code = app.exec_()

    dd.close()
    camera_port.close()
    yarp.Network.fini()
    sys.exit(exit_code)
"""
# test_minimal.py
import sys
import yarp
import begin
import ctypes
from PySide2.QtWidgets import QApplication, QLabel
from PySide2.QtCore import QTimer
from PySide2.QtGui import QImage, QPixmap


class TestWidget(QLabel):
    def __init__(self):
        super().__init__("Esperando frame...")
        # Abrir puerto para leer imagen
        self.port = yarp.Port()
        self.port.open("/test/img:i")
        yarp.Network.connect("/grabber","/test/img:i")

        # Frame buffer
        self.frame_rgb = yarp.ImageRgb()

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer)
        self.timer.start(33)

    def on_timer(self):
        ok = self.port.read(self.frame_rgb)
        if not ok:
            print("No se pudo leer del puerto.")
            return

        w = int(self.frame_rgb.width())
        h = int(self.frame_rgb.height())

        if w == 0 or h == 0:
            print("Dimensiones incorrectas:", w, h)
            return

        step = w * 3  # RGB888

        c_ptr = self.frame_rgb.getRawImage()
        if c_ptr is None:
            print("ERROR: No se pudo obtener el puntero de la imagen.")
            return

        try:
            # Conversión explícita para garantizar un entero válido
            c_ptr = int(c_ptr.__int__())
        except Exception as e:
            print("ERROR al convertir c_ptr:", e, type(c_ptr))
            return

        buffer_size = int(w * h * 3)

        try:
            # Definir claramente array_type antes de usar from_address
            array_type = (ctypes.c_ubyte * buffer_size)
            raw_buffer = array_type.from_address(c_ptr)
            data = bytearray(raw_buffer)

            qimg = QImage(data, w, h, step, QImage.Format_RGB888)
            pix = QPixmap.fromImage(qimg)
            self.setPixmap(pix)
        except Exception as e:
            print("Error al crear imagen Qt:", e)


@begin.start(auto_convert=True)
def main():
    yarp.Network.init()
    if not yarp.Network.checkNetwork():
        print("No hay servidor YARP.")
        sys.exit(1)

    # Lanza la GUI
    app = QApplication(sys.argv)
    w = TestWidget()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

"""