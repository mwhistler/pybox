import serial
import threading


class Net0SerialPhy:
    serial_port = serial.Serial()
    receiver_thread = threading.Thread
    frames_received = []
    stop_receiver_thread = 0

    def __init__(self, serial_port_name):
        self.open(serial_port_name)
        self.receiver_thread = threading.Thread(target=self.receiver)
        self.stop_receiver_thread = 0
        self.receiver_thread.start()

    # TODO: improve closing thread
    def close(self):
        self.stop_receiver_thread = 1
        while self.receiver_thread.isAlive():
            pass
        self.serial_port.close()
        print("Net0SerialPhy closed")

    def receiver(self):
        while self.stop_receiver_thread == 0 and self.serial_port.is_open:
            data = bytearray()
            while self.stop_receiver_thread == 0 and self.serial_port.read() != bytes([0x02]):
                pass
            data.append(0x02)
            while data[-1] != 0x03:
                data.append(self.serial_port.read()[0])  # data.append(struct.unpack(">B", self.serial_port.read())[0])
            print("data recv: " + str(data.hex()))
            self.frames_received.append(data)
            # print("RECEIVED FRAMES QUEUE SIZE: " + str(frames_received.__len__()))
            # return data

    def receive(self):
        if self.frames_received.__len__() > 0:
            received_frame = bytearray(self.frames_received[0])
            self.frames_received.__delitem__(0)
            return received_frame
        return None

    def send(self, data: bytearray):
        if not isinstance(data, bytearray):
            raise TypeError('expected %s or bytearray, got %s' % (bytearray, type(data)))
        self.serial_port.write(data)
        print("data sent: " + str(data.hex()))

    def open(self, serial_port_name):
        self.serial_port.baudrate = 115200
        self.serial_port.port = serial_port_name
        self.serial_port.dsrdtr = False
        self.serial_port.xonxoff = False
        self.serial_port.rtscts = False
        self.serial_port.dtr = False
        self.serial_port.timeout = 10
        self.serial_port.inter_byte_timeout = 0
        self.serial_port.open()
        return True
