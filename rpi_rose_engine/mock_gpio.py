# mock_gpio.py
"""Mock implementation of RPi.GPIO for testing on non-Raspberry Pi systems."""

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MockGPIO:
    # Constants to mimic RPi.GPIO
    HIGH = 1
    LOW = 0
    OUT = "OUT"
    BCM = "BCM"

    def __init__(self):
        self.pins = {}  # Store pin configurations and states
        self.mode = None

    def setmode(self, mode):
        """Set the GPIO mode (e.g., BCM)."""
        self.mode = mode
        logger.debug(f"Set GPIO mode to {mode}")

    def setup(self, pin, mode):
        """Set up a pin as input or output."""
        self.pins[pin] = {"mode": mode, "state": self.LOW}
        logger.debug(f"Setup pin {pin} as {mode}")

    def output(self, pin, state):
        """Set the output state of a pin."""
        if pin not in self.pins:
            logger.warning(f"Pin {pin} not set up, assuming OUTPUT")
            self.pins[pin] = {"mode": self.OUT, "state": state}
        else:
            self.pins[pin]["state"] = state
        logger.debug(f"Set pin {pin} to {'HIGH' if state == self.HIGH else 'LOW'}")

    def cleanup(self):
        """Clean up GPIO pins."""
        self.pins.clear()
        logger.debug("GPIO cleanup performed")

# Export the mock GPIO class as the module
GPIO = MockGPIO()
