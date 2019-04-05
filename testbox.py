import struct
from net0_serial_device import Net0SerialDevice
from net0_parser import NET0Command
from testbox_types import TBChannels
from testbox_types import TBCommands
from testbox_types import TBRegisters
from testbox_types import TBErrorCodes
from testbox_types import SC
import testbox_types


class Testbox(Net0SerialDevice):

    def __init__(self, serial_port_name):
        self.registers = {}
        super(Testbox, self).__init__(serial_port_name)

    # USAGE: cmd_read_register('REG_SOFTWARE_VERSION') or like in read_registers() function
    def cmd_read_register(self, register: TBRegisters):
        rsp = self.exec_command(NET0Command(TBCommands['CMD_READ_REGISTER'], bytearray([TBRegisters[register]['code']])))
        if rsp is not None and SC(rsp.status) == SC.SUCCESS:
            if rsp.data[0] == TBRegisters[register]['code'] and rsp.data[1] == TBRegisters[register]['size']:
                self.registers[register] = rsp.data[2:]
                return
        del self.registers[register]

    def read_registers(self):
        for register in TBRegisters.keys():
            self.cmd_read_register(register)

    def print_registers(self):
        for register, value in self.registers.items():
            print(register + ": " + str(bytearray(value).hex()))

    # cmd_write_register works only with binary content
    # TODO: create user friendly functions, for example: set_next_calibration_date(date) etc
    def cmd_write_register(self, register: TBRegisters, data):
        data = bytearray(data)
        if data.__len__() == TBRegisters[register]['size']:
            cmd = bytearray([TBRegisters[register]['code'], TBRegisters[register]['size']]) + data
            if cmd is not None:
                rsp = self.exec_command(NET0Command(TBCommands['CMD_WRITE_REGISTER'], cmd))
                if SC(rsp.status) == SC.SUCCESS:
                    # write the same to local copy:
                    self.registers[register] = data
                    print(register + " written successfully with " + str(data.hex()))
                    return
                else:
                    print("cmd_write_register error 0x" + str(bytearray([rsp.status]).hex()) + " " + TBErrorCodes[
                        rsp.status])
        print(register + "write FAILED")

    def cmd_channel_config(self, channel: TBChannels.keys, config: list, board_id=0):
        cfg_struct = None

        if board_id == 0:
            cfg_struct = testbox_types.prepare_channel_config_struct(channel, config)
        else:  # board_id != 0 - call functions from modules
            pass

        if cfg_struct is not None:
            rsp = self.exec_command(NET0Command(TBCommands['CMD_CHANNEL_CONFIG'], cfg_struct))
            if SC(rsp.status) == SC.SUCCESS:
                return True
            else:
                print("cmd_channel_config error 0x" + str(bytearray([rsp.status]).hex()) + " " + TBErrorCodes[rsp.status])
        return False

    def cmd_set_channel(self, channel, value, board_id = 0):
        cdata = struct.pack("<H", board_id) + \
                struct.pack("<H", TBChannels[channel]) + \
                struct.pack("<I", value)
        rsp = self.exec_command(NET0Command(TBCommands['CMD_SET_CHANNEL'], cdata))
        if SC(rsp.status) == SC.SUCCESS or SC(rsp.status) == SC.IN_PROGRESS:
            return True
        else:
            print("cmd_set_channel error 0x" + str(bytearray([rsp.status]).hex()) + " " + TBErrorCodes[rsp.status])

    def cmd_get_channel(self, channel, board_id = 0):
        cdata = struct.pack("<H", board_id) + \
                struct.pack("<H", TBChannels[channel])
        rsp = self.exec_command(NET0Command(TBCommands['CMD_GET_CHANNEL'], cdata))
        if SC(rsp.status) == SC.SUCCESS:
            return testbox_types.TBReadout(rsp.data)
        elif SC(rsp.status) == SC.IN_PROGRESS:
            rsp = self.get_result()
            if SC(rsp.status) == SC.SUCCESS:
                return testbox_types.TBReadout(rsp.data)
        else:
            print("cmd_get_channel error 0x" + str(bytearray([rsp.status]).hex()) + " " + TBErrorCodes[rsp.status])
