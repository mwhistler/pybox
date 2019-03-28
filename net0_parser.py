import struct


class NET0CommandResult:
    code = 0
    status = 0
    data = bytearray()

    def __init__(self, net0_frame_data_field):
        if net0_frame_data_field is not None:
            self.code = net0_frame_data_field[0] & 0x7F
            self.status = net0_frame_data_field[1]
            self.data = net0_frame_data_field[2:]


class NET0Command:
    code = 0
    data = bytearray()

    def __init__(self, code: bytes, data: bytearray):
        self.code = code
        self.data = data[:]


def extract_command_result_from_frame(frame: bytearray):
    if frame is not None:
        return NET0CommandResult(unpack_net0_frame(frame))
    return None


def create_frame(net0_command: NET0Command):
    frame = bytearray([net0_command.code]) + bytearray(net0_command.data)
    crc = crc16(frame)
    frame += bytearray([(crc & 0xFF00) >> 8, crc & 0x00FF])
    out_frame = bytearray([0x02])
    for b in frame:
        if b == 0x02 or b == 0x03 or b == 0x10:
            out_frame.append(0x10)
            b |= 0x80
        out_frame.append(b)
    out_frame.append(0x03)
    return out_frame


def crc16(buff: bytearray):
    result = 0xFFFF
    for bajt in buff:
        result ^= bajt
        result &= 0xFFFF
        for bit in range(8, 0, -1):
            if (result & 0x0001) != 0:
                result = result >> 1
                result = result ^ 0xA001
            else:
                result = result >> 1
            result &= 0xFFFF
    return result


def unpack_net0_frame(frame: bytearray):
    unpacked = bytearray()
    un_dle_next_byte = 0
    for b in frame:
        if b == 0x02 or b == 0x03:
            pass
        elif b == 0x10:
            un_dle_next_byte = 1
        else:
            if un_dle_next_byte == 0:
                unpacked.append(b)
            else:
                unpacked.append(b & 0x7F)
                un_dle_next_byte = 0
    # print(str(unpacked.hex()))
    if crc16(unpacked[:-2]) == struct.unpack(">H", unpacked[-2:])[0]:
        return unpacked[:-2]
    else:
        print("CRC ERROR!!!")
        return None
