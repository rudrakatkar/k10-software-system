from ultralytics import YOLO
import cv2

class YOLOOBBDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def infer(self, frame):
        results = self.model.predict(
            source=frame,
            imgsz=640,
            conf=0.3,
            verbose=False
        )

        for r in results:
            if r.obb is None:
                continue
            for obb in r.obb:
                pts = obb.xyxyxyxy[0].cpu().numpy().astype(int)
                cv2.polylines(
                    frame,
                    [pts.reshape((-1,1,2))],
                    True,
                    (0,255,0),
                    2
                )
        return frame
