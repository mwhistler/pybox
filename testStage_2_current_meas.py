import testbox
from testbox_fixture import TestBoxFixture


tbox = testbox.TestBox("COM46", True)

fx = TestBoxFixture(tbox)


current = fx.get_channel('AMP0').value
print("Zmierzony prad = " + str(current))


tbox.close()
