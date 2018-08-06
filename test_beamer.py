#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import uic, QtWidgets, QtCore
import serial


class BeamerTesting(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

        self.on_pressed = False
        self.off_pressed = False
        self.ser = serial.Serial('/dev/ttyUSB0')
        self.ser.baudrate = 19200
        self.ser.bytesize = 8
        self.ser.parity = 'N'
        self.ser.stopbits = 1
        #self.ser.timeout = 5

    def initUI(self):
        self.setGeometry(0, 0, 600, 200)
        self.on_btn = QtWidgets.QPushButton("ON")
        self.on_btn.clicked.connect(self.on_btn_clicked)
        self.off_btn = QtWidgets.QPushButton("OFF")
        self.off_btn.clicked.connect(self.off_btn_clicked)
        self.off_btn.setStyleSheet('background-color: red')
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.off_btn)
        self.layout.addWidget(self.on_btn)
        self.setLayout(self.layout)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.show()

    def on_btn_clicked(self):
        if self.on_pressed is False:
            print("clicked on btn")
            self.on_pressed = True
            self.off_btn.setStyleSheet('background-color: white')
            self.repaint()
            input_on = b'\xbe\xef\x10\x05\x00\xc6\xff\x11\x11\x01\x00\x01'
            self.ser.write(input_on)
            self.start_timer()

            #self.on_btn.setStyleSheet('background-color: white')
            #status = self.read_status()
            #if status

            self.off_btn.setEnabled(True)
            self.on_btn.setEnabled(True)
            self.on_btn.setStyleSheet('background-color: green')
            self.on_pressed = False

    def start_timer(self):
        self.timer = QtCore.QTime()
        self.timer.start()
        if self.on_pressed:
            while self.timer.elapsed() <= 15000:
                #self.off_btn.setEnabled(False)
                #self.on_btn.setEnabled(False)
                if int(self.timer.elapsed()/1000) % 2 == 0:
                    self.on_btn.setStyleSheet('background-color: green')
                else:
                    self.on_btn.setStyleSheet('background-color: white')
                self.timer.elapsed()
                self.repaint()
        if self.off_pressed:
            while self.timer.elapsed() <= 8000:
                #self.off_btn.setEnabled(False)
                #self.on_btn.setEnabled(False)
                if int(self.timer.elapsed() / 1000) % 2 == 0:
                    self.off_btn.setStyleSheet('background-color: red')
                else:
                    self.off_btn.setStyleSheet('background-color: white')
                self.repaint()

    def read_status(self):
        self.ser.write(b'\xbe\xef\x10\x05\x00\x46\x7e\x11\x11\x01\x00\xff')
        s = self.ser.read(size=3)
        print(s)
        s_hex = hex(int.from_bytes(s,byteorder='little'))
        print(s_hex[2])
        status = s_hex[2]
        return status

    def off_btn_clicked(self):
        if self.off_pressed is False:
            self.off_pressed = True
            print("clicked off btn")
            self.on_btn.setStyleSheet('background-color: white')
            self.repaint()
            input_off = b'\xbe\xef\x10\x05\x00\x0c\x3e\x11\x11\x01\x00\x18'
            self.ser.write(input_off)
            self.start_timer()
            self.off_btn.setEnabled(True)
            self.on_btn.setEnabled(True)
            self.off_btn.setStyleSheet('background-color: red')
            self.off_pressed = False


def main():
    app = QtWidgets.QApplication(sys.argv)
    beamer = BeamerTesting()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
