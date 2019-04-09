import struct

# this file specifies channels and its config structs for TestBox onboard features.
# extension cards channels are specified in separate files.
#
# this implementation fills TestBox specification v. 19
# which is available at [confluence_link]


def prepare_channel_config_struct(channel, config: list):
    if channel not in TBOnBoardChannels.keys():
        print("prepare_channel_config_struct() unknown channel: " + channel)
        return None

    cdata = struct.pack("<H", 0) + struct.pack("<H", TBOnBoardChannels[channel])

    cfg_struct = None

    if channel in TBRelayChannels:
        cfg_struct = TBRelayOutConfigStruct(config).bytes()
    elif channel in TBPowerOutChannels:
        cfg_struct = TBPowerOutConfigStruct(config).bytes()
    elif channel in TBPowerSupplyChannels:
        cfg_struct = TBPowerSupplyConfigStruct(config).bytes()
    elif channel in TBAmmeterChannels:
        cfg_struct = TBAmmeterConfigStruct(config).bytes()
    elif channel in TBVoltimeterChannels:
        cfg_struct = TBVoltimeterConfigStruct(config).bytes()
    elif channel in TBAnalogInChannels:
        cfg_struct = TBAnalogInConfigStruct(config).bytes()
    elif channel in TBDigitalIOChannels:
        cfg_struct = TBDigitalIOConfigStruct(config).bytes()
    elif channel in TBTemperatureChannels:
        cfg_struct = []
    elif channel in TBVoltageOutChannels:
        cfg_struct = []
    else:
        print("prepare_channel_config_struct() unknown channel " + channel)
        return None

    return cdata + cfg_struct


TBOnBoardChannels = {
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

TBPWMChannels = {
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

TBVoltimeterChannels = {
    'VIN0': 0x0080,
    'VIN1': 0x0081,
    'VIN2': 0x0082,
    'VIN3': 0x0083,
}

TBAnalogInChannels = {
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

# ========== RELAY and POWER OUTPUTS ============

TBOutOperatingMode = {
    'STATIC': 0,
    'PULSE': 1,
    'PWM': 2
}

TBOutIdleState = {
    'N_OPEN': 0,
    'N_CLOSE': 1,
    'N_OFF': 0,
    'N_ON': 1,
    'N_NEGATIVE': 0,
    'N_POSITIVE': 1
}

# RELAY_OUT_CONFIG_STRUCT:
# U16: OUT_OPERATING_MODE: [STATIC=0, PULSE=1]
# U16: OUT_IDLE_STATE: [N_OPEN=0, N_CLOSE=1]
# U16: PULSE_WIDTH [1-10000][ms]
# U16: PULSE_PERIOD [1-10000][ms]


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


# POWER_OUT_CONFIG_STRUCT:
# U16: OUT_OPERATING_MODE: [STATIC=0, PULSE=1, PWM=2]
# U16: OUT_IDLE_STATE: [N_OFF=0, N_ON=1]
# U16: PULSE_WIDTH [1-10000][ms]
# U16: PULSE_PERIOD [1-10000][ms]
# U32: PWM_FREQUENCY [1000 -100000][Hz]


class TBPowerOutConfigStruct:
    operating_mode = TBOutOperatingMode
    idle_state = TBOutIdleState
    pulse_width = 1
    pulse_period = 1
    pwm_frequency = 10000

    # TODO: improve parameters assets
    # TODO: discriminate OD and PWM channels
    def __init__(self, config: list):
        if len(config) >= 2:
            self.operating_mode = TBOutOperatingMode[config[0]]
            self.idle_state = TBOutIdleState[config[1]]
            if len(config) > 2:
                if len(config) == 5:
                    self.pulse_width = config[2]
                    self.pulse_period = config[3]
                    self.pwm_frequency = config[4]
                else:
                    print("wrong parameters list, should be first two or all five")
        else:
            print("wrong parameters list, should be two or five")

    def bytes(self):
        out = bytearray()
        out += struct.pack("<H", self.operating_mode)
        out += struct.pack("<H", self.idle_state)
        out += struct.pack("<H", self.pulse_width)
        out += struct.pack("<H", self.pulse_period)
        out += struct.pack("<I", self.pwm_frequency)
        return out

# ============== POWER SUPPLIES ==================


TBOnOffState = {
    'OFF': 0,
    'ON': 1
}

TBPowerSupplyOffMethod = {
    'OFF_HIZ': 0,
    'OFF_SHORTCUT': 1
}

# POWER_SUPPLY_CONFIG_STRUCT:
# U16: OUTPUT_VOLTAGE [1500 – 10000][mV]
# U16: OFF_METHOD: [OFF_HIZ = 0, OFF_SHORTCUT = 1]


class TBPowerSupplyConfigStruct:
    output_voltage = 2600
    off_method = 0

    # TODO: add parameters assets
    def __init__(self, config: list):
        self.output_voltage = config[0]
        self.off_method = TBPowerSupplyOffMethod[config[1]]

    def bytes(self):
        out = bytearray()
        out += struct.pack("<H", self.output_voltage)
        out += struct.pack("<H", self.off_method)
        return out

# ============ AMMETERS =============


TBAmmeterRange = {
    'IR_HIGH': 0,
    'IR_LOW': 1
}

# AMMETER_CONFIG_STRUCT:
# U16: RANGE: [IR_HIGH=0, IR_LOW=1]
# U16: AVERAGING_TIME: 1, 2, 4, 8, 16, 32, 64, 128, 256, 512 [ms]


class TBAmmeterConfigStruct:
    range = 0
    averaging_time = 8

    # TODO: add parameters assets
    def __init__(self, config: list):
        self.range = TBAmmeterConfigStruct[config[0]]
        self.averaging_time = config[1]

    def bytes(self):
        out = bytearray()
        out += struct.pack("<H", self.range)
        out += struct.pack("<H", self.averaging_time)
        return out


# ========== VOLTIMETERS =============

# VOLTMETER_CONFIG_STRUCT:
# U32: AVERAGING_TIME: 1, 2, 4, 8, 16, 32, 64, 128, 256, 512 [ms]


class TBVoltimeterConfigStruct:
    averaging_time = 8

    def __init__(self, config: list):
        if len(config) == 1 and config[0] in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]:
            self.averaging_time = config[0]
        else:
            print("wrong parameters, defaults kept (averaging_time = 8)")
            # TODO: consider raising exceptions instead printing a message

    def bytes(self):
        out = bytearray()
        out += struct.pack("<I", self.averaging_time)
        return out

# ============ ANALOG IN ===============

# ANALOG_IN_CONFIG_STRUCT
# U32: PGA_GAIN: 1, 2, 4, 8 [x]


class TBAnalogInConfigStruct:
    pga_gain = 1

    # TODO: add parameters assets
    def __init__(self, config: list):
        if len(config) == 1 and config[0] in [1, 2, 4, 8]:
            self.pga_gain = config[0]
        else:
            print("wrong parameters, defaults kept (pga_gain = 1)")

    def bytes(self):
        out = bytearray()
        out += struct.pack("<I", self.pga_gain)
        return out

# =========== DIGITAL IO =================


TBIODirection = {
    'IO_DIR_OUTPUT': 0,
    'IO_DIR_INPUT': 1
}

TBInputSensitivity = {
    'FALLING': 0,
    'RISING': 1
}

TBPullUp = {
    'PUP_OFF': 0,
    'PUP_UP': 1,
    'PUP_DOWN': 2
}

TBInputOperatingMode = {
    'STATIC': 0,
    'PULSE_COUNTER': 1,
    'TIME_MEASURE': 2,
    'RTC_MEASURE': 3
}

TBTimeMeasureMode = {
    'PERIOD': 0,
    'PULSE': 1
}

# DIGITAL_IO_CONFIG_STRUCT:
# U16: IO_DIRECTION: [IO_DIR_OUTPUT=0, IO_DIR_INPUT=1]
# U16: OUT_OPERATING_MODE: [STATIC=0, PULSE=1]
# U8: OUT_IDLE_STATE: [N_NEGATIVE=0, N_POSITIVE=1]
# U8: INPUT_SENSIVITY: [FALLING=0, RISING=1]
# U16: PULSE_WIDTH [1-10000][ms]
# U16: PULSE_PERIOD [1-10000][ms]
# U16: PULL_UP: [PUP_OFF=0, PUP_UP=1, PUP_DOWN=2]
# U16: INPUT_OPERATING_MODE: [STATIC=0, PULSE_COUNTER=1, TIME_MEASURE=2, RTC_MEASURE=3]
# U16: TIME_MEASURE_MODE: [PERIOD=0, PULSE=1]
# U16: TIMEOUT [ms]
# U16: PROBES [1-100]

class TBDigitalIOConfigStruct:
    io_direcion = TBIODirection
    operating_mode = TBOutOperatingMode
    idle_state = TBOutIdleState
    input_sensitivity = TBInputSensitivity
    pulse_width = 0
    pulse_period = 0
    pull_up = TBPullUp
    input_operating_mode = TBInputOperatingMode
    time_measure_mode = TBTimeMeasureMode
    timeout = 0
    probes = 0

    # TODO: add parameters assets
    def __init__(self, config: list):
        self.io_direcion = TBIODirection[config[0]]
        self.operating_mode = TBOutOperatingMode[config[1]]
        self.idle_state = TBOutIdleState[config[2]]
        self.input_sensitivity = TBInputSensitivity[config[3]]
        self.pulse_width = config[4]
        self.pulse_period = config[5]
        self.pull_up = TBPullUp[config[6]]
        self.input_operating_mode = TBInputOperatingMode[config[7]]
        self.time_measure_mode = TBTimeMeasureMode[config[8]]
        self.timeout = config[9]
        self.probes = config[10]

    def bytes(self):
        out = bytearray()
        out += struct.pack("<H", self.io_direcion)
        out += struct.pack("<H", self.operating_mode)
        out += struct.pack("<B", self.idle_state)
        out += struct.pack("<B", self.input_sensitivity)
        out += struct.pack("<H", self.pulse_width)
        out += struct.pack("<H", self.pulse_period)
        out += struct.pack("<H", self.pull_up)
        out += struct.pack("<H", self.input_operating_mode)
        out += struct.pack("<H", self.time_measure_mode)
        out += struct.pack("<H", self.timeout)
        out += struct.pack("<H", self.probes)
        return out
