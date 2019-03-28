import struct
from net0_serial_device import Net0SerialDevice
# from net0_serial_phy import Net0SerialPhy


class Testbox(Net0SerialDevice):

    def __init__(self, serial_port_name):
        super(Testbox, self).__init__(serial_port_name)


class TestBoxMeasureResult:

    def __init__(self, datafield):
        pass
