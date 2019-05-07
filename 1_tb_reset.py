import testbox
from testbox_fixture import TestBoxFixture


tbox = testbox.TestBox("COM46", True)

fx = TestBoxFixture(tbox)


# testbox reset:

# Reset power
print("Resetowanie zasilan")
fx.set_channel('PWR1', 0)
fx.channel_config('PWR0', [3600, 'OFF_HIZ'])
fx.set_channel('PWR0', 0)
fx.delay(1)
fx.set_channel('PWR0', 1)

# Pulse input low state
print("Stan wyjsc w stan niski")
fx.set_channel('OD0', 0)
fx.set_channel('OD1', 0)
fx.set_channel('PWM0', 0)
fx.set_channel('PWM1', 0)
fx.set_channel('PWM2', 0)

# Turning off programmer
print("Odlaczenie programatora")
fx.set_channel('REL0', 0)
fx.set_channel('REL1', 0)
fx.set_channel('REL2', 0)
fx.set_channel('REL3', 0)

tbox.close()
