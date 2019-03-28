from net0_serial_phy import Net0SerialPhy
import net0_parser
import time


class Net0SerialDevice:
    phy = Net0SerialPhy

    def __init__(self, serial_port_name):
        self.phy = Net0SerialPhy(serial_port_name)

    # returns NET0CommandResult object:
    # TODO: improve timeout handling
    def get_result(self):
        now = time.clock()
        while time.clock() - now < 10:
            rcv = self.phy.receive()
            if rcv is not None:
                return net0_parser.extract_command_result_from_frame(rcv)
        return None

    # sends NET0Command object:
    def send_command(self, command: net0_parser.NET0Command):
        if not isinstance(command, net0_parser.NET0Command):
            raise TypeError('expected %s or bytearray, got %s' % (net0_parser.NET0Command, type(command)))
        self.phy.send(net0_parser.create_frame(command))

    # sends NET0Command object and returns NET0CommandResult object:
    def exec_command(self, command: net0_parser.NET0Command):
        self.send_command(command)
        return self.get_result()

    def close(self):
        self.phy.close()
