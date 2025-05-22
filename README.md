# RPi Rose Engine

A Tkinter GUI application to drive an electrical rose engine using vector graphics (SVG rosettes) on a Raspberry Pi.


## Project Structure

- `rpi_rose_engine/`: Python package containing core modules (`config`, `gui`, `svg_parser`, `motor_control`, `mock_gpio`).
- `scripts/`: Executable scripts, including `main.py` (application entry point).
- `tests/`: Directory for future unit tests.
- `pyproject.toml`: Poetry configuration for dependencies and packaging.
- `README.md`, `LICENSE.txt`: Documentation and licensing.

## Prerequisites

- Raspberry Pi with GPIO access
- Three stepper motors with drivers connected to GPIO pins (see `rpi_rose_engine/config.py`)
- Python 3.10 or higher
- Poetry for package management

## Installation

```bash
git clone https://github.com/yourusername/rpi-rose-engine.git
cd rpi-rose-engine
poetry install
poetry run rpi-rose-engine
```
> [!NOTE]
> This program uses a `mock_gpio.py` module for testing and development on non-Raspberry Pi Debian systems.

## Initial Results
![Working result](resources/init_vibe_code_results.png)
