import cv2
import numpy as np
from config import EMERGENCY_SETTINGS


class EmergencyDetector:
    def __init__(self):
        self.settings = EMERGENCY_SETTINGS
        self.vehicle_history = {}

    def detect(self, vehicle_id, roi):
        """Определяет, является ли транспорт экстренным"""
        try:
            # Анализ верхней части (25%)
            h, w = roi.shape[:2]
            roof = roi[:h // 4, :]

            # Улучшение контраста
            hsv = cv2.cvtColor(roof, cv2.COLOR_BGR2HSV)
            hsv[:, :, 1] = cv2.equalizeHist(hsv[:, :, 1])

            # Цветовые маски
            red_mask = (
                    cv2.inRange(hsv, np.array(self.settings["red_lower1"]), np.array(self.settings["red_upper1"])) +
                    cv2.inRange(hsv, np.array(self.settings["red_lower2"]), np.array(self.settings["red_upper2"]))
            )
            blue_mask = cv2.inRange(hsv, np.array(self.settings["blue_lower"]), np.array(self.settings["blue_upper"]))

            # Морфологические операции
            kernel = np.ones((3, 3), np.uint8)
            red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
            blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)

            # Анализ контуров
            red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            red_area = sum(cv2.contourArea(cnt) for cnt in red_contours if
                           cv2.contourArea(cnt) > self.settings["min_contour_area"])
            blue_area = sum(cv2.contourArea(cnt) for cnt in blue_contours if
                            cv2.contourArea(cnt) > self.settings["min_contour_area"])

            # Логика подтверждения
            is_emergency = (red_area > 0) or (blue_area > 0)

            if vehicle_id not in self.vehicle_history:
                self.vehicle_history[vehicle_id] = {'frames': 0, 'emergency_frames': 0}

            if is_emergency:
                self.vehicle_history[vehicle_id]['emergency_frames'] += 1
            self.vehicle_history[vehicle_id]['frames'] += 1

            return self.vehicle_history[vehicle_id]['emergency_frames'] >= self.settings["emergency_frames_threshold"]

        except Exception as e:
            print(f"Detection error: {e}")
            return False

    def cleanup_history(self, current_vehicles):
        """Очистка истории для отсутствующих машин"""
        for vid in list(self.vehicle_history.keys()):
            if vid not in current_vehicles:
                del self.vehicle_history[vid]