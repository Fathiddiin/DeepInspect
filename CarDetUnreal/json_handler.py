import os
import json
from config import JSON_PATH, ROADS, ROAD_ORDER


def update_json(counts):
    """Обновляет JSON файл с количеством машин"""
    try:
        # Формируем строку времени
        time_parts = []
        for road in ROAD_ORDER:
            count = counts[road]
            time_parts.append(f"{4 + count * 2:02d}" if count > 0 else "00")

        time_str = "".join(time_parts) + "0"  # Последний 0 - заглушка для скорой

        # Безопасная запись
        os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
        temp_path = JSON_PATH + ".tmp"

        with open(temp_path, 'w') as f:
            json.dump({"time": time_str}, f)

        if os.path.exists(JSON_PATH):
            os.remove(JSON_PATH)
        os.rename(temp_path, JSON_PATH)

        print(f"Обновлено: {time_str}")
        return time_str

    except Exception as e:
        print(f"Ошибка записи JSON: {e}")
        return None