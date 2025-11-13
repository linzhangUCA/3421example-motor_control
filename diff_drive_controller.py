from wheel_controller import WheelController


class diff_drive_controller:
    def __init__(self, left_ids: list | tuple, right_ids: list | tuple) -> None:
        self.left_wheel = WheelController(*left_ids)
        self.right_wheel = WheelController(*right_ids)

        # Variables
        self.meas_lin_vel = 0.0
        self.meas_ang_vel = 0.0

        # Constants
        self.WHEEL_SEP = 0.12  # wheel separation in meters


if __name__ == "__main__":
    from utime import sleep
