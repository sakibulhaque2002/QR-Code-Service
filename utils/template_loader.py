# utils/template_loader.py

import json
import os

def load_templates():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(base_dir, "templates", "qr_templates.json")

    if not os.path.exists(template_path):
        raise FileNotFoundError("qr_templates.json not found")

    with open(template_path, "r") as f:
        return json.load(f)
