#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import tango
from tango import AttrWriteType, DevState, DispLevel, DevFloat
from tango.server import Device, attribute, command, device_property
import serial


class SmaractSCUIrisMotor(Device):

    speed = attribute(name='speed', label='Speed', dtype="int", access=AttrWriteType.READ_WRITE)

    deviceCtrl = device_property(dtype="str")
    axis = device_property(dtype="int")

    def init_device(self):
        # connect to camera
        Device.init_device(self)
        self.set_state(DevState.INIT)

        self._speed = 0

        try:
            self.ctrl = tango.DeviceProxy(self.deviceCtrl)
        except:
            self.error_stream('Could not connect to smaract tango controller')
            self.set_state(DevState.OFF)

    def read_speed(self):
        return self._speed

    def write_speed(self, value):
        self._speed = value

    @command
    def open_iris(self):
        self.ctrl.write(':U%dS%d\n'.encode()%(self.axis,self._speed))

    @command
    def close_iris(self):
        self.ctrl.write(':D%dS%d\n'.encode()%(self.axis,self._speed))


if __name__ == "__main__":
    SmaractSCUIrisMotor.run_server()

