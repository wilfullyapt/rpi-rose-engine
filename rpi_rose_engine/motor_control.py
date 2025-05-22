""" Motor control for Raspberry Pi or mocked motor control """

import threading
import time
import platform

if platform.system() == "Linux" and "raspberrypi" in platform.uname().release.lower():
    import RPi.GPIO as GPIO
else:
    from rpi_rose_engine.mock_gpio import GPIO

from rpi_rose_engine import config

class MotorController:
    """Controls stepper motors for the rose engine."""
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        pins = [
            config.PIN_MOTOR1_STEP, config.PIN_MOTOR1_DIR,
            config.PIN_MOTOR2_STEP, config.PIN_MOTOR2_DIR,
            config.PIN_MOTOR3_STEP, config.PIN_MOTOR3_DIR
        ]
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        self.stop_flag = False

    def move_motor(self, step_pin, dir_pin, steps):
        """Move a motor a specified number of steps."""
        direction = GPIO.HIGH if steps > 0 else GPIO.LOW
        GPIO.output(dir_pin, direction)
        for _ in range(abs(steps)):
            if self.stop_flag:
                break
            GPIO.output(step_pin, GPIO.HIGH)
            time.sleep(config.STEP_DELAY)
            GPIO.output(step_pin, GPIO.LOW)
            time.sleep(config.STEP_DELAY)

    def start(self, r_steps, feed_rate, num_rotations, on_finish):
        """Start the cutting process in a separate thread."""
        self.stop_flag = False

        def thread_func():
            try:
                steps_per_rotation = config.S1
                feed_steps = int(feed_rate * config.S3)
                for _ in range(num_rotations):
                    if self.stop_flag:
                        break
                    for i, r_step in enumerate(r_steps):
                        if self.stop_flag:
                            break
                        # Move rotational motor one step
                        self.move_motor(config.PIN_MOTOR1_STEP, config.PIN_MOTOR1_DIR, 1)
                        # Adjust radial motor
                        self.move_motor(config.PIN_MOTOR2_STEP, config.PIN_MOTOR2_DIR, r_step)
                    # Advance feed motor
                    self.move_motor(config.PIN_MOTOR3_STEP, config.PIN_MOTOR3_DIR, feed_steps)
            finally:
                self.stop_flag = False
                on_finish()

        threading.Thread(target=thread_func).start()

    def stop(self):
        """Stop the cutting process."""
        self.stop_flag = True
