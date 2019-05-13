import enum
import struct


class CommandStat(enum.Enum):
    SUCCESS = 0x00
    IN_PROGRESS = 0x01
    OUT_OF_RANGE = 0xF1
    TIMEOUT = 0xF2
    INVALID_DATA = 0xF8
    COMMAND_NOT_IMPLEMENTED = 0xFD
    ERROR = 0xFF


ModuleCommands = {
    'CMD_START': 0x01,
    'CMD_LOW_POWER': 0x02,
    'CMD_POWER': 0x03,
    'CMD_PROVIDE_RTC_SIGNAL': 0x04,
    'CMD_RADIO_TX': 0x05,
    'CMD_DISABLE_TEST_MODE': 0x06,
    'CMD_WRITE_RTC_CALIB': 0x07,
    'CMD_WRITE_PID': 0x08,
    'CMD_50MHZ': 0x09,
    'CMD_WRITE_50MHZ_CALIB': 0x0A,
    'CMD_READ_CONF': 0x0B,
    'CMD_UART_SEND': 0x0C,
    'CMD_RESERVED': 0x0D,
    'CMD_RTCSTAT_SEND': 0x0E,
    'CMD_STOP': 0x0F,
    'CMD_WRITE_ID': 0x10,
    'CMD_READ_ID': 0x11,
    'CMD_ERASE_ID': 0x12,
    'ANS_UNEXPECTED': 0xff,
}


def get_rtc_stat(data_buf: bytes):
    stat = struct.unpack_from('>H', data_buf, 0)
    return stat[0]


def get_test_mode_stat(data_buf: bytes):
    return get_rtc_stat(data_buf)
