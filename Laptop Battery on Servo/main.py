import psutil
import time
import serial

COM = "COM7"
ser = serial.Serial(COM, 9600,timeout=1)

while True:
    time.sleep(1)
    battery_percent = str(psutil.sensors_battery()[0])
    ser.write(bytearray(battery_percent.encode()))
    reachedPos = str(ser.readline())
    print(reachedPos)

