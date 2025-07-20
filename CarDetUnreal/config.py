import os
import numpy as np

# Пути и настройки
JSON_PATH = os.path.expanduser(r"C:\Users\az09c\OneDrive\Desktop\DeepInspect\Windows\JSON\vaqt.json")

# Конфигурация дорог
ROADS = {
    "south": {
        "poly": np.array([[146, 672], [33, 707], [795, 1076], [889, 886]], np.int32),
        "color": (0, 0, 255),
        "index": 0
    },
    "west": {
        "poly": np.array([[1117, 733], [1002, 776], [1778, 1071], [1884, 861]], np.int32),
        "color": (255, 255, 0),
        "index": 1
    },
    "east": {
        "poly": np.array([[1083, 81], [964, 85], [1414, 528], [1820, 516]], np.int32),
        "color": (0, 255, 0),
        "index": 2
    },
    "north": {
        "poly": np.array([[63, 120], [2, 206], [637, 524], [828, 338]], np.int32),
        "color": (255, 0, 0),
        "index": 3
    }
}

ROAD_ORDER = ["south", "west", "east", "north"]