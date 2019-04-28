import struct
from testbox_onboard import TBDigitalIOConfigStruct

RFExtChannels = {
    'IO0': 0x0000,
    'IO1': 0x0001,
    'IO2': 0x0002,
    'IO3': 0x0003,
 }

RFExtDigitalIOChannels = {
    'IO0': 0x0000,
    'IO1': 0x0001,
    'IO2': 0x0002,
    'IO3': 0x0003,
}


def prepare_channel_config_struct(channel, config: list):
    if channel not in RFExtChannels.keys():
        print("prepare_channel_config_struct() unknown channel: " + channel)
        return None

    cdata = struct.pack("<H", 0) + struct.pack("<H", RFExtChannels[channel])

    cfg_struct = None

    if channel in RFExtDigitalIOChannels:
        cfg_struct = TBDigitalIOConfigStruct(config).bytes()
    else:
        print("prepare_channel_config_struct() unknown channel " + channel)
        return None

    return cdata + cfg_struct
