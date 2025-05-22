""" Hard coded config setting for hardware """


# Motor parameters
S1 = 200  # Steps per revolution for the rotational motor
S2 = 100  # Steps per mm for radial motor
S3 = 100  # Steps per mm for feed motor
STEP_DELAY = 0.001  # Delay between steps in seconds

# GPIO pin assignments
PIN_MOTOR1_STEP = 17  # Rotational motor step pin
PIN_MOTOR1_DIR = 18   # Rotational motor direction pin
PIN_MOTOR2_STEP = 22  # Radial motor step pin
PIN_MOTOR2_DIR = 23   # Radial motor direction pin
PIN_MOTOR3_STEP = 24  # Feed motor step pin
PIN_MOTOR3_DIR = 25   # Feed motor direction pin
