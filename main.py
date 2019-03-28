import testbox

tbox = testbox.Testbox("COM6")
tbox.read_registers()
tbox.print_registers()

tbox.cmd_write_register('REG_CALIBRATION_WARNING_TIMESTAMP', bytearray([0x11, 0x22, 0x33, 0x44]))
