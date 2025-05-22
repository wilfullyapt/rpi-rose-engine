""" SVG parsing """

import math
import xml.etree.ElementTree as ET
from svg.path import parse_path
from shapely.geometry import Polygon, LineString, Point

from rpi_rose_engine import config

def parse_svg(file_path):
    """Parse an SVG file and return a Shapely Polygon."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    path_data = None
    for elem in root.iter():
        if elem.tag.endswith('path'):
            path_data = elem.get('d')
            break
    if not path_data:
        raise ValueError("No path found in SVG")
    path = parse_path(path_data)
    points = [(p.real, p.imag) for p in path]
    return Polygon(points)

def compute_r(polygon, theta_deg):
    """Compute the radial distance from center at angle theta_deg."""
    theta_rad = math.radians(theta_deg)
    line = LineString([(0, 0), (1000 * math.cos(theta_rad), 1000 * math.sin(theta_rad))])
    intersection = polygon.boundary.intersection(line)
    if not intersection:
        return 0
    point = intersection[0] if isinstance(intersection, list) else intersection
    return math.hypot(point.x, point.y)

class SVGProcessor:
    """Processes SVG files and computes radial steps."""
    def __init__(self):
        self.polygon = None
        self.r_steps = []

    def load_svg(self, file_path, scale_factor):
        """Load SVG and compute radial steps."""
        self.polygon = parse_svg(file_path)
        self.compute_r_steps(scale_factor)

    def compute_r_steps(self, scale_factor):
        """Compute radial steps based on polygon and scale factor."""
        thetas = [i * 360 / config.S1 for i in range(config.S1)]
        r_values = [compute_r(self.polygon, theta) for theta in thetas]
        r_physical = [r * scale_factor for r in r_values]
        self.r_steps = [int(r * config.S2) for r in r_physical]

    def get_r_steps(self):
        """Return computed radial steps."""
        return self.r_steps
