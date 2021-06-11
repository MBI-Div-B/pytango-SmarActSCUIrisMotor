#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import tango
from tango import AttrWriteType, DevState, DispLevel, DevFloat
from tango.server import Device, attribute, command, device_property
import serial


class SmaractSCUIrisMotor(Device):

    DeviceCtrl = device_property(dtype="str")
    Axis = device_property(dtype="int")

    position = attribute(
        name='position',
        label='Position',
        dtype="int",
        access=AttrWriteType.READ_WRITE,
        memorized=True)

    def init_device(self):
        # connect to camera
        Device.init_device(self)
        self.set_state(DevState.INIT)

        self.__position = 0

        try:
            self.ctrl = tango.DeviceProxy(self.DeviceCtrl)
            self.set_state(DevState.ON)
        except:
            self.error_stream('Could not connect to smaract tango controller')
            self.set_state(DevState.OFF)


    def read_position(self):
        return self.__position

    def write_position(self, value):
        diff = value - self.__position
        if diff < 0: # close
            self.ctrl.write(':D{:d}S{:d}'.format(self.Axis, abs(diff)))
        else: # open
            self.ctrl.write(':U{:d}S{:d}'.format(self.Axis, abs(diff)))

        self.__position = value

    def send_command(self, cmd):
        self.ctrl.write(cmd + '\n'.encode('utf8'))


if __name__ == "__main__":
    SmaractSCUIrisMotor.run_server()

