# Make sure you've uploaded `dual_motor_driver.py` to the Pico board

from dual_motor_driver import DualMotorDriver
from time import sleep

# SETUP
dmd = DualMotorDriver(right_ids=(9, 11, 10), left_ids=(15, 13, 14), stby_id=12)

# LOOP
# Forward ramp up and down
for i in range(100):
    dmd.linear_forward((i + 1) / 100)
    print(f"f, dc: {i}%")
    sleep(8 / 100)  # 8 seconds to ramp up
for i in reversed(range(100)):
    dmd.linear_forward((i + 1) / 100)
    print(f"f, dc: {i}%")
    sleep(7 / 100)  # 7 seconds to ramp down
# Backward ramp up and down
for i in range(100):
    dmd.linear_backward((i + 1) / 100)
    print(f"b, dc: {i}%")
    sleep(6 / 100)  #  6 seconds to ramp up
for i in reversed(range(100)):
    dmd.linear_backward((i + 1) / 100)
    print(f"b, dc: {i}%")
    sleep(5 / 100)  #  5 seconds to ramp down
# Left ramp up and down
for i in range(100):
    dmd.angular_left((i + 1) / 100)
    print(f"l, dc: {i}%")
    sleep(4 / 100)  #  4 seconds to ramp up
for i in reversed(range(100)):
    dmd.angular_left((i + 1) / 100)
    print(f"l, dc: {i}%")
    sleep(3 / 100)  #  3 seconds to ramp down
# Right ramp up and down
for i in range(100):
    dmd.angular_right((i + 1) / 100)
    print(f"r, dc: {i}%")
    sleep(2 / 100)  #  2 seconds to ramp up
for i in reversed(range(100)):
    dmd.angular_right((i + 1) / 100)
    print(f"r, dc: {i}%")
    sleep(1 / 100)  #  1 second to ramp down

# Terminate
dmd.stop()
print("motors stopped.")
sleep(0.1)  # full stop
dmd.disable()  # disable motor driver
print("motor driver disabled.")

