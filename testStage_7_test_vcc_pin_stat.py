import dut
import elf_module_common
import testbox
from testbox_fixture import TestBoxFixture

import struct

tbox = testbox.TestBox("COM46", True)
fx = TestBoxFixture(tbox)

elfModule = dut.Dut("COM49", True)

fx.channel_config('IO0', ['IO_DIR_OUTPUT', 'STATIC', 'N_POSITIVE', 'FALLING', 10000, 10000, 'PUP_OFF', 'STATIC', 'PERIOD', 100, 100])
fx.set_channel('IO0', 1)
fx.delay(0.1)
print("Poczatek czytania portu DUT")
#TODO
response = elfModule.send_test_command(elf_module_common.ModuleCommands['TEST_CMD_READ_VCC_PIN'], [0x00, 0x00])
if isinstance(response, (bytes,)):
    print("Odebrano prawidlowa ramke z DUT'a")
    print("response = " + str(response))
    if elf_module_common.get_pin_stat(response) == 1:
        print("wykryto prawidlowo podlaczenie pinu Vcc (stan Elfa podlaczony)")
    else:
        print("nie wykryto prawidlowo podlaczenia pinu Vcc (brak podlaczenia Elfa)")
        exit(-1)
else:
    print("Status pinu Vcc nie zostal odczytany!")
    exit(-2)

fx.set_channel('IO0', 0)
response = elfModule.send_test_command(elf_module_common.ModuleCommands['TEST_CMD_READ_VCC_PIN'], [0x00, 0x00])
if isinstance(response, (bytes,)):
    print("Odebrano prawidlowa ramke z DUT'a")
    if elf_module_common.get_pin_stat(response) == 0:
        print("wykryto prawidlowo brak podlaczenia pinu Vcc (brak podlaczenia Elfa")
    else:
        print("wykryto nie prawidlowo stan podlaczenia pinu Vcc (wykryto podlaczenie Elfa)")
        exit(-1)
else:
    print("Status pinu Vcc nie zostal odczytany!")
    exit(-2)
