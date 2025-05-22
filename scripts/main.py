""" Main entry point """

import tkinter as tk
import atexit
import platform

if platform.system() == "Linux" and "raspberrypi" in platform.uname().release.lower():
    import RPi.GPIO as GPIO
else:
    from rpi_rose_engine.mock_gpio import GPIO

from rpi_rose_engine.gui import GUI
from rpi_rose_engine.svg_parser import SVGProcessor
from rpi_rose_engine.motor_control import MotorController

def main():
    """Initialize and run the rose engine controller."""
    atexit.register(GPIO.cleanup)
    root = tk.Tk()
    root.title("Rose Engine Controller")
    svg_processor = SVGProcessor()
    motor_controller = MotorController()
    gui = GUI(root, svg_processor, motor_controller)
    root.mainloop()

if __name__ == "__main__":
    main()
