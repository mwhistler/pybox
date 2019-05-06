import testbox
from testbox_fixture import TestBoxFixture


tbox = testbox.TestBox("COM46", False)

fx = TestBoxFixture(tbox)
# examples:

tbox.cmd_write_register('REG_CALIBRATION_WARNING_TIMESTAMP', [0x00, 0x00, 0x00, 0x00])

fx.channel_config('REL1', ['PULSE', 'N_OPEN', 100, 200])

fx.channel_config('PWM0', ['STATIC', 'N_OFF', 1, 1, 10000])  # full params,use for PWM
fx.channel_config('OD0', ['STATIC', 'N_OFF'])  # without optional parameters, use for OD or PWM as static/pulse
fx.channel_config('OD1', ['PULSE', 'N_OFF', 100, 200, 10000])
fx.channel_config('PWR0', [5000, 'OFF_SHORTCUT'])

fx.set_channel('REL1', 3)

fx.set_channel('PWR0', 1)
fx.delay(1)

if fx.get_channel('VIN0').value > 2:
    print("WIEKSZE")
else:
    print("MNIEJSZE")

fx.set_channel('PWR0', 0)

# tbox.cmd_set_channel('OD1', 5)

# tbox.channels.VIN0.configure('STATIC', 'N_OFF', 1, 1, 10000)
# tbox.channels.VIN0.set(1)
# tbox.channels.VIN0.get()

tbox.close()
