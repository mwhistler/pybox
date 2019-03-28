import testbox

tbox = testbox.Testbox("COM6")
for register in testbox.testBoxRegisters.keys():
    tbox.cmd_read_register(register)
# tbox.cmd_read_register('REG_SOFTWARE_VERSION')
tbox.print_registers()
