import dut
import elf_module_common
import struct


#tbox = testbox.TestBox("COM46", 115200, True)

elfModule = dut.Dut("COM49", True)

#fx = TestBoxFixture(tbox)


# set test mode in DUT:
# power off
#TODO power off
#fx.delay(1)

# power on
#TODO power on

print("Poczatek czytania portu DUT")
#elfModule.get_result()

response = elfModule.send_test_command(elf_module_common.ModuleCommands['CMD_RTCSTAT_SEND'], [0x00, 0x00])

if isinstance(response, (list,)):
    print("Odebrano odpowedz z DUT'a")
    if response[0] == 0 and response[1] == 1:
        print("Zegar RTC dziala prawidlowo")
        exit(1)
    else:
        print("Zegar RTC nie dziala prawidlowo")
else:
    print("Status RTC nie zostal odczytany!")

