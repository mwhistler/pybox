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
fx.set_channel('REL0', 1)
fx.set_channel('REL1', 1)
fx.set_channel('REL2', 1)
fx.set_channel('REL3', 1)

# Ammeter calibration
print("wylaczenie zasilania")
fx.set_channel('PWR1', 0)
fx.channel_config('OD1', ['STATIC', 'N_OFF'])  # without optional parameters, use for OD or PWM as static/pulse
fx.set_channel('OD1', 1)                #power off
fx.channel_config('PWR0', [3600, 'OFF_HIZ'])
fx.channel_config('AMP0', ['IR_LOW', 128])
print("Wlacz zasilanie 3,0V na wejście amperomierza")
fx.set_channel('PWR0', 1)
print("Kalibruj amperomierz")
fx.delay(1)
fx.tb.cmd_amp0_calibrate('AMP0', 'DEV_CTRL_AMMETER_OFFSET_NULL')
current = fx.get_channel('AMP0').value

if current != 0:
    print("Kalibracja amperomierza niepowiodla sie")
    exit(-1)

print("Amperomierz skalibrowany")
fx.set_channel('OD1', 0)                #power on
print("Zasilanie DUTa podlaczone")


tbox.close()
