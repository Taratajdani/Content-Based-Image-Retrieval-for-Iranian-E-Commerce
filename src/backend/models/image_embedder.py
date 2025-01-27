import torch
from PIL import Image
import torchvision.transforms as transforms
from transformers import AutoModel, AutoImageProcessor

class ImageEmbedder:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_id = 'google/vit-base-patch16-224'
        self.model = AutoModel.from_pretrained(self.model_id).to(self.device)
        self.processor = AutoImageProcessor.from_pretrained(self.model_id)
        self.model.eval()

    def preprocess_image(self, image):
        image = self.processor(images=image, return_tensors="pt").to(self.device)
        return image

    def generate_embedding(self, image):
      with torch.no_grad():
        preprocessed_image = self.preprocess_image(image)
        outputs = self.model(**preprocessed_image)
        embedding = outputs.last_hidden_state.mean(dim=1)
      return embedding.cpu().numpy()
import sys

for p in sys.path:
    print( p )
