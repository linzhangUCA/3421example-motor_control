from motor_driver import MotorDriver
from machine import Pin


class EncodedMotorDriver(MotorDriver):
    def __init__(self, driver_ids: list | tuple, encoder_ids: list | tuple) -> None:
        super().__init__(*driver_ids)
        # Pin configuration
        self.enc_a_pin = Pin(encoder_ids[0], Pin.IN)
        self.enc_b_pin = Pin(encoder_ids[1], Pin.IN)
        self.enc_a_pin.irq(
            trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.update_counts_a
        )
        self.enc_b_pin.irq(
            trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.update_counts_b
        )
        # Variables
        self.enc_a_val = self.enc_a_pin.value()
        self.enc_b_val = self.enc_b_pin.value()
        self.encoder_counts = 0
        self.prev_counts = 0
        self.meas_ang_vel = 0.0
        self.meas_lin_vel = 0.0

    def update_counts_a(self, pin):
        self.enc_a_val = pin.value()
        if self.enc_a_val == 1:
            if self.enc_b_val == 0:  # a=1, b=0
                self.encoder_counts += 1
            else:  # a=1, b=1
                self.encoder_counts -= 1
        else:
            if self.enc_b_val == 0:  # a=0, b=0
                self.encoder_counts -= 1
            else:  # a=0, b=1
                self.encoder_counts += 1

    def update_counts_b(self, pin):
        self.enc_b_val = pin.value()
        if self.enc_b_val == 1:
            if self.enc_a_val == 0:  # b=1, a=0
                self.encoder_counts -= 1
            else:  # b=1, a=1
                self.encoder_counts += 1
        else:
            if self.enc_a_val == 0:  # b=0, a=0
                self.encoder_counts += 1
            else:  # b=0, a=1
                self.encoder_counts -= 1

    def reset_encoder_counts(self):
        self.encoder_counts = 0


# TEST
if __name__ == "__main__":  # Test only the encoder part
    from utime import sleep

    # SETUP
    # emd = EncodedMotorDriver(
    #     driver_ids=(9, 11, 10),
    #     encoder_ids=(16, 17),
    # )  # right motor, encoder's green and yellow on GP19 and GP20
    emd = EncodedMotorDriver(
        driver_ids=(15, 13, 14),
        encoder_ids=(18, 19),
    )  # left motor, encoder's green and yellow on GP18 and GP19
    STBY = Pin(12, Pin.OUT)
    STBY.off()

    # LOOP
    STBY.on()  # enable motor driver
    # Forwardly ramp up and down
    for i in range(100):
        emd.forward((i + 1) / 100)
        print(f"f, dc: {i}%, enc_cnt: {emd.encoder_counts}")
        sleep(4 / 100)  # 4 seconds to ramp up
    for i in reversed(range(100)):
        emd.forward((i + 1) / 100)
        print(f"f, dc: {i}%, enc_cnt: {emd.encoder_counts}")
        sleep(4 / 100)  # 4 seconds to ramp down
    # Backwardly ramp up and down
    for i in range(100):
        emd.backward((i + 1) / 100)
        print(f"f, dc: {i}%, enc_cnt: {emd.encoder_counts}")
        sleep(4 / 100)  # 4 seconds to ramp up
    for i in reversed(range(100)):
        emd.backward((i + 1) / 100)
        print(f"f, dc: {i}%, enc_cnt: {emd.encoder_counts}")
        sleep(4 / 100)  # 4 seconds to ramp down

    # Terminate
    emd.stop()
    sleep(0.5)
    print("motor stopped.")
    STBY.off()  # disable motor driver
    print("motor driver disabled.")
