# Make sure you've uploaded `motor_driver.py` to the Pico board

from motor_driver import MotorDriver
from machine import Pin
from time import sleep

# SETUP
md = MotorDriver(15, 13, 14)  # left motor
STBY = Pin(12, Pin.OUT)
STBY.off()

# LOOP
STBY.on()  # enable motor driver
# Forwardly ramp up and down
for i in range(100):
    md.forward((i + 1) / 100)
    print(f"f, dc: {i}%")
    sleep(4 / 100)  # 4 seconds to ramp up
for i in reversed(range(100)):
    md.forward((i + 1) / 100)
    print(f"f, dc: {i}%")
    sleep(2 / 100)  # 2 seconds to ramp down
# Backwardly ramp up and down
for i in range(100):
    md.backward((i + 1) / 100)
    print(f"b, dc: {i}%")
    sleep(2 / 100)  # 2 seconds to ramp up
for i in reversed(range(100)):
    md.backward((i + 1) / 100)
    print(f"b, dc: {i}%")
    sleep(4 / 100)  # 4 seconds to ramp down

# Terminate
md.stop()
print("motor stopped.")
sleep(0.1)  # full stop
STBY.off()  # disable motor driver
print("motor driver disabled.")
