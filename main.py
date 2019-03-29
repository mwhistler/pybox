import testbox


tbox = testbox.Testbox("COM46")

#tbox.read_registers()
#tbox.print_registers()

tbox.cmd_write_register('REG_CALIBRATION_WARNING_TIMESTAMP', [0x00, 0x00, 0x00, 0x00])

tbox.cmd_channel_config('REL0', ['PULSE', 'N_OPEN', 100, 200])
tbox.cmd_channel_config('REL1', ['PULSE', 'N_OPEN', 100, 200])
tbox.cmd_channel_config('REL2', ['PULSE', 'N_OPEN', 100, 200])
tbox.cmd_channel_config('REL3', ['PULSE', 'N_OPEN', 100, 200])

tbox.cmd_set_channel('REL0', 3)
tbox.cmd_set_channel('REL1', 3)
tbox.cmd_set_channel('REL2', 3)
tbox.cmd_set_channel('REL3', 3)

tbox.close()
