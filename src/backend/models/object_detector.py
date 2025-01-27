import torch
from PIL import Image
import torchvision.transforms as transforms

class ObjectDetector:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(self.device)
        self.model.eval()
        self.transforms = transforms.Compose([
            transforms.Resize((640, 640)),
            transforms.ToTensor(),
        ])
        self.classes = self.model.module.names if hasattr(self.model, 'module') else self.model.names

    def preprocess_image(self, image):
         image = image.convert("RGB")
         image = self.transforms(image).unsqueeze(0).to(self.device)
         return image

    def detect_objects(self, image):
        preprocessed_image = self.preprocess_image(image)
        with torch.no_grad():
            results = self.model(preprocessed_image)
            detections = results.pandas().xyxy[0]
            detections = detections[['name', 'confidence']]
        if detections.empty:
          return None
        detections = detections.sort_values(by=['confidence'], ascending=False)
        return detections.iloc[0]['name']