import serial
import threading
import time


class Net0SerialPhy:
    def __init__(self, serial_port_name):
        self.serial_port = serial.Serial()
        self.receiver_thread = threading.Thread
        self.stop_receiver_thread = False
        self.received_data = bytearray()
        self.frames_received = []
        self.open(serial_port_name)

    def close(self):
        self.stop_receiver_thread = True
        while self.receiver_thread.isAlive():
            time.sleep(0.01)
            pass
        self.serial_port.close()
        print("Net0SerialPhy closed")

    def receiver(self):
        while self.stop_receiver_thread is False:
            try:
                if self.serial_port.inWaiting():
                    self.received_data += self.serial_port.read(self.serial_port.inWaiting())

                try:
                    if self.received_data[0] != 0x02:
                        self.received_data[:self.received_data.index(0x02)] = []
                    etx_index = self.received_data.index(0x03)
                except (ValueError, IndexError):
                    time.sleep(0.01)
                    continue

                print("data recv: " + str(bytearray(self.received_data[:etx_index + 1]).hex()))
                self.frames_received.append(bytearray(self.received_data[:etx_index + 1]))
                self.received_data = self.received_data[etx_index:]

            except serial.SerialException:
                self.close()

    def receive(self):
        try:
            return bytearray(self.frames_received.pop(0))
        except IndexError:
            return None

    def send(self, data: bytearray):
        if type(data) is not bytearray:
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
