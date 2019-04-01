import serial
import threading


class Net0SerialPhy:
    serial_port = serial.Serial()
    receiver_thread = threading.Thread
    frames_received = []
    stop_receiver_thread = False

    def __init__(self, serial_port_name):
        self.open(serial_port_name)

    def close(self):
        self.stop_receiver_thread = True
        while self.receiver_thread.isAlive():
            pass
        self.serial_port.close()
        print("Net0SerialPhy closed")

    def receiver(self):
        while self.stop_receiver_thread is False and self.serial_port.is_open:
            data = bytearray()
            while self.stop_receiver_thread is False and self.serial_port.read() != bytes([0x02]):
                pass
            data.append(0x02)
            while data[-1] != 0x03:
                data.append(self.serial_port.read()[0])
            print("data recv: " + str(data.hex()))
            self.frames_received.append(data)
            # print("RECEIVED FRAMES QUEUE SIZE: " + str(frames_received.__len__()))
            # return data

    def receive(self):
        try:
            return bytearray(self.frames_received.pop(0))
        except IndexError:
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
        self.receiver_thread = threading.Thread(target=self.receiver)
        self.stop_receiver_thread = False
        self.receiver_thread.start()
        return True
