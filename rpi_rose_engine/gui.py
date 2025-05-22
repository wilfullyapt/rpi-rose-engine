# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox

class GUI:
    """Graphical user interface for the rose engine controller."""
    def __init__(self, root, svg_processor, motor_controller):
        self.root = root
        self.svg_processor = svg_processor
        self.motor_controller = motor_controller

        # GUI elements
        tk.Label(root, text="Scale factor:").grid(row=0, column=0)
        self.scale_entry = tk.Entry(root)
        self.scale_entry.insert(0, "1.0")
        self.scale_entry.grid(row=0, column=1)

        tk.Label(root, text="Feed rate (mm/rot):").grid(row=1, column=0)
        self.feed_entry = tk.Entry(root)
        self.feed_entry.insert(0, "0.1")
        self.feed_entry.grid(row=1, column=1)

        tk.Label(root, text="Number of rotations:").grid(row=2, column=0)
        self.rotations_entry = tk.Entry(root)
        self.rotations_entry.insert(0, "1")
        self.rotations_entry.grid(row=2, column=1)

        self.file_label = tk.Label(root, text="No file selected")
        self.file_label.grid(row=3, column=0, columnspan=2)

        self.load_button = tk.Button(root, text="Load SVG", command=self.load_svg)
        self.load_button.grid(row=4, column=0)

        self.start_button = tk.Button(root, text="Start", command=self.start_cutting, state=tk.DISABLED)
        self.start_button.grid(row=4, column=1)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_cutting, state=tk.DISABLED)
        self.stop_button.grid(row=5, column=0, columnspan=2)

    def load_svg(self):
        """Load an SVG file and prepare for cutting."""
        file_path = filedialog.askopenfilename(filetypes=[("SVG files", "*.svg")])
        if not file_path:
            return
        try:
            scale_factor = float(self.scale_entry.get())
            self.svg_processor.load_svg(file_path, scale_factor)
            self.file_label.config(text=f"Selected file: {file_path.split('/')[-1]}")
            self.start_button.config(state=tk.NORMAL)
        except ValueError as e:
            messagebox.showerror("Invalid Input", "Scale factor must be a number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load SVG: {e}")

    def start_cutting(self):
        """Start the cutting process."""
        try:
            feed_rate = float(self.feed_entry.get())
            num_rotations = int(self.rotations_entry.get())
            r_steps = self.svg_processor.get_r_steps()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

            def on_finish():
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)

            self.motor_controller.start(r_steps, feed_rate, num_rotations, on_finish)
        except ValueError:
            messagebox.showerror("Invalid Input", "Feed rate and rotations must be valid numbers")

    def stop_cutting(self):
        """Stop the cutting process."""
        self.motor_controller.stop()
