from encoded_motor_driver import EncodedMotorDriver
from machine import Pin, Timer
from math import pi


class SentientWheelDriver(EncodedMotorDriver):
    def __init__(self, driver_ids, encoder_ids) -> None:
        super().__init__(driver_ids, encoder_ids)

        # Constants
        self.wheel_radius = 0.025  # m
        self.gear_ratio = 98.5
        self.cpr = 28  # CPR = PPR * 4
        self.meas_freq = 100  # Hz
        # Velocity measuring timer
        self.vel_meas_timer = Timer(
            freq=self.meas_freq,
            mode=Timer.PERIODIC,
            callback=self.measure_velocity,
        )
        # Variables
        self._enc_a_val = self.enc_a_pin.value()
        self._enc_b_val = self.enc_b_pin.value()
        self.encoder_counts = 0
        self.prev_counts = 0
        self.meas_ang_vel = 0.0
        self.meas_lin_vel = 0.0

    def reset_encoder_counts(self):
        self.encoder_counts = 0

    def measure_velocity(self, timer):
        curr_counts = self.encoder_counts
        delta_counts = curr_counts - self.prev_counts
        self.prev_counts = curr_counts  # UPDATE previous counts
        counts_per_sec = delta_counts * self.meas_freq  # delta_c / delta_t
        orig_rev_per_sec = counts_per_sec / self.cpr
        orig_rad_per_sec = orig_rev_per_sec * 2 * pi  # original motor shaft velocity
        self.meas_ang_vel = orig_rad_per_sec / self.gear_ratio
        self.meas_lin_vel = self.meas_ang_vel * self.wheel_radius


# TEST
if __name__ == "__main__":  # Test only the encoder part
    from time import sleep

    # SETUP
    swd = SentientWheelDriver(
        driver_ids=(9, 11, 10),
        encoder_ids=(16, 17),
    )  # right motor, encoder's green and yellow on GP16 and GP17
    # swd = SentientWheelDriver(
    #     driver_ids=(15, 13, 14),
    #     encoder_ids=(18, 19),
    # )  # left motor, encoder's green and yellow on GP18 and GP19
    STBY = Pin(12, Pin.OUT)
    STBY.off()

    # LOOP
    STBY.on()  # enable motor driver
    # Forwardly ramp up and down
    for i in range(100):
        swd.forward((i + 1) / 100)
        print()
        print(
            f"meas's angular velocity={swd.meas_ang_vel}, linear velocity={swd.meas_lin_vel}"
        )
        sleep(4 / 100)  # 4 seconds to ramp up
    for i in reversed(range(100)):
        swd.forward((i + 1) / 100)
        print(
            f"meas's angular velocity={swd.meas_ang_vel}, linear velocity={swd.meas_lin_vel}"
        )
        sleep(4 / 100)  # 4 seconds to ramp down
    # Backwardly ramp up and down
    for i in range(100):
        swd.backward((i + 1) / 100)
        print(
            f"meas's angular velocity={swd.meas_ang_vel}, linear velocity={swd.meas_lin_vel}"
        )
        sleep(4 / 100)  # 4 seconds to ramp up
    for i in reversed(range(100)):
        swd.backward((i + 1) / 100)
        print(
            f"meas's angular velocity={swd.meas_ang_vel}, linear velocity={swd.meas_lin_vel}"
        )
        sleep(4 / 100)  # 4 seconds to ramp down

    # Terminate
    swd.stop()
