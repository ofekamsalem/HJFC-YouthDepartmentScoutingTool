import json
import os

  
def load_config():
    project_root = os.path.dirname(os.path.dirname(__file__))   # goes up to ScoutingTool/
    config_path = os.path.join(project_root, "config", "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)