import cv2
import numpy as np
from ultralytics import YOLO
import mss
import time
from config import ROADS
from json_handler import update_json


def main():
    # Инициализация YOLO
    model = YOLO("yolov8x.pt").to("cuda")

    with mss.mss() as sct:
        monitor = sct.monitors[1]
        last_update = time.time()

        while True:
            # Захват экрана
            img = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            # Детекция машин
            results = model(frame)[0]
            counts = {name: 0 for name in ROADS}

            for box in results.boxes:
                if int(box.cls[0]) not in [2, 5, 7]:  # Только машины
                    continue

                # Определяем центр объекта
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                # Проверяем принадлежность к дороге
                for name, data in ROADS.items():
                    if cv2.pointPolygonTest(data["poly"], (cx, cy), False) > 0:
                        counts[name] += 1
                        cv2.rectangle(frame, (x1, y1), (x2, y2), data["color"], 2)
                        cv2.putText(frame, name, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, data["color"], 2)
                        break

            # Визуализация дорог
            for name, data in ROADS.items():
                cv2.polylines(frame, [data["poly"]], True, data["color"], 2)
                M = cv2.moments(data["poly"])
                if M["m00"] > 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    cv2.putText(frame, str(counts[name]), (cx - 20, cy),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, data["color"], 2)

            # Обновление JSON каждую секунду
            if time.time() - last_update >= 1:
                update_json(counts)
                last_update = time.time()

            # Отображение
            cv2.imshow("Traffic Monitoring", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()