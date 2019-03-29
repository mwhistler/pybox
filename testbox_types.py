import enum
import struct


def prepare_channel_config_struct(channel, config: list):
    if channel not in TBChannels.keys():
        print("Wrong channel: " + channel)
        return None

    cdata = struct.pack("<H", 0) + struct.pack("<H", TBChannels[channel])

    cfg_struct = None

    if channel in TBRelayChannels:
        cfg_struct = TBRelayOutConfigStruct(config).bytes()
    elif channel in TBPowerOutChannels:
        cfg_struct = TBPowerOutConfigStruct(config).bytes()
    else:
        return None

    return cdata + cfg_struct


TBChannels = {
    'PWR0': 0x0001,
    'PWR1': 0x0002,
    'VOUT0': 0x0010,
    'VOUT1': 0x0011,
    'OD0': 0x0040,
    'OD1': 0x0041,
    'PWM0': 0x0050,
    'PWM1': 0x0051,
    'PWM2': 0x0052,
    'REL0': 0x0060,
    'REL1': 0x0061,
    'REL2': 0x0062,
    'REL3': 0x0063,
    'AMP0': 0x0070,
    'AMP1': 0x0070,
    'VIN0': 0x0080,
    'VIN1': 0x0081,
    'VIN2': 0x0082,
    'VIN3': 0x0083,
    'VIN4': 0x008F,
    'IO0': 0x0090,
    'IO1': 0x0091,
    'IO2': 0x0092,
    'IO3': 0x0093,
    'IO4': 0x0094,
    'T0': 0x00A0,
    'T1': 0x00A1,
    'T2': 0x00A2,
}

TBPowerSupplyChannels = {
    'PWR0': 0x0001,
    'PWR1': 0x0002,
}

TBVoltageOutChannels = {
    'VOUT0': 0x0010,
    'VOUT1': 0x0011,
}

TBPowerOutChannels = {
    'OD0': 0x0040,
    'OD1': 0x0041,
    'PWM0': 0x0050,
    'PWM1': 0x0051,
    'PWM2': 0x0052,
}

TBRelayChannels = {
    'REL0': 0x0060,
    'REL1': 0x0061,
    'REL2': 0x0062,
    'REL3': 0x0063,
}

TBAmmeterChannels = {
    'AMP0': 0x0070,
    'AMP1': 0x0070,
}

TBVoltmeterChannels = {
   'VIN0': 0x0080,
    'VIN1': 0x0081,
    'VIN2': 0x0082,
    'VIN3': 0x0083,
    'VIN4': 0x008F,
}

TBDigitalIOChannels = {
    'IO0': 0x0090,
    'IO1': 0x0091,
    'IO2': 0x0092,
    'IO3': 0x0093,
    'IO4': 0x0094,
}

TBTemperatureChannels = {
    'T0': 0x00A0,
    'T1': 0x00A1,
    'T2': 0x00A2,
}

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

# ========== RELAY OUTPUTS

TBOutOperatingMode = {
    'STATIC': 0,
    'PULSE': 1,
    'PWM': 2
}

TBOutIdleState = {
    'N_OPEN': 0,
    'N_CLOSE': 1,
    'N_OFF': 0,
    'N_ON': 1
}


class TBRelayOutConfigStruct:
    operating_mode = TBOutOperatingMode
    idle_state = TBOutIdleState
    pulse_width = 0
    pulse_period = 0

    # TODO: add parameters assets
    def __init__(self, config: list):
        self.operating_mode = TBOutOperatingMode[config[0]]
        self.idle_state = TBOutIdleState[config[1]]
        self.pulse_width = config[2]
        self.pulse_period = config[3]

    def bytes(self):
        out = bytearray()
        out += struct.pack("<H", self.operating_mode)
        out += struct.pack("<H", self.idle_state)
        out += struct.pack("<H", self.pulse_width)
        out += struct.pack("<H", self.pulse_period)
        return out

class TBPowerOutConfigStruct:
    operating_mode = TBOutOperatingMode
    idle_state = TBOutIdleState
    pulse_width = 0
    pulse_period = 0
    pwm_frequency = 0

    # TODO: add parameters assets
    def __init__(self, config: list):
        self.operating_mode = TBOutOperatingMode[config[0]]
        self.idle_state = TBOutIdleState[config[1]]
        self.pulse_width = config[2]
        self.pulse_period = config[3]
        self.pwm_frequency = config[4]

    def bytes(self):
        out = bytearray()
        out += struct.pack("<H", self.operating_mode)
        out += struct.pack("<H", self.idle_state)
        out += struct.pack("<H", self.pulse_width)
        out += struct.pack("<H", self.pulse_period)
        out += struct.pack("<I", self.pwm_frequency)
        return out
