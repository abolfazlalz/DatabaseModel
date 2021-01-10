import json
from pathlib import Path
import os


class ConfigController:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        print(base_dir)
        f = open(base_dir, "r")
        lines = f.readline()
        self.configs = json.loads(lines)
