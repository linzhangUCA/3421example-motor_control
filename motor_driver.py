from machine import Pin, PWM


class MotorDriver:
    def __init__(self, pwm_id, in1_id, in2_id) -> None:
        self.pwm_pin = PWM(Pin(pwm_id))
        self.pwm_pin.freq(1000)
        self.in1_pin = Pin(in1_id, Pin.OUT)
        self.in2_pin = Pin(in2_id, Pin.OUT)

    def stop(self):
        self.pwm_pin.duty_u16(0)

    def forward(self, speed=0.0):  # map 0~65535 to 0~1
        assert 0 <= speed <= 1  # make sure speed in range [0, 1]
        self.in1_pin.off()
        self.in2_pin.on()
        self.pwm_pin.duty_u16(int(65535 * speed))

    def backward(self, speed=0.0):  # map 0~65535 to 0~1
        assert 0 <= speed <= 1  # make sure speed in range [0, 1]
        self.in1_pin.on()
        self.in2_pin.off()
        self.pwm_pin.duty_u16(int(65535 * speed))


# TEST
if __name__ == "__main__":
    from time import sleep

    # SETUP
    md = MotorDriver(9, 11, 10)  # right motor
    # md = MotorDriver(15, 13, 14)  # left motor
    STBY = Pin(12, Pin.OUT)
    STBY.off()

    # LOOP
    STBY.on()  # enable motor driver
    # Forwardly ramp up and down
    # Speed ramp up, use 4 seconds
    for i in range(100):
        md.forward((i + 1) / 100)
        print(f"duty cycle: {i}%")
        sleep(4 / 100)  # use 4 seconds to ramp up
    # Speed ramp down, 4 seconds
    for i in reversed(range(100)):
        md.forward((i + 1) / 100)
        print(f"duty cycle: {i}%")
        sleep(4 / 100)  # use 4 seconds to ramp up

    # Backwardly ramp up and down
    # Speed ramp up, use 4 seconds
    for i in range(100):
        md.backward((i + 1) / 100)
        print(f"duty cycle: {i}%")
        sleep(4 / 100)  # use 4 seconds to ramp up
    # Speed ramp down, 4 seconds
    for i in reversed(range(100)):
        md.backward((i + 1) / 100)
        print(f"duty cycle: {i}%")
        sleep(4 / 100)  # use 4 seconds to ramp up

    # Terminate
    md.stop()
    print("motor stopped.")
    sleep(0.1)  # full stop
    STBY.off()  # disable motor driver
    print("motor driver disabled.")
