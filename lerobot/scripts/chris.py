import time

from lerobot.common.robot_devices.motors.feetech import FeetechMotorsBus as MotorBus

PORT = "/dev/tty.usbmodem58760432681" # Put YOUR port here

BAUDRATE = 1_000_000
MODEL = "sts3215"
MAX_MOTOR_ID = 10 # S100 only has 6...
SCAN_IDS = list(range(1, MAX_MOTOR_ID))


def monitor():
    # Initialize the MotorBus
    # - "motors" info is arbitrary here since we're using `read_with_motor_ids`
    # - XXX: Set to specific torque mode?
    motor_bus = MotorBus(
        port=PORT,
        motors={"motor": (1, MODEL)}, # name: (motor_idx, motor_model)
    )
    motor_bus.connect()

    # Monitor Motor Bus
    try:
        # Display some diagnostic info
        # - Baud rate
        # - Motor ids
        print("Baud rate:", motor_bus.port_handler.getBaudRate())
        motor_ids = motor_bus.find_motor_indices(possible_ids=SCAN_IDS)
        motor_models = [MODEL for _ in range(len(motor_ids))]
        n_motors = len(motor_ids)
        print("Motor ids:", motor_ids)

        # Continually monitor info for each servo
        print("\nMonitoring")
        prev_positions = [0 for _ in range(n_motors)]
        while True:
            time.sleep(1)

            positions = motor_bus.read_with_motor_ids(
                motor_models=motor_models,
                motor_ids=motor_ids,
                data_name="Present_Position",
            )
            positions_delta = [positions[i] - prev_positions[i] for i in range(n_motors)]
            prev_positions = positions
            print(
                "Positions",
                "[Abs]".rjust(10),
                " ".join([str(x).rjust(6) for x in positions]),
                "[Δ]".rjust(10),
                " ".join([str(x).rjust(6) for x in positions_delta]),
            )

    finally:
        motor_bus.disconnect()
        print("Disconnected from motor bus.")


if __name__ == "__main__":
    monitor()