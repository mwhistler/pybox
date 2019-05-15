import testbox
from testbox_fixture import TestBoxFixture


tbox = testbox.TestBox("COM46", True)

fx = TestBoxFixture(tbox)

fx.channel_config('AMP0', ['IR_LOW', 128])  #Dokladny zakres
fx.delay(1)
current = fx.get_channel('AMP0').value
fx.channel_config('AMP0', ['IR_HIGH', 128])
print("Zmierzony prad = " + str(current))


tbox.close()
