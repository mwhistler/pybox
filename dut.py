import serial
import threading
import time
import net0_parser
import elf_module_common


class Dut:

    def __init__(self, serial_port_name, low_level_info=True):
        self.stop_receiver_thread = False
        self.received_data = bytearray()
        self.frames_received = []
        self.low_level_info = low_level_info
        #serial com setings
        self.serial_port = serial.Serial()
        self.serial_port.baudrate = 9600
        self.serial_port.parity = serial.PARITY_EVEN
        self.serial_port.port = serial_port_name
        #self.serial_port.dsrdtr = False
        #self.serial_port.xonxoff = False
        #self.serial_port.rtscts = False
       # self.serial_port.dtr = False
        self.serial_port.timeout = 10
        self.serial_port.inter_byte_timeout = 0
        self.serial_port.bytesize = 8
        #self.serial_port.rs485_mode = serial.
        self.serial_port.open()

        self.stop_receiver_thread = False
        #self.receiver_thread.start()

    def __del__(self):
        self.serial_port.close()

    def send_frame(self, frame):
        frame_net0 = net0_parser.create_frame_from_array(bytearray(frame))
        self.serial_port.write(bytearray(frame_net0))
        if self.low_level_info:
            print("wyslij do portu COM: " + str((bytearray(frame_net0).hex())))
        frame_net0.clear()
        counter = 0
        while True:
            time.sleep(0.1)
            frame_net0 = self.serial_port.read_all()
            if frame_net0:
                return net0_parser.unpack_net0_frame(frame_net0)
            if counter > 10:
                break
            counter += 1
        return None

    def send_test_command(self, command: elf_module_common.ModuleCommands, arg: bytearray):
        frame = []
        frame.append(command)
        frame.extend(list(arg))
        response = self.send_frame(bytearray(frame))
        if response:
            if response[0] == (0x80 | command):
                frame_data = list(response)
                frame_data.pop(0)               #wykasuj rozkaz z ramki
                return frame_data
            elif response[0] == elf_module_common.ModuleCommands['ANS_UNEXPECTED']:
                return elf_module_common.CommandStat.COMMAND_NOT_IMPLEMENTED
            else:
                return elf_module_common.CommandStat.ERROR
        return None

    def set_config(self):
        time_counter = 0
        while True:
            rcv = self.serial_port.read_all()
            command = [0x4d, 0x40, 0x09, 0xff, 0xff, 0xd0, 0xff, 0x16]
            if len(rcv) > 0 and self.low_level_info:
                print("odczyt z portu COM: " + str((bytearray(rcv).hex())))
            if command == list(rcv):
                print("Odebrano rzadanie konfiguracji")
                break
            time.sleep(1)
            time_counter += 1
            if time_counter > 10:
                print("Brak ramki konfiguracyjnej")
                return False

        config_frame = [0x4D, 0xBF, 0x09, 0x2B, 0xFF, 0xA2, 0xFF, 0xFF, 0xFF, 0xFF,
                        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
                        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
                        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
                        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
                        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
                        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
                        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0xFF, 0xFF, 0xFF,
                        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x6E,
                        0xAC, 0x16]

        self.serial_port.write(bytearray(config_frame))
        if self.low_level_info:
            print("wyslij do portu COM: " + str((bytearray(config_frame).hex())))

        time.sleep(0.2)
        self.serial_port.read_all()
        time.sleep(2)

        rcv = self.serial_port.read_all()
        if len(rcv) > 0:
            if self.low_level_info:
                print("odczyt z portu COM: " + str((bytearray(rcv).hex())))
            print("Nie udalo sie wejsc w tryb testowy")
            return False
        return True

