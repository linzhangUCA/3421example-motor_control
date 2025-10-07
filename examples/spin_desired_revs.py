from encoded_motor_driver import EncodedMotorDriver
from machine import Pin
from time import sleep  

# SETUP
emd = EncodedMotorDriver((9, 11, 10), (7, 8))  # left motor, encoders on pins 7 and 8
STBY = Pin(12, Pin.OUT)
STBY.off()
# Constants
CPR = 28
GEAR_RATIO = 98.5
TARGET_REVS = 10
TARGET_COUNTS = CPR * GEAR_RATIO * TARGET_REVS 

# LOOP
STBY.on()  # enable motor driver
while emd.encoder_counts < TARGET_COUNTS:
    emd.forward(0.3)
    print(f"f, enc_cnt: {emd.encoder_counts}")
    sleep(0.001)  # check every 0.01 second
emd.stop()
print("motor stopped.")
sleep(1)
STBY.off()  # disable motor driver