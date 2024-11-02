from machine import I2C, Pin

PETAL_ADDRESS = 0x00

i2c0 = I2C(0, sda=Pin(0), scl=Pin(1), freq=400_000)
i2c1 = I2C(1, sda=Pin(26), scl=Pin(27), freq=400_000)


def petal_init(bus):
    """configure the petal SAO"""
    bus.writeto_mem(PETAL_ADDRESS, 0x09, bytes([0x00]))  ## raw pixel mode (not 7-seg)
    bus.writeto_mem(PETAL_ADDRESS, 0x0A, bytes([0x09]))  ## intensity (of 16)
    bus.writeto_mem(PETAL_ADDRESS, 0x0B, bytes([0x07]))  ## enable all segments
    bus.writeto_mem(PETAL_ADDRESS, 0x0C, bytes([0x81]))  ## undo shutdown bits
    bus.writeto_mem(PETAL_ADDRESS, 0x0D, bytes([0x00]))  ##
    bus.writeto_mem(PETAL_ADDRESS, 0x0E, bytes([0x00]))  ## no crazy features (default?)
    bus.writeto_mem(PETAL_ADDRESS, 0x0F, bytes([0x00]))  ## turn off display test mode


petal_bus = None
try:
    petal_init(i2c0)
    petal_bus = i2c0
except:
    pass
try:
    petal_init(i2c1)
    petal_bus = i2c1
except:
    pass
if not petal_bus:
    print(f"Warning: Petal not found.")
