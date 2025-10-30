from encoded_motor_driver import EncodedMotorDriver
from machine import Timer


class WheelController(EncodedMotorDriver):
    def __init__(self, driver_ids, encoder_ids) -> None:
        super().__init__(driver_ids, encoder_ids)
        # Constants
        self.k_p = 12.0
        self.k_i = 10.0
        self.k_d = 0.00001
        self.vel_reg_freq = 50  # Hz
        # Variables
        self.error = 0.0
        self.prev_error = 0.0
        self.error_inte = 0.0  # integral
        self.error_diff = 0.0  # differentiation
        self.ref_lin_vel = 0.0
        # PID controller config
        self.vel_reg_timer = Timer(
            freq=self.vel_reg_freq,
            mode=Timer.PERIODIC,
            callback=self.regulate_velocity,
        )

    def regulate_velocity(self, timer):
        if self.ref_lin_vel == 0.0:
            self.stop()
        else:
            self.error = self.ref_lin_vel - self.meas_lin_vel  # ang_vel also works
            self.error_inte = self.error_inte + self.error / self.vel_reg_freq
            self.error_diff = (self.error - self.prev_error) * self.vel_reg_freq
            duty = (
                self.k_p * self.error
                + self.k_i * self.error_inte
                + self.k_d * self.error_diff
            )
            if duty > 0:
                if duty > 1:
                    duty = 1
                self.forward(duty)
            else:
                if duty < -1:
                    duty = -1
                self.backward(-duty)

    def set_wheel_velocity(self, ref_lin_vel):
        self.ref_lin_vel = ref_lin_vel


if __name__ == "__main__":
    """ Use following tuning PID"""
    from utime import sleep
    from machine import Pin

    wc = WheelController(
        driver_ids=(15, 13, 14),
        encoder_ids=(18, 19),
    )
    STBY = Pin(12, Pin.OUT)
    STBY.on()
    for i in range(500):
        if i == 100:  # step up @ t=1 s
            wc.set_wheel_velocity(0.1)
        print(
            f"Reference velocity: {wc.ref_lin_vel} m/s, Measured velocity: {wc.meas_lin_vel} m/s"
        )
        sleep(0.01)

    wc.set_wheel_velocity(0)
    sleep(1)
    STBY.off()
