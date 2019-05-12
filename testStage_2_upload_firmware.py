import testbox
from testbox_fixture import TestBoxFixture


tbox = testbox.TestBox("COM46", True)

fx = TestBoxFixture(tbox)


# upload firmware:

# Config relays
fx.channel_config('REL0', ['STATIC', 'N_OPEN', 0, 0])
fx.channel_config('REL1', ['STATIC', 'N_OPEN', 0, 0])
fx.channel_config('REL2', ['STATIC', 'N_OPEN', 0, 0])
fx.channel_config('REL3', ['STATIC', 'N_OPEN', 0, 0])


# Turning on programmer
print("Podlaczenie programatora")
fx.set_channel('REL0', 0)
fx.set_channel('REL1', 0)
fx.set_channel('REL2', 0)
fx.set_channel('REL3', 0)

fx.delay(5)     # Czas na zaprogramowanie DUT'a

print("Odlaczenie programatora")
fx.set_channel('REL0', 1)
fx.set_channel('REL1', 1)
fx.set_channel('REL2', 1)
fx.set_channel('REL3', 1)


tbox.close()
