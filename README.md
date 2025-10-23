# 3421example-motor_control

## Example Wiring Diagram
### 1. Motors Only
![motor_driving](images/pico_tb6612.jpg)

### 2. Motors + Encoders
![motor_driving](images/encoder_motor_pico.jpg)

## Usage

Upload `.py` files from root of this repository to the Pico board.
>
> - [`motor_driver.py`](motor_driver.py)
> - [`dual_motor_driver.py`](dual_motor_driver.py)
> - [`encoded_motor_driver.py`](encoded_motor_driver.py)

In another MicroPython script which is going to run on Pico (~Local Python~), import the desired class to spin the motors.

1. Spin a single motor:

```Python
from motor_driver import MotorDriver
```

2. Spin two motors together:

```Python
from dual_motor_driver import DualMotorDriver
```

3. Count encoder pulses:

```Python
from encoded_motor_driver import EncodedMotorDriver
```
