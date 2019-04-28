import testbox
import testbox_common
import testbox_onboard
from testbox_common import SC
import time
import enum

# this class wraps around TestBox low level functions to provide user friendly interface


class TestBoxFixture:
    def __init__(self, tb: testbox.TestBox):
        self.tb = tb
        self.print_channel_operations_info = True
        self.print_info = True
        self.read_registers()
        # self.print_registers()

    def read_registers(self):
        for register in testbox_common.TBRegisters.keys():
            self.tb.cmd_read_register(register)

    def print_registers(self):
        for register, value in self.tb.registers.items():
            print(register + ": " + str(bytearray(value).hex()))

    def delay(self, seconds):
        if self.print_info:
            print("delay for " + str(seconds) + "s")
        time.sleep(seconds)

    def channel_config(self, channel: testbox_onboard.TBOnBoardChannels.keys, config: list, board_id=0):
        """

        :rtype: Net0Response
        """
        if self.print_channel_operations_info:
            print("channel_config: B" + str(board_id) + "." + channel + ": " + str(config))
        rsp = self.tb.cmd_channel_config(channel, config, board_id)
        if SC(rsp.status) != SC.SUCCESS:
            if self.print_channel_operations_info:
                print("channel_config: error 0x" + str(bytearray([rsp.status]).hex()) + " " +
                      testbox_common.TBErrorCodes[rsp.status])
        return rsp

    def get_channel(self, channel, board_id=0):

        rsp = self.tb.cmd_get_channel(channel, board_id)

        if SC(rsp.status) == SC.SUCCESS:
            readout = testbox_common.TBReadout(rsp.data)
            if self.print_channel_operations_info:
                print("get_channel: B" + str(board_id) + "." + channel + ": " + str(readout.value))
            return readout
        else:
            if self.print_channel_operations_info:
                print("get_channel: B" + str(board_id) + "." + channel + ": error 0x" +
                      str(bytearray([rsp.status]).hex()) + " " + testbox_common.TBErrorCodes[rsp.status])
        return None

    def set_channel(self, channel, value, board_id=0):

        rsp = self.tb.cmd_set_channel(channel, value, board_id)

        if self.print_channel_operations_info:
            if SC(rsp.status) == SC.SUCCESS:
                print("set_channel: B" + str(board_id) + "." + channel + ": " + str(value) + " OK")
            else:
                print("set_channel: B" + str(board_id) + "." + channel + ": " + "error 0x" +
                      str(bytearray([rsp.status]).hex()) + " " +
                      testbox_common.TBErrorCodes[rsp.status])

        return rsp

