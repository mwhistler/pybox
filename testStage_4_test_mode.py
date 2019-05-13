import dut
import elf_module_common


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

if elfModule.set_config():
    print("DUT jest w trybie testowym")
    response = elfModule.send_test_command(elf_module_common.ModuleCommands['CMD_START'], [0x00, 0x00])
    if isinstance(response, (bytes,)):
        print("Odebrano odpowedz z DUT'a")
        response_ok = 0
        if elf_module_common.get_test_mode_stat(response) == response_ok:
            print("Urzadzenie gotowe do testow")
            exit(1)
        print("odpowiedz =", str(response))
        exit(-1)
    else:
        print("Nie odebrano prawidlowej odpowiedzi")
else:
    print("nie odebrano rozkazu konfiguracji z DUT'a")
    exit(-2)

