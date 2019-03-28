import struct
from net0_serial_device import Net0SerialDevice
from net0_parser import NET0Command


testBoxCommands = {
    'CMD_READ_REGISTER': 0x01,
    'CMD_WRITE_REGISTER': 0x02,
    'CMD_CLEAR_REGISTER': 0x03,
    'CMD_DEVICE_CONTROL': 0x08,
    'CMD_GET_CHANNEL': 0x09,
    'CMD_SET_CHANNEL': 0x0A,
    'CMD_CHANNEL_CONFIG': 0x0B,
    'CMD_ENTER_BOOTLOAD': 0x3F
}

# values in arrays are [REG_CODE, _REG_LENGTH]
testBoxRegisters = {
    'REG_SOFTWARE_VERSION': [0x01, 4],
    'REG_HARDWARE_VERSION': [0x02, 4],
    'REG_MANUFACTURER_CODE': [0x04, 2],
    'REG_DEVICE_TYPE': [0x05, 1],
    'REG_CALIBRATION_WARNING_TIMESTAMP': [0x06, 4],
    'REG_CALIBRATION_REQUIRED_TIMESTAMP': [0x07, 4],
    'REG_INSTALLED_MODULES': [0x08, 4],
    'REG_DEVICE_STATUS_FLAGS': [0x09, 4],
    'REG_TOOLSET_ID': [0x10, 4],
    'REG_TOOLS': [0x11, 128],
}


class Testbox(Net0SerialDevice):
    registers = {}

    def __init__(self, serial_port_name):
        super(Testbox, self).__init__(serial_port_name)

    # USAGE: cmd_read_register('REG_SOFTWARE_VERSION') or like in read_registers() function
    def cmd_read_register(self, register: testBoxRegisters):
        rsp = self.exec_command(NET0Command(testBoxCommands['CMD_READ_REGISTER'], bytearray([testBoxRegisters[register][0]])))
        if rsp is not None and rsp.status == 0x00:
            if rsp.data[0] == bytearray(testBoxRegisters[register])[0] and rsp.data[1] == bytearray(testBoxRegisters[register])[1]:
                self.registers[register] = rsp.data[2:]
                return
        del self.registers[register]

    def read_registers(self):
        for register in testBoxRegisters.keys():
            self.cmd_read_register(register)

    def print_registers(self):
        for register, value in self.registers.items():
            print(register + ": " + str(bytearray(value).hex()))

    # cmd_write_register works only with binary content
    # TODO: create user friendly functions, for example: set_next_calibration_date(date) etc
    def cmd_write_register(self, register: testBoxRegisters, data: bytearray):
        if data.__len__() == bytearray(testBoxRegisters[register])[1]:
            cmd = bytearray(testBoxRegisters[register]) + data
            if cmd is not None:
                rsp = self.exec_command(NET0Command(testBoxCommands['CMD_WRITE_REGISTER'], cmd))
                if rsp.status == 0x00:
                    # write the same to local copy:
                    self.registers[register] = data
                    print(register + " written successfully with " + str(data.hex()))
                    return
        print(register + "write FAILED")

    def cmd_configure_channel(self):
        pass

    def cmd_set_channel(self):
        pass

    def cmd_get_channel(self):
        pass


class TestBoxMeasureResult:

    def __init__(self, datafield):
        pass
