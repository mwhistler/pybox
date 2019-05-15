import enum
import struct

import net0_parser


class TBChannelID:
    def __init__(self, byts: bytearray):
        self.board_id = struct.unpack("<H", byts[:2])[0]
        self.channel = struct.unpack("<H", byts[2:])[0]


class TBReadout:
    def __init__(self, read: bytearray):
        self.channel = TBChannelID(read[:4])
        self.timestamp = struct.unpack("<I", read[4:8])[0]
        self.value = struct.unpack("<i", read[8:12])[0]
        if len(read) > 12:
            unit = struct.unpack("<i", read[12:16])[0]
            self.value *= 10**((unit - 4) * 3)


def unpack_measure_from_rsp(rsp: net0_parser.NET0CommandResult):
    if rsp.status == SC.SUCCESS:
        return TBReadout(rsp.data)
    pass


TBErrorCodes = {
    0x00: 'SUCCESS',
    0x01: 'IN_PROGRESS',
    0xF1: 'OUT_OF_RANGE',
    0xF2: 'TIMEOUT',
    0xF3: 'CHANNEL_NOT_IMPLEMENTED',
    0xF8: 'INVALID_DATA',
    0xF9: 'COMMAND_NOT_IMPLEMENTED',
    0xFF: 'ERROR'
}


class SC(enum.Enum):
    SUCCESS = 0x00
    IN_PROGRESS = 0x01
    OUT_OF_RANGE = 0xF1
    TIMEOUT = 0xF2
    CHANNEL_NOT_IMPLEMENTED = 0xF3
    INVALID_DATA = 0xF8
    COMMAND_NOT_IMPLEMENTED = 0xF9
    ERROR = 0xFF


TBCommands = {
    'CMD_READ_REGISTER': 0x01,
    'CMD_WRITE_REGISTER': 0x02,
    'CMD_CLEAR_REGISTER': 0x03,
    'CMD_DEVICE_CONTROL': 0x08,
    'CMD_GET_CHANNEL': 0x09,
    'CMD_SET_CHANNEL': 0x0A,
    'CMD_CHANNEL_CONFIG': 0x0B,
    'CMD_ENTER_BOOTLOAD':  0x3F,
}
TBRegisters = {
    'REG_SOFTWARE_VERSION': {'code': 0x01, 'size': 4},
    'REG_HARDWARE_VERSION': {'code': 0x02, 'size': 4},
    'REG_MANUFACTURER_CODE': {'code': 0x04, 'size': 2},
    'REG_DEVICE_TYPE': {'code': 0x05, 'size': 1},
    'REG_CALIBRATION_WARNING_TIMESTAMP': {'code': 0x06, 'size': 4},
    'REG_CALIBRATION_REQUIRED_TIMESTAMP': {'code': 0x07, 'size': 4},
    'REG_INSTALLED_MODULES': {'code': 0x08, 'size': 4},
    'REG_DEVICE_STATUS_FLAGS': {'code': 0x09, 'size': 4},
    'REG_TOOLSET_ID': {'code': 0x10, 'size': 4},
    'REG_TOOLS': {'code': 0x11, 'size': 128},
}

TBControl = {
    'DEV_CTRL_USBUSART_BRIDGE': {'code': 0x01, 'size': 1},
    'DEV_CTRL_AMMETER_OFFSET_NULL': {'code': 0x02, 'size': 4},
}
