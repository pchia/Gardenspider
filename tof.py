import board
import busio
import adafruit_vl53l0x
import time
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl53l0x.VL53L0X(i2c)

distance = sensor.range
print (distance)


#while True:
#    distance = sensor.range
#    print (distance)
#    time.sleep(.5)
#print('Range: {}mm'.format(sensor.range))
