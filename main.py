import testbox

tbox = testbox.Testbox("COM6")

tbox.read_registers()
tbox.print_registers()

tbox.cmd_write_register('REG_CALIBRATION_WARNING_TIMESTAMP', bytearray([0x00, 0x00, 0x00, 0x00]))

tbox.close()
