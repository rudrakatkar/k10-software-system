from ultralytics import YOLO
import torch


class YOLOOBBDetector:
    def __init__(self, model_path,
                 conf=0.5,
                 tracker="botsort.yaml",
                 imgsz=640):

        self.device = 0 if torch.cuda.is_available() else "cpu"
        self.conf = conf
        self.tracker = tracker
        self.imgsz = imgsz

        # Load model
        self.model = YOLO(model_path)
        self.model.to(self.device)

        print(f"[YOLO] Loaded on: {self.device}")
        if self.device != "cpu":
            print("[YOLO] GPU:", torch.cuda.get_device_name(0))

    def infer(self, frame):
        """
        Runs OBB tracking on a single frame
        Returns annotated frame
        """

        results = self.model.track(
            frame,
            task="obb",
            conf=self.conf,
            device=self.device,
            imgsz=self.imgsz,
            tracker=self.tracker,
            verbose=False,
            persist=True   # IMPORTANT for tracking continuity
        )

        annotated_frame = results[0].plot(
            font_size=0.6,
            line_width=1
        )

        return annotated_frame
