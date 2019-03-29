import testbox


tbox = testbox.Testbox("COM6")

# examples:

# tbox.read_registers()
# tbox.print_registers()

# tbox.cmd_write_register('REG_CALIBRATION_WARNING_TIMESTAMP', [0x00, 0x00, 0x00, 0x00])

tbox.cmd_channel_config('REL0', ['PULSE', 'N_OPEN', 100, 200])

tbox.cmd_channel_config('PWM0', ['STATIC', 'N_OFF', 1, 1, 10000])  # full params,use for PWM
tbox.cmd_channel_config('OD0', ['STATIC', 'N_OFF'])  # without optional parameters, use for OD or PWM as static/pulse
tbox.cmd_channel_config('OD0', ['STATIC', 'N_OFF', 1, 1, 10000])
tbox.cmd_channel_config('PWR0', [2000, 'OFF_HIZ'])

tbox.cmd_set_channel('REL0', 3)


tbox.close()
