from motor_driver import MotorDriver
from machine import Pin

class EncodedMotorDriver(MotorDriver):
    def __init__(self, driver_ids, encoder_ids) -> None:
        super().__init__(*driver_ids)
        self.enc_a_pin = Pin(encoder_ids[0], Pin.IN)
        self.enc_b_pin = Pin(encoder_ids[1], Pin.IN)
        self.enc_a_pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._update_counts_a)
        self.enc_b_pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._update_counts_b)
        # variables
        self._enc_a_val = self.enc_a_pin.value()
        self._enc_b_val = self.enc_b_pin.value()
        self.encoder_counts = 0

    def _update_counts_a(self, pin):
        self._enc_a_val = pin.value()
        if self._enc_a_val == 1:
            if self._enc_b_val == 0:  # a=1, b=0
                self.encoder_counts += 1
            else:  # a=1, b=1
                self.encoder_counts -= 1
        else:
            if self._enc_b_val == 0:  # a=0, b=0
                self.encoder_counts -= 1
            else:  # a=0, b=1
                self.encoder_counts += 1

    def _update_counts_b(self, pin):
        self._enc_b_val = pin.value()
        if self._enc_b_val == 1:
            if self._enc_a_val == 0:  # b=1, a=0
                self.encoder_counts -= 1
            else:  # b=1, a=1
                self.encoder_counts += 1
        else:
            if self._enc_a_val == 0:  # b=0, a=0
                self.encoder_counts += 1
            else:  # b=0, a=1
                self.encoder_counts -= 1

    def reset_encoder_counts(self):
        self.encoder_counts = 0

# TEST
if __name__ == "__main__":  # Test only the encoder part
    from time import sleep

    # SETUP
    emd = EncodedMotorDriver((9, 11, 10), (7, 8))  # channel A motor, encoders on pins 7 and 8
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
        print(f"b, dc: {i}%, enc_cnt: {emd.encoder_counts}")
        sleep(4 / 100)  # 4 seconds to ramp up
    for i in reversed(range(100)):
        emd.backward((i + 1) / 100)
        print(f"b, dc: {i}%, enc_cnt: {emd.encoder_counts}")
        sleep(4 / 100)  # 4 seconds to ramp down

    # Terminate
    emd.stop()